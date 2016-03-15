import glob
import mmap
import re
import json

from os import path

from settings import *
from utils import isoformat_to_datetime


class DoesNotExist(Exception):
    pass


class InvalidKey(Exception):
    pass


class DBEntry(object):
    def __init__(self, key, storage=STORAGE_DIR):
        self.key = key
        self.storage = storage
        self._metadata = {}
        self._text = ''
        self.path = path.join(self.storage, self.key)
        self.path_metadata = path.join(self.path, 'metadata.json')
        self.path_pages = path.join(self.path, 'pages')

    @property
    def original_document_path(self):
        document = path.join(self.path, 'original.pdf')
        if not path.exists(document):
            raise DoesNotExist()
        return document

    @property
    def metadata(self):
        if not self._metadata:
            self._metadata = {
                'tags': [],
                'datetime_scan': None,
                'datetime_document': None,
                'original_name': '',
                'title': ''
            }
            with open(self.path_metadata, 'r') as f:
                self._metadata.update(json.load(f))
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        if not self._metadata:
            self.metadata
        self._metadata = value

    @property
    def text(self):
        if not self._text:
            texts = []
            for page in glob.glob(path.join(self.path, 'pages/*.txt')):
                with open(page, 'r') as f:
                    texts.append(f.read())
            self._text = '\n'.join(texts)
        return self._text

    @property
    def datetime_scan(self):
        isoformat = self.metadata.get('datetime_scan', None)
        return isoformat_to_datetime(isoformat)

    @property
    def datetime_document(self):
        isoformat = self.metadata.get('datetime_document', None)
        return isoformat_to_datetime(isoformat)

    @property
    def datetime(self):
        return (
            self.datetime_document
            if self.datetime_document else
            self.datetime_scan
        )

    @property
    def tags(self):
        return self.metadata.get('tags', [])

    @property
    def color_tags(self):
        tags = {}
        for tag in self.tags:
            tags[tag] = (
                TAG_DEFINITIONS.get(tag, {}).get('color', TAG_DEFAULT_COLOR)
            )
        return tags

    def write_metadata(self):
        with open(self.path_metadata, 'w') as f:
            f.write(json.dumps(self.metadata, indent=4, sort_keys=True))

    def match_tags(self):
        tags = []

        for key, info in TAG_DEFINITIONS.items():
            regex = None
            matching_algorithm = info.get('matching_algorithm')
            matching_term = info.get('match')

            if matching_algorithm == MATCH_ANY:
                words = matching_term.strip().split(' ')
                regex = re.compile(r'(?i)({})'.format(
                    '|'.join([r'\b{}\b'.format(word) for word in words])
                ))

            if matching_algorithm == MATCH_ALL:
                words = matching_term.strip().split(' ')
                regex = re.compile(r'(?i){}'.format(
                    ''.join([r'(?=.*\b{}\b)'.format(word) for word in words])
                ), re.DOTALL)

            if matching_algorithm == MATCH_LITERAL:
                regex = re.compile(r'(?i)(\b{}\b)'.format(matching_term))

            if matching_algorithm == MATCH_REGEX:
                regex = re.compile(matching_term, re.DOTALL)

            if regex and regex.search(self.text):
                tags.append(key)

        return tags

    def retag(self):
        tags = self.match_tags()
        self.metadata.update({'tags': tags})
        self.write_metadata()

    def contains_text(self, text):
        b_text = bytes(re.escape(text), 'utf-8')
        for page in glob.iglob(path.join(self.path_pages, '*.txt')):
            with open(page, 'rb', 0) as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
                    if re.search(br'(?i)%b' % b_text, s):
                        return True
        return False

    def __str__(self):
        return self.metadata.get('original_name')

    def __repr__(self):
        return self.__str__()


class DB(object):
    def __init__(self, storage=STORAGE_DIR):
        self.storage = storage

    def _get_key_from_path(self, dpath):
        result = re.search(
            (
                '^%s//?(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_[a-z0-9]{40}).*$' %
                re.escape(self.storage)
            ),
            dpath
        )
        return result.group(1) if result else None

    def all(self, sort=True):
        entries = [
            DBEntry(self._get_key_from_path(path))
            for path in glob.glob(path.join(self.storage, '*'))
        ]

        if sort:
            return sorted(entries, reverse=True,
                          key=lambda e: (e.datetime is None, e.datetime))
        return entries

    def get(self, sha1):
        if len(sha1) != 40:
            raise InvalidKey()

        result = glob.glob(path.join(self.storage, '*{}'.format(sha1)))

        if len(result) == 0:
            raise DoesNotExist()

        return DBEntry(self._get_key_from_path(result[0]))

    def filter(self, text='', tags=[]):
        entries = self.all()
        if tags:
            entries = filter(lambda e: set(tags).issubset(e.tags), entries)
        if text:
            entries = filter(lambda e: e.contains_text(text), entries)
        return entries
