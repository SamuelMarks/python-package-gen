#!/usr/bin/env python

from __future__ import print_function

from os import path, walk, makedirs, mkdir
from functools import partial
from string import Template
from argparse import ArgumentParser

from __init__ import __author__, __version__


class Scaffold(object):
    def __init__(self, cmd_args):
        cmd_args['package_name'] = cmd_args['name']
        cmd_args['directory'] = path.realpath(cmd_args['directory'])
        if path.basename(path.normpath(cmd_args['directory'])) != cmd_args['package_name']:
            cmd_args['directory'] = path.join(cmd_args['directory'], cmd_args['package_name'])

        self.cmd_args = cmd_args
        # tuple(setattr(self, k, v) for k, v in locals() if not k.startswith('_'))  # Yay: Ruby!
        self.tree = self.gen_tree()

    def gen_tree(self):
        root_join = partial(path.join, self.cmd_args['directory'])
        return (
            root_join(self.cmd_args['name'] + '.py' if self.cmd_args['single_file']
                      else path.join(self.cmd_args['name'], '__init__.py')),
            root_join('setup.py'),
            root_join('.gitignore'),
            root_join('requirements.txt')
        )

    def create_files_and_folders(self):
        print('Outputting to directory:', self.cmd_args['directory'])

        if path.isdir(self.cmd_args['directory']):
            if next(walk('.')) and not (lambda _input: _input.lower() in ('true', 't'))(
                    raw_input('This directory has files in it. Write anyway?: [False]')):
                raise IOError('Path non-empty')
        else:
            makedirs(self.cmd_args['directory'])

        if not self.cmd_args['single_file'] and not path.exists(self.tree[0]):
            mkdir(path.dirname(self.tree[0]))

        templates_join = partial(path.join, path.dirname(path.realpath(__file__)), 'templates')
        for filepath in self.tree:
            dirname, filename = path.split(filepath)
            print(
                'Writing to: "{filename}" within: "{dirname}"...'.format(dirname=dirname, filename=filename)
            )
            # open(filepath, 'a+').close()  # touch
            print('filename: ', filename, "self.cmd_args['name']: ", self.cmd_args['name'])
            open(filepath, 'w').write(Template(
                open(templates_join('__init__.py') if filename[:-3] == self.cmd_args['name']
                     else templates_join(path.basename(filepath)), 'r').read()
            ).substitute(**self.cmd_args))


def build_arguments():
    parser = ArgumentParser()
    parser.add_argument('-n', '--name', help='Package name', required=True)
    parser.add_argument('-a', '--author', help='Author name', default=__author__)  # :P
    parser.add_argument('-v', '--version', help='Version number', default='0.0.1')
    parser.add_argument('-d', '--directory', help='Directory to extract to')
    parser.add_argument('-s', '--single-file', help='Single file project, or package?', action='store_true')
    return parser.parse_args()


def _tmp_dir_run():
    from tempfile import gettempdir
    from time import time

    kwargs = dict(name='foo', author=__author__, version=__version__,
                  directory=path.join(gettempdir(), str(int(time()))))

    sd = Scaffold(dict(single_file=False, **kwargs))
    sd.create_files_and_folders()
    '''
    sd = Scaffold(dict(single_file=True, **kwargs))
    sd.create_files_and_folders()
    '''


if __name__ == '__main__':
    # _tmp_dir_run()
    Scaffold(dict(build_arguments()._get_kwargs())).create_files_and_folders()
