# comparXiv 
Script to compare two version of an arXiv preprint.

## INSTALLATION
You can install *comparxiv* via
```
pip install comparxiv
```

## USAGE
To compare v1 and v2 of a paper with *comparxiv*, run e.g.
```
comparxiv 1905.06348 1 2
```

After a successful run, you should find a latexdiff-generated PDF file in your folder.

For more details, simply run
```
comparxiv --help
```

## DEPENDENCIES

- argparse
- tqdm

## VERSIONS

- **v1.0** (xx/xx/2020): First version released.

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
- [ ]Reduce the amount of pdflatex/difflatex terminal output.
- [ ]Handle old arxiv numbers.
- [ ]Publish the first version.
- [ ]Compare references, identify removed/added references.
- [ ]Compare figures, identify removed/added figures.
- [ ]Extract tex comments and their changes.
- [ ]?