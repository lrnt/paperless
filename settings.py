from os import path

BASE_PATH = path.dirname(path.realpath(__file__))

CONSUME_DIR = path.join(BASE_PATH, 'consume')
STORAGE_DIR = path.join(BASE_PATH, 'storage')

CONVERT_BIN = '/usr/bin/convert'
CONVERT_DEFAULT_SETTINGS = ['-density', '300', '-depth', '8', '-scene', '1',
                            '-alpha', 'off']

TESSERACT_BIN = '/usr/bin/tesseract'
TESSERACT_LANGUAGES = 'eng'

MATCH_ANY = 1
MATCH_ALL = 2
MATCH_LITERAL = 3
MATCH_REGEX = 4

TAG_DEFAULT_COLOR = '#a6cee3'
TAG_DEFINITIONS = {
    'sometag': {
        'matching_algorithm': MATCH_ANY,
        'match': 'any of these words',
        'color': '#fb9a99'
    }
}

try:
    from settings_local import *
except ImportError:
    pass
