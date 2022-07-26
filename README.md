# wordle_me_this
CLI wordle helper

This is mainly an opportunity to explore `asyncio` and `set` operations.  

# Build package

```
$ python3 -m pip install build_requirements.txt
$ python3 -m build
```

# Install

```
$ python -m pip install .
```

# Usage

```
Usage: python -m wordle_me_this [OPTIONS] [POSITION]

  list usable words from the local dict word list. use the POSITION argument
  to identify which letters should be in which places. any non-alpha letter
  for blanks.  like: ".o.e." or "s__rt"

Options:
  -i, --include TEXT    letters to include
  -o, --omit TEXT       letters to omit
  --dupes / --no-dupes  allow dup letters in word  [default: dupes]
  --rebuild             rebuild cached word list
  --help                Show this message and exit.
```

## Suggest a start word

```
$ wordle-me-this
auger
maize
anion
agile
toxic
```

## Suggest the next word based on include/omit

```
$ wordle-me-this --omit uger --include a
patsy
sandy
halos
nodal
salts
clamp
cilia
...
```

## Show words where 'a' is the second letter and 's' is the last letter
```
$ wordle-me-this _a__s -i y -o ktio

yawls  yawns  yards
babys  ladys  zanys
yarns  navys  manys
yawss

```
