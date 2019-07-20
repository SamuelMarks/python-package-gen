python package gen
==================
![Python version range](https://img.shields.io/badge/python-2.7%E2%80%933.6+-blue.svg)

Simple code-generator using only stdlib. Supports two modes, single file and folder.

Both provide tests (unittest) and support for:

    python setup.py install
    python setup.py test

## Install

    pip install https://github.com/SamuelMarks/python-package-gen/zipball/master#egg=python_package_gen

## Example run

    python -m python_package_gen -n bar -o bar

### Generates

    $ tree -a bar --charset=ascii
    bar
    |-- .editorconfig
    |-- .gitignore
    |-- README.md
    |-- bar
    |   |-- __init__.py
    |   `-- _data
    |       `-- logging.yml
    |-- requirements.txt
    `-- setup.py
    
    2 directories, 7 files

## Usage

    $ python -m python_package_gen -h
    usage: __main__.py [-h] -n NAME [-a AUTHOR] [-d DESCRIPTION] [-v VERSION] [-t]
                       [-o OUTPUT_DIRECTORY] [-s] [-f]
    
    Generate project scaffold
    
    optional arguments:
      -h, --help            show this help message and exit
      -n NAME, --name NAME  Package name
      -a AUTHOR, --author AUTHOR
                            Author name [Samuel Marks]
      -d DESCRIPTION, --description DESCRIPTION
                            Description
      -v VERSION, --version VERSION
                            Version number [0.0.1]
      -t, --tests           Generate unittests [True]
      -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                            Directory to extract to [tempdir/ISO-time with s/:/_]
      -s, --single-file     single-file project [False]
      -f, --flatten         on bad module-name, generate p-kg/p_kg,p-kg/setup.py
                            not p-kg/p_kg/setup.py [False]
