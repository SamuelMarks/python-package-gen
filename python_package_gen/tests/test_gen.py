from __future__ import absolute_import, print_function
from argparse import Namespace, ArgumentError
from tempfile import gettempdir
from time import ctime
from unittest import TestCase, main as unittest_main
from os import path, listdir

from shutil import rmtree

from python_package_gen.Scaffold import Scaffold

try:
    from itertools import imap
except ImportError:
    imap = map

from python_package_gen.utils import it_consumes


class PackageGenTest(TestCase):
    default_files = 'logging.conf', 'README.md', '.editorconfig', '.gitignore', 'requirements.txt', 'setup.py'

    valid_mocks = (Namespace(author='Samuel Marks',
                             description='Description',
                             name='Foo',
                             output_directory=path.join(gettempdir(), str(ctime())),
                             single_file=False,
                             tests=True,
                             version='0.0.1'),)

    invalid_mocks = (Namespace(author='Samuel Marks',
                               description='Description',
                               name=None,
                               output_directory='',
                               single_file=False,
                               tests=True,
                               version='0.0.1'),)

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
            self.assertItemsEqual((cli_args.name,) + self.default_files, listdir(cli_args.output_directory))
            module_name_dir = path.join(cli_args.output_directory, cli_args.name)
            self.assertTrue(path.isdir(module_name_dir))
            self.assertItemsEqual(('__init__.py',), listdir(module_name_dir))

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