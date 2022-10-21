
[![Build Status](https://travis-ci.com/temken/comparxiv.svg?branch=main)](https://travis-ci.com/temken/comparxiv)
[![Coverage Status](https://coveralls.io/repos/github/temken/comparxiv/badge.svg?branch=main)](https://coveralls.io/github/temken/comparxiv?branch=main)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# comparxiv 

A wrapper of [**latexdiff**](https://ctan.org/pkg/latexdiff?lang=en) to compare two version of an [arXiv](https://arxiv.org) preprint with a single command.

<img src="https://user-images.githubusercontent.com/29034913/80139519-e28a4800-85a6-11ea-92f4-1210c1070376.png" width="750">

> **Disclaimer:** This is a beta version. Despite extensive testing, it does not work for all preprints on arXiv.

## INSTALLATION
You can install *comparxiv* via
```
pip install comparxiv
```

or direct from source.

```
git clone https://github.com/temken/comparxiv.git
cd comparxiv 
python setup.py install
```

## USAGE
There are three ways to run *comparxiv*:

**(A) ID**: The easiest way is to simply provide a preprint ID such as

```
comparxiv hep-ph/0612370
```

This will compare the two latest versions of the paper.

**(B) ID + version**: To compare version *N* with *N-1*, you can either run 
```
comparxiv 1709.06573vN 
```
or
```
comparxiv 1709.06573 N
```

**(B) ID + two versions**: To compare two specified version *N* and *M*, there are also two possible ways to give the input. Either
```
comparxiv 1905.06348 N M
```

or

```
comparxiv 1905.06348vN M 
```

The order of the two arguments (N and M) matters, the second version (M) is interpreted as the *new* version. 

A successful run will generate a pdf and open it.

For more details and options, run
```
comparxiv --help
```

## DEPENDENCIES

- [python](https://www.python.org/) and [pip](https://pypi.org/project/pip/)
- a tex distribution with [pdflatex](https://linux.die.net/man/1/pdflatex) and [latexdiff](https://ctan.org/pkg/latexdiff?lang=en) (*)
- [argparse](https://pypi.org/project/argparse/) (**)
- [arxiv](https://pypi.org/project/arxiv/) (**)
- [requests](https://pypi.org/project/requests/) (**)
- [tqdm](https://pypi.org/project/tqdm/) (**)

> (*) Are part of any tex distribution, which can be installed on Linux e.g. via
> ```
> sudo apt-get install texlive-full
> ```
> or on macOS e.g. using [homebrew](https://brew.sh/).
> ```
> brew cask install mactex
> ```
> (**): Get installed automatically via pip, if necessary.

## VERSIONS

- **v0.1** (24/04/2020): First version released.

## To-do list
Planned features

- comparison of figures
- support of latex papers on biorxiv (?)

## AUTHORS & CONTACT

The author of this script is Timon Emken.

For questions, bug reports or other suggestions please contact [emken@chalmers.se](mailto:emken@chalmers.se).


## LICENSE

This project is licensed under the MIT License - see the LICENSE file.

## ACKNOWLEDGEMENTS

I am grateful for [this useful tutorial](https://python-packaging.readthedocs.io/en/latest/index.html) by Scott Torborg about python packaging.
