#!/usr/bin/env python3
""" This is the main CLI entry point """
import asyncio
import os

import click
import tabulate

from . import const
from . import ops


@click.command()
@click.argument('position', required=False, default='', type=str)
@click.option('--include', '-i', help='letters to include')
@click.option('--omit', '-o', help='letters to omit')
@click.option('--dupes/--no-dupes', default=True, show_default=True, type=bool, help='allow dup letters in word')
@click.option('--rebuild', is_flag=True, default=False, help='rebuild cached word list')
def cli(position, include, omit, dupes, rebuild):
    """ list usable words from the local dict word list """

    if not os.path.exists(const.WORDS_CACHE) or rebuild:
        ops.build_local_word_list()

    tasks = dict()

    loop = asyncio.get_event_loop()
    if include:
        tasks[id(include)] = loop.create_task(
            ops.with_each_word_from_cache(
                ops.words_with,
                position,
                include,
                dupes_ok=dupes,
            )
        )
    if omit:
        tasks[id(omit)] = loop.create_task(
            ops.with_each_word_from_cache(
                ops.words_without,
                position,
                omit,
                dupes_ok=dupes
            )
        )
    if not include and not omit:
        tasks[None] = loop.create_task(
            ops.with_each_word_from_cache(
                ops.start_words,
                position,
                max_words=const.N_START_WORDS
            )
        )

    loop.run_until_complete(asyncio.wait(tasks.values()))

    words = list()
    if not include and not omit:
        words = [w for w in tasks[None].result()]
    elif include and omit:
        words = [w for w in tasks[id(include)].result().intersection(tasks[id(omit)].result())]
    elif include:
        words = [w for w in tasks[id(include)].result()]
    elif omit:
        words = [w for w in tasks[id(omit)].result()]

    loop.close()
    if words:
        print_columns(words)


def columns(data: list, n: int = 3):
    """ break out data list into 20 lists """
    count = int(len(data)/n)
    if count < 1:
        return [data]
    return [data[idx:idx+count] for idx in range(0, len(data), count)]


def print_columns(data: list):
    """ print in columns """
    print()
    print(tabulate.tabulate(columns(data), tablefmt='plain'))
    print()


if __name__ == '__main__':
    asyncio.run(cli())
