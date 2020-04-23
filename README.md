
[![Build Status](https://travis-ci.com/temken/comparxiv.svg?branch=master)](https://travis-ci.com/temken/comparxiv)
[![Coverage Status](https://coveralls.io/repos/github/temken/comparxiv/badge.svg?branch=master)](https://coveralls.io/github/temken/comparxiv?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# comparxiv 

A wrapper of [**latexdiff**](https://ctan.org/pkg/latexdiff?lang=en) to compare two version of an [arXiv](https://arxiv.org) preprint with a single command.

<img src="https://user-images.githubusercontent.com/29034913/80016516-81de0b00-84d3-11ea-92b9-325fd2e219f4.png" width="750">

> **Disclaimer:** This is a beta version. Despite extensive testing, it does not work for all preprints on arXiv. Especially older preprints can cause problems.

## INSTALLATION
You can install *comparxiv* via
```
pip install comparxiv
```

or direct from source. Just run

```
git clone https://github.com/temken/comparxiv.git
cd comparxiv 
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

- python and pip
- a tex distribution with pdflatex and latexdiff (*)
- argparse (**)
- tqdm (**)
- requests (**)

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

## AUTHORS & CONTACT

The author of this script is Timon Emken.

For questions, bug reports or other suggestions please contact [emken@chalmers.se](mailto:emken@chalmers.se).


## LICENSE

This project is licensed under the MIT License - see the LICENSE file.

## ACKNOWLEDGEMENTS

I am grateful for [this useful tutorial](https://python-packaging.readthedocs.io/en/latest/index.html) by Scott Torborg about python packaging.
