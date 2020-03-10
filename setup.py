from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='comparxiv',
      version='0.1',
      description='Compare two versions of an arXiv preprint.',
      long_description = readme(),
      keywords='arxiv preprint comparison',
      url='http://github.com/temken/comparxiv',
      author='Timon Emken',
      author_email='emken@chalmeres.se',
      license='MIT',
      packages=['comparxiv'],
      install_requires=[
          'tqdm',
      ],
      entry_points = {
        'console_scripts': ['comparxiv=comparxiv.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)