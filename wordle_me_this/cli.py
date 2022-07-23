#!/usr/bin/env python3
""" This is the main CLI entry point """
import asyncio
import os

import click

from . import const
from . import ops


@click.command()
@click.option('--include', '-i', help='letters to include')
@click.option('--omit', '-o', help='letters to omit')
@click.option('--rebuild', is_flag=True, default=False, help='rebuild cached word')
def cli(include, omit, rebuild):
    """ list usable words from the local dict word list """

    if not os.path.exists(const.WORDS_CACHE) or rebuild:
        ops.build_local_word_list()

    tasks = dict()

    loop = asyncio.get_event_loop()
    if include:
        tasks[id(include)] = loop.create_task(ops.with_each_word_from_cache(ops.words_with, include))
    if omit:
        tasks[id(omit)] = loop.create_task(ops.with_each_word_from_cache(ops.words_without, omit))
    if not include and not omit:
        tasks[None] = loop.create_task(ops.with_each_word_from_cache(ops.start_words, max_words=const.N_START_WORDS))

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


if __name__ == '__main__':
    asyncio.run(cli())
