#!/usr/bin/env python3
""" CLI tool for listing usable words for the wordle game """
import asyncio
import os
import random
import string

import click

N_START_WORDS = 5
WORDS_CONFIG = os.path.realpath(os.path.expanduser('~/.wmt'))
WORDS_CACHE = os.path.join(WORDS_CONFIG, 'words')
WORDS_FILE = '/usr/share/dict/words'
WORD_LENGHT = 5
VOWELS = set('aeiou')


class ErrorWordsFileNotFound(Exception):
    """ not able to locate the dictionary words file on the local system """


@click.command()
@click.option('--include', '-i', help='letters to include')
@click.option('--omit', '-o', help='letters to omit')
@click.option('--rebuild', is_flag=True, default=False, help='rebuild cached word')
def cli(include, omit, rebuild):
    """ list usable words from the local dict word list """

    if not os.path.exists(WORDS_CACHE) or rebuild:
        os.makedirs(WORDS_CONFIG, exist_ok=True)
        build_local_word_list(WORDS_CACHE)

    tasks = dict()

    loop = asyncio.get_event_loop()
    if include:
        tasks[id(include)] = loop.create_task(
            with_each_word_from_cache(words_with, include)
        )
    if omit:
        tasks[id(omit)] = loop.create_task(
            with_each_word_from_cache(words_without, omit)
        )
    if not include and not omit:
        tasks[None] = loop.create_task(
            with_each_word_from_cache(start_words, max_words=N_START_WORDS)
        )

    loop.run_until_complete(asyncio.wait(tasks.values()))

    if not include and not omit:
        for word in tasks[None].result():
            print(word)
    elif include and omit:
        for word in tasks[id(include)].result().intersection(tasks[id(omit)].result()):
            print(word)
    elif include:
        for word in tasks[id(include)].result():
            print(word)
    elif omit:
        for word in tasks[id(omit)].result():
            print(word)
    else:
        print('nothing to do')

    loop.close()


def sort_by_most_vowels(word: str):
    return len(VOWELS.intersection(set(word))) / float(len(word))

async def with_each_word_from_cache(func, letters: str = '', max_words: int = -1, dupes_ok: bool = True):
    found = set()
    with open(WORDS_CACHE, 'r', encoding='utf-8') as wcfh:
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
        found = sorted(found, key=sort_by_most_vowels)[max_words*-3:]
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


def build_local_word_list(output_file_path:str):
    if not os.path.exists(WORDS_FILE):
        raise ErrorWordsFileNotFound()

    with open(WORDS_FILE, 'r') as wfh:
        with open(WORDS_CACHE, 'w', encoding='utf-8') as cfh:
            while True:
                line = wfh.readline()
                if not line:
                    break
                word = line.translate(str.maketrans('', '', string.punctuation))
                if len(word.strip()) == WORD_LENGHT:
                    cfh.write(word)


if __name__ == '__main__':
    print('here we go...')
    t = asyncio.run(cli())

