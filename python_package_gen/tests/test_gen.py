#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from argparse import Namespace, ArgumentError
from datetime import datetime
from functools import partial
from os import path, listdir
from shutil import rmtree
from tempfile import gettempdir
from unittest import TestCase, main as unittest_main

from python_package_gen.Scaffold import Scaffold

try:
    from itertools import imap, ifilter
except ImportError:
    imap = map
    ifilter = filter

from python_package_gen.utils import it_consumes, listfiles, templates_pkg_join


class PackageGenTest(TestCase):
    default_root_files = '.editorconfig', '.gitignore', 'README.md', 'requirements.txt', 'setup.py'
    default_data_files = sorted(listfiles(partial(path.join, templates_pkg_join('config', '_data'))))

    valid_mocks = (Namespace(author='Samuel Marks',
                             description='Description',
                             name='Foo',
                             output_directory=path.join(gettempdir(), datetime.now().isoformat()).replace(':', '_'),
                             single_file=False,
                             tests=True,
                             version='0.0.1',
                             flatten=False),)

    invalid_mocks = (Namespace(author='Samuel Marks',
                               description='Description',
                               name=None,
                               output_directory='',
                               single_file=False,
                               tests=True,
                               version='0.0.1',
                               flatten=False),)

    @classmethod
    def tearDownClass(cls):
        (lambda f: it_consumes(imap(f, cls.valid_mocks)) and it_consumes(imap(f, cls.invalid_mocks)))(
            lambda m: m.output_directory and path.isdir(m.output_directory) and rmtree(m.output_directory)
        )

    def test_valid_mocks(self):
        def run_cli_args(cli_args):
            self.assertFalse(path.isdir(cli_args.output_directory))

            scaffold = Scaffold(dict(cli_args._get_kwargs()))
            scaffold.create_files_and_folders()
            scaffold.to_single_file()

            self.assertTrue(path.isdir(cli_args.output_directory))
            pkg_dir = partial(path.join, cli_args.output_directory, scaffold.cmd_args['package_name'])
            self.assertTrue(path.isdir(pkg_dir()))
            self.assertEqual(self.default_root_files, sorted(listfiles(pkg_dir)))

            _data_dir = partial(path.join, pkg_dir(), scaffold.cmd_args['package_name'], '_data')
            self.assertTrue(path.isdir(_data_dir()))
            self.assertEqual(self.default_data_files, sorted(listdir(_data_dir())))

            module_name_dir = partial(path.join, cli_args.output_directory, scaffold.cmd_args['package_name'],
                                      scaffold.cmd_args['package_name'])
            self.assertTrue(path.isdir(module_name_dir()))
            self.assertEqual(('__init__.py',), tuple(sorted(listfiles(module_name_dir))))

            return scaffold

        it_consumes(imap(run_cli_args, self.valid_mocks))

    def test_invalid_mocks(self):
        def run_cli_args(cli_args):
            self.assertFalse(path.isdir(cli_args.output_directory))

            self.assertRaises(ArgumentError, lambda: Scaffold(dict(cli_args._get_kwargs())))

            self.assertFalse(path.isdir(cli_args.output_directory))

        it_consumes(imap(run_cli_args, self.invalid_mocks))


if __name__ == '__main__':
    unittest_main()
