import argparse
import glob
import hashlib
import json
import shutil
import subprocess
import tempfile
import mmap
import re

from datetime import datetime
from os import path, stat, mkdir, remove
from time import sleep

from settings import *
from db import DB, DoesNotExist

db = DB()

class ImproperlyConfigured(Exception):
    pass


class AlreadyImported(Exception):
    pass


class ProcessingError(Exception):
    pass


class Document(object):
    def __init__(self, document):
        if not path.exists(document):
            raise ProcessingError('Could not find document.')

        self.pages = {}
        self.path = document
        self.dest_base = tempfile.mkdtemp()
        self.dest_pages = path.join(self.dest_base, 'pages')

        # Create the pages directory if it doesn't exist yet
        if not path.exists(self.dest_pages):
            mkdir(self.dest_pages)

    @property
    def sha1(self):
        sha1 = hashlib.sha1()
        with open(self.path, 'rb') as f:
            for line in f:
                sha1.update(line)
        return sha1.hexdigest()

    @property
    def datetime_scan(self):
        return datetime.fromtimestamp(stat(self.path).st_mtime)

    @property
    def metadata(self):
        return {
            'original_name': path.basename(self.path),
            'title': '',
            'datetime_scan': self.datetime_scan.isoformat(),
            'datetime_document': '',
            'sha1': self.sha1,
            'tags': []
        }

    @property
    def final_destination_name(self):
        return '{}_{}'.format(
            self.datetime_scan.strftime('%Y-%m-%d_%H-%M-%S'),
            self.sha1
        )

    def process(self):
        try:
            db.get(self.sha1)
            raise AlreadyImported()
        except DoesNotExist:
            pass

        self.create_pages()
        self.create_ocr_text_files()
        self.create_metadata_file()
        self.copy_original()
        self.cleanup()
        self.move_to_final_destination()

    def _convert(self, settings=[], prefix='', fileformat='png'):
        if prefix:
            prefix = '{}-'.format(prefix)

        exit_code = subprocess.Popen((
            CONVERT_BIN, *CONVERT_DEFAULT_SETTINGS, *settings, self.path,
            path.join(self.dest_pages, '{}%04d.{}'.format(prefix, fileformat))
        )).wait()

        if exit_code != 0:
            raise ProcessingError(
                'Was unable to convert document to pngs ({}).'.format(exit_code)
            )

        return glob.glob(path.join(
            self.dest_pages, '{}[0-9][0-9][0-9][0-9].{}'.format(prefix,
                                                                fileformat)
        ))

    def create_pages(self):
        originals = self._convert()
        greyscales = self._convert(
            settings=['-type', 'grayscale'],
            prefix='grayscale',
            fileformat='pnm'
        )

        keys = [
            path.basename(png).replace('.png', '')
            for png in originals
        ]

        for idx, key in enumerate(keys):
            self.pages[key] = {
                'original': originals[idx],
                'greyscale': greyscales[idx],
            }

    def create_ocr_text_files(self):
        for key, page in self.pages.items():
            png = path.join(self.dest_pages, page['greyscale'])
            proc = subprocess.Popen((
                TESSERACT_BIN, png, 'stdout', '-l', TESSERACT_LANGUAGES
            ), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

            ocr_name = '{}.txt'.format(key)
            ocr_path = path.join(self.dest_pages, ocr_name)
            ocr_text = proc.communicate()[0].decode('utf-8')

            with open(ocr_path, 'w+') as f:
                f.write(ocr_text)

    def create_metadata_file(self):
        with open(path.join(self.dest_base, 'metadata.json'), 'w') as f:
            f.write(json.dumps(self.metadata, indent=4, sort_keys=True))

    def copy_original(self):
        dest = path.join(self.dest_base, 'original.pdf')
        shutil.copy2(self.path, dest)

    def cleanup(self):
        for key, page in self.pages.items():
            remove(page['greyscale'])

    def move_to_final_destination(self):
        shutil.move(
            self.dest_base,
            path.join(STORAGE_DIR, self.final_destination_name)
        )


class Consumer(object):
    def __init__(self, keep=False, continuous=False, interval=10):
        self._check_config()
        self.keep = keep
        self.continuous = continuous
        self.interval = interval

    def consume(self):
        while True:
            self._consume()
            if not self.continuous:
                break
            sleep(self.interval)


    def _consume(self):
        pdfs = glob.glob(path.join(CONSUME_DIR, '*.pdf'))

        for pdf in pdfs:
            document = Document(pdf)
            print('Importing {}... '.format(document.sha1), end='', flush=True)

            try:
                document.process()
            except AlreadyImported:
                print('Already imported.')
            else:
                print('Tagging... ', end='', flush=True)
                entry = db.get(document.sha1)
                entry.retag()
                print('Done.')
            finally:
                if not self.keep:
                    remove(pdf)

    def _check_config(self):
        error_msg = '{} directory does not exist.'

        if not path.exists(CONSUME_DIR):
            raise ImproperlyConfigured(error_msg.format('CONSUME_DIR'))

        if not path.exists(STORAGE_DIR):
            raise ImproperlyConfigured(error_msg.format('STORAGE_DIR'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Paperless consumer.')
    parser.add_argument('-k', '--keep', action='store_true',
                        help="dont't remove consumed documents")
    parser.add_argument('-c', '--continuous', action='store_true',
                        help='run consumer in a continuous loop')
    parser.add_argument('-i', '--interval', default=10, type=int,
                        help='interval in seconds for the continuous loop')

    consumer = Consumer()
    args = parser.parse_args(namespace=consumer)

    if args.interval < 1:
        parser.fail('--interval/-i has to be a postive integer')

    consumer.consume()
