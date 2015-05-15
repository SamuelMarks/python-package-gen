#!/usr/bin/env python

from os import path
from argparse import ArgumentParser
from tempfile import gettempdir
from time import time

from __init__ import __author__
from Scaffold import Scaffold


def _build_parser():
    parser = ArgumentParser(description='Generate project scaffold')
    parser.add_argument('-n', '--name', help='Package name', required=True)
    parser.add_argument('-a', '--author', help='Author name [{}]'.format(__author__), default=__author__)  # :P
    parser.add_argument('-d', '--description', help='Description', default='')
    parser.add_argument('-v', '--version', help='Version number [0.0.1]', default='0.0.1')
    parser.add_argument('-t', '--tests', help='Generate unittests [True]', default=True, action='store_true')
    parser.add_argument('-o', '--output-directory', help='Directory to extract to [tempdir/time()]',
                        default=path.join(gettempdir(), str(int(time()))))
    parser.add_argument('-s', '--single-file', help='single-file project [False]',
                        default=False, action='store_true')
    return parser


if __name__ == '__main__':
    scaffold = Scaffold(dict(_build_parser().parse_args()._get_kwargs()))
    scaffold.create_files_and_folders()
    scaffold.to_single_file()