from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='comparxiv',
      version='0.1.1',
      description='Compare two versions of an arXiv preprint with latexdiff.',
      long_description = readme(),
      long_description_content_type='text/markdown',
      keywords='arxiv preprint comparison latexdiff latex',
      url='http://github.com/temken/comparxiv',
      author='Timon Emken',
      author_email='emken@chalmers.se',
      license='MIT',
      packages=['comparxiv'],
      install_requires=[
          'tqdm',
          'argparse',
          'requests'
      ],
      entry_points = {
        'console_scripts': ['comparxiv=comparxiv.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)