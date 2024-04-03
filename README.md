python package gen
==================
[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech)
![Python version range](https://img.shields.io/badge/python-2.7%20|%203.5%20|%203.6%20|%203.7%20|%203.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12%20|%203.13-blue.svg)
[![License](https://img.shields.io/badge/license-Apache--2.0%20OR%20MIT%20OR%20CC0--1.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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

## License

Licensed under any of:

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)
- CC0 license ([LICENSE-CC0](LICENSE-CC0) or <https://creativecommons.org/publicdomain/zero/1.0/legalcode>)

at your option.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
licensed as above, without any additional terms or conditions.
