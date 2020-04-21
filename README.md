[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# comparXiv 
A wrapper of [**latexdiff**](https://ctan.org/pkg/latexdiff?lang=en) to compare two version of an [arXiv](https://arxiv.org) preprint with a single command.

> This is a beta version. Despite extensive testing, it does not work for all preprints on arXiv. (Especially older preprints can be problematic.)

## BUILD AND COVERAGE STATUS

| Branch      | Build status |  Code coverage |
| ----------- | ----------- |----------- |
| master      | [![Build Status](https://travis-ci.com/temken/comparXiv.svg?token=CWyAeZfiHMD8t4eitDid&branch=master)](https://travis-ci.com/temken/comparXiv)      |		|
| dev   | [![Build Status](https://travis-ci.com/temken/comparXiv.svg?token=CWyAeZfiHMD8t4eitDid&branch=dev)](https://travis-ci.com/temken/comparXiv)        |			|

## INSTALLATION
You can install *comparxiv* via
```
pip install comparxiv
```

or direct from source

```
python setup.py install
```

## USAGE
To compare v1 and v2 of a paper with *comparxiv*, run e.g.
```
comparxiv 1905.06348 1 2
```

or simply

```
comparxiv hep-ph/0612370
```

(By default, comparxiv compares version 1 and 2).

A successful run will generate a pdf and open it.

For more details and options, run
```
comparxiv --help
```

## DEPENDENCIES

- a tex distribution with pdflatex and latexdiff
- argparse (*)
- tqdm (*)

> (*) Get installed automatically via pip, if necessary.

## VERSIONS

- **v0.1.0** (22/04/2020): First version released.

## AUTHORS & CONTACT

The author of this script is Timon Emken.

For questions, bug reports or other suggestions please contact [emken@chalmers.se](mailto:emken@chalmers.se).


## LICENCE

This project is licensed under the MIT License - see the LICENSE file.

## ACKNOWLEDGEMENTS

I am grateful for [this useful tutorial](https://python-packaging.readthedocs.io/en/latest/index.html) by Scott Torborg about python packaging.
