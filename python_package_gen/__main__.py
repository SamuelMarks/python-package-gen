#!/usr/bin/env python

from datetime import datetime
from os import path
from argparse import ArgumentParser, ArgumentTypeError
from tempfile import gettempdir

from __init__ import __author__
from Scaffold import Scaffold


def is_dir(dir_path):
    """
    Checks if a path is an actual directory

    :param dir_path: directory path
    :type dir_path: str

    :returns dir_path
    :rtype str
    """
    if path.exists(dir_path) and not path.isdir(dir_path):
        raise ArgumentTypeError("'{}' is not a directory".format(dir_path))
    return dir_path


def _build_parser():
    """
    Build argparse parser object

    :returns argparse parser object
    :rtype ArgumentParser
    """
    parser = ArgumentParser(description='Generate project scaffold')
    parser.add_argument('-n', '--name', help='Package name', required=True)
    parser.add_argument('-a', '--author', help='Author name [{}]'.format(__author__), default=__author__)  # :P
    parser.add_argument('-d', '--description', help='Description', default='')
    parser.add_argument('-v', '--version', help='Version number [0.0.1]', default='0.0.1')
    parser.add_argument('-t', '--tests', help='Generate unittests [True]', default=True, action='store_true')
    parser.add_argument('-o', '--output-directory', help='Directory to extract to [tempdir/ISO-time with s/:/_]',
                        default=path.join(gettempdir(), datetime.now().isoformat().replace(':', '_')), type=is_dir)
    parser.add_argument('-s', '--single-file', help='single-file project [False]',
                        default=False, action='store_true')
    parser.add_argument('-f', '--flatten',
                        help='on bad module-name, generate p-kg/p_kg,p-kg/setup.py not p-kg/p_kg/setup.py [False]',
                        default=False, action='store_true')
    return parser


if __name__ == '__main__':
    scaffold = Scaffold(dict(_build_parser().parse_args()._get_kwargs()))
    scaffold.create_files_and_folders()
    scaffold.to_single_file()
