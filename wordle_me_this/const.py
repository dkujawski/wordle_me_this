""" Default configurations """
import os


N_START_WORDS = 5
WORDS_CONFIG = os.path.realpath(os.path.expanduser('~/.wmt'))
WORDS_CACHE = os.path.join(WORDS_CONFIG, 'words')
WORDS_FILE = '/usr/share/dict/words'
WORD_LENGHT = 5
VOWELS = set('aeiou')
