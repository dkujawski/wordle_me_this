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
$ wordle-me-this --help
Usage: wordle-me-this [OPTIONS]

  list usable words from the local dict word list

Options:
  -i, --include TEXT  letters to include
  -o, --omit TEXT     letters to omit
  --rebuild           rebuild cached word
  --help              Show this message and exit.

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

