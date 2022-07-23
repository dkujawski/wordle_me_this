import os
import random
import string

from . import const


class ErrorWordsFileNotFound(Exception):
    """ not able to locate the dictionary words file on the local system """


def vowel_ratio(word: str):
    """ calculate ratio of vowels to consonants in the word """
    return len(const.VOWELS.intersection(set(word))) / float(len(word))


async def with_each_word_from_cache(func, letters: str = '', max_words: int = -1, dupes_ok: bool = True):
    """ check each word to see if it meets criteria """
    found = set()
    with open(const.WORDS_CACHE, 'r', encoding='utf-8') as wcfh:
        for line in wcfh:
            word = line.strip()
            if not word:
                break
            if not dupes_ok:
                if len(set(word)) < len(word):
                    continue
            if func(word, letters):
                found.add(word)
    if max_words > 0:
        found = sorted(found, key=vowel_ratio)[max_words*-3:]
        found = set(random.choices(list(found), k=max_words))
    return found


def start_words(word: str, max_words: int, dupes_ok: bool = False):
    """ words with no duplicate letters """
    return True


def words_with(word: str, letters: set):
    """ all letters in word """
    if not isinstance(letters, set):
        letters = set(letters)
    return letters.issubset(set(word))


def words_without(word: str, letters: set):
    """ word does not contain any letters """
    unique_letters_in_word = set(word)
    return len(unique_letters_in_word) == len(unique_letters_in_word.difference(letters))


def build_local_word_list():
    """ build the wordlist using the system word list """

    if not os.path.exists(const.WORDS_CONFIG):
        os.makedirs(const.WORDS_CONFIG, exist_ok=True)

    if not os.path.exists(const.WORDS_FILE):
        raise ErrorWordsFileNotFound()

    with open(const.WORDS_FILE, 'r') as wfh:
        with open(const.WORDS_CACHE, 'w', encoding='utf-8') as cfh:
            while True:
                line = wfh.readline()
                if not line:
                    break
                if line[0].isupper():
                    continue
                word = line.translate(str.maketrans('', '', string.punctuation))
                if len(word.strip()) == const.WORD_LENGHT:
                    cfh.write(word)
