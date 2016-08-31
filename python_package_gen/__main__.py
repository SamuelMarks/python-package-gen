#!/usr/bin/env python

from os import path
from argparse import ArgumentParser, ArgumentTypeError
from tempfile import gettempdir
from time import ctime

from __init__ import __author__
from Scaffold import Scaffold


def is_dir(dirname):
    """Checks if a path is an actual directory"""
    if not path.isdir(dirname):
        raise ArgumentTypeError("{0} is not a directory".format(dirname))
    return dirname


def _build_parser():
    parser = ArgumentParser(description='Generate project scaffold')
    parser.add_argument('-n', '--name', help='Package name', required=True)
    parser.add_argument('-a', '--author', help='Author name [{}]'.format(__author__), default=__author__)  # :P
    parser.add_argument('-d', '--description', help='Description', default='')
    parser.add_argument('-v', '--version', help='Version number [0.0.1]', default='0.0.1')
    parser.add_argument('-t', '--tests', help='Generate unittests [True]', default=True, action='store_true')
    parser.add_argument('-o', '--output-directory', help='Directory to extract to [tempdir/ctime()]',
                        default=path.join(gettempdir(), str(ctime())), type=is_dir)
    parser.add_argument('-s', '--single-file', help='single-file project [False]',
                        default=False, action='store_true')
    return parser


if __name__ == '__main__':
    scaffold = Scaffold(dict(_build_parser().parse_args()._get_kwargs()))
    scaffold.create_files_and_folders()
    scaffold.to_single_file()
