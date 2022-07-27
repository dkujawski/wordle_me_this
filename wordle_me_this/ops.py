""" The ops module contains the word filtering logic.
"""
import os
import random
import string

from typing import Callable

from . import const


class ErrorWordsFileNotFound(Exception):
    """ not able to locate the dictionary words file on the local system """


class ErrorUnexpectedWordLength(Exception):
    """ word does not match expected word length """


def vowel_ratio(word: str) -> float:
    """ Calculate the ratio of vowels to consonants

    Args:
        word (str): the word to evaluate

    Returns:
        (float) between 0 and 1 where 1 is all vowels

    """
    return len(const.VOWELS.intersection(set(word))) / float(len(word))


async def with_each_word_from_cache(
    func: Callable,
    position: str,
    letters: str = '',
    max_words: int = -1,
    dupes_ok: bool = True,
    mostly_vowels: bool = False,
    random_sample: bool = False,
) -> list[str]:
    """ Iterate over each word in the words cache.
    Skip any words based on preset rules activated by passed in args.
    Evaluate ``func`` with each remaining word and ``letters``.

    Args:
        func (Callable): A function that takes ``word: str, letters: str`` and returns ``bool``.
            When ``True`` is returned include the word in the return list.
        position (str): A string of character representing the position of known letters
            using non-alpha letters to identify unkowns. Like: ``__a_k`` which will only include
            letters that contain an ``a`` in the third position and a ``k`` in the last position.
        letters (str): the letters to pass into ``func``
        max_words (int): limit the total returned word count to ``max_words``.
            When less than 1 all words will matching criterion will be returned.
        dupes_ok (bool): allow words that contain the same letter more than once
        mostly_vowels (bool): sort the found words so that words with more vowels are listed. Default: ``False``
        random_sample (bool): when ``max_words > 0`` take a random sample
            from the top ``3*max_words``. Default: ``False``

    Returns:
        (list[str]): words that fit the passed in criterion

    """
    found = set()
    with open(const.WORDS_CACHE, 'r', encoding='utf-8') as wcfh:
        for line in wcfh:
            word = line.strip()
            if not word:
                break
            if not dupes_ok:
                if len(set(word)) < len(word):
                    continue
            if not letters_match_with(word, position):
                continue
            if func(word, letters):
                found.add(word)
    if max_words > 0:
        if mostly_vowels:
            found = sorted(found, key=vowel_ratio, reverse=True)
        if random_sample and mostly_vowels:
            found = set(random.sample(found[:max_words*3], max_words))
        elif random_sample:
            found = set(random.sample(found, max_words))
        elif mostly_vowels:
            found = set(found[:max_words])

    return found


def letters_match_with(word: str, position: str) -> bool:
    """ Compare each character in ``word`` with the ``position`` key.
    The ``position`` is expected to be same length as ``word`` and contain
    alpha and non-alpha characters where a non-alpha character indicates an
    unknown letter for the given position.  Like: ``a___d`` where the first
    letter is known to be an ``a`` and the last letter is known to be a ``d``
    while the middle 3 letters are unknown.

    Args:
        word (str): the word being evaluated
        position (str): the position key, like ``_i_ch``

    Returns (bool):
        ``True`` when the letters of ``word`` match the ``position`` key

    """
    if len(position) and len(word) != len(position):
        raise ErrorUnexpectedWordLength(f"{word}:{len(word)} != {position}:{len(position)}")
    for idx, letter in enumerate(position):
        if letter not in string.ascii_lowercase:
            # letter is unknown at this position
            continue
        if word[idx] != letter:
            return False
    return True


def start_words(
    word: str,
    max_words: int,
    dupes_ok: bool = False,
    mostly_vowels: bool = True,
    random_sample: bool = True,
) -> bool:
    """ This is expected to be an interior function passed into the ``with_each_word_from_cache`` function
    Return a list of suitable starting words.
    Defaults are words with no duplicate letters and are mostly made of vowels.
    A different subset of words will be returned each time.

    Args:
        word (str): the word passed in from the outer function
        max_words (int): limit the number of words returned
        dupes_ok (bool): allow multiple letters of the same character in the word. Default ``False``
        mostly_vowels (bool): sort found words so that words made of mostly vowels are favored
        random_sample (bool): when ``max_words > 0`` return a random sample of ``max_words``
            from the top ``max_words * 3`` results

    Returns (bool):
        Always returns ``True``

    """
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
