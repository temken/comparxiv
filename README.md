# comparXiv 
A wrapper of [**latexdiff**](https://ctan.org/pkg/latexdiff?lang=en) to compare two version of an [arXiv](https://arxiv.org) preprint with a single command.


> This is a beta version. Despite extensive testing, it does not work for all preprints on arXiv. Especially older preprints can be problematic.

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

A successful run will generate a pdf and open it.

For more details about e.g. default arguments and options, simply run
```
comparxiv --help
```

## DEPENDENCIES

- tex distribution
- latexdiff
- argparse
- tqdm

## VERSIONS

- **v0.1.0** (xx/04/2020): First version released.

## AUTHORS & CONTACT

The author of this script is Timon Emken.

For questions, bug reports or other suggestions please contact [emken@chalmers.se](mailto:emken@chalmers.se).


## LICENCE

This project is licensed under the MIT License - see the LICENSE file.

## ACKNOWLEDGEMENTS

I am grateful for [this useful tutorial](https://python-packaging.readthedocs.io/en/latest/index.html) by Scott Torborg about python packaging.

## TO-DO

- [x]Handle multiple tex files and identify the master file accurately.
- [x]Make it a proper, installable executable script, that works from any directory.
- [x]Progress bar with tqdm.
- [x]Handle the inline arguments properly, especially when they are invalid.
- [x]Option to deactivate the removal of the temp files (ideally with an option flag).
- [x]Reduce the amount of pdflatex/latexdiff terminal output.
- [x]Handle old arxiv numbers.
- [ ]Set up tests.
- [ ]Publish the first version.
- [ ]Compare figures, identify removed/added figures.