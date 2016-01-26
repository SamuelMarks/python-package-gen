python package gen
==================

Simple code-generator using only stdlib. Supports two modes, single file and folder.

Both provide tests (unittest) and support for:

    python setup.py install
    python setup.py test

## Install

    pip install git+https://github.com/SamuelMarks/python-package-gen#egg=python_package_gen

## Example run

    python -m python_package_gen -n bar -o bar

### Generates

    $ tree -a bar --charset=ascii
    bar
    |-- bar
    |   `-- __init__.py
    |-- .editorconfig
    |-- .gitignore
    |-- __init__.py
    |-- logging.conf
    |-- README.md
    |-- requirements.txt
    `-- setup.py
    
    1 directory, 8 files

## Usage

    $ python -m python_package_gen -h
    usage: [-h] -n NAME [-a AUTHOR] [-d DESCRIPTION] [-v VERSION] [-t]
           [-o OUTPUT_DIRECTORY] [-s]
    
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
                            Directory to extract to [tempdir/time()]
      -s, --single-file     single-file project [False]
