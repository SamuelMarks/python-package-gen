from __future__ import print_function
from argparse import ArgumentError
from collections import namedtuple
from fileinput import input as fileinput
from os import path, walk, makedirs, listdir, rmdir

try:
    input = raw_input
except NameError:
    pass

from shutil import move

from python_package_gen.utils import it_consumes, templates_pkg_join, listfiles, change_to_module_name

from utils import OTemplate

Tree = namedtuple('Tree', 'pkg_dir fnames to_subdir')


class Scaffold(object):
    def __init__(self, cmd_args):
        for arg in ('name', 'output_directory'):
            if not cmd_args[arg]:
                raise ArgumentError(
                    namedtuple('Argument', 'dest option_strings metavar')('{!r}'.format(arg), None, None), 'required'
                )

        cmd_args['package_name'] = change_to_module_name(cmd_args['name'])
        cmd_args['output_directory'] = path.join(cmd_args['output_directory'], cmd_args['package_name'])
        if cmd_args['package_name'] != cmd_args['name']:
            print('Module name invalid. {!r} renamed to: {!r}'.format(path.join(cmd_args['output_directory'], cmd_args['name']),
                                                 cmd_args['output_directory']))

        it_consumes(setattr(self, k, v) for k, v in cmd_args.iteritems())  # Yay: Ruby!
        self.cmd_args = cmd_args

        self.trees = self.gen_tree()

    def gen_tree(self):
        """
        :returns (Tree, Tree, Tree)
        """

        return (Tree(templates_pkg_join('config'), listdir(templates_pkg_join('config')), tuple()),
                Tree(templates_pkg_join('config', '_data'), listdir(templates_pkg_join('config', '_data')),
                     (self.package_name, '_data')),
                Tree(templates_pkg_join(), listfiles(templates_pkg_join), (self.package_name,))
                )

    def create_files_and_folders(self):
        print('Output directory: {!r}'.format(path.dirname(self.output_directory)))
        print('self.tree =', self.trees)

        if path.isdir(self.output_directory):
            if next(walk('.')) != ('.', [], []) and not (
                lambda _input: _input.lower() in ('true', 't')
            )(input('This output_directory has files in it. Write anyway?: [False]')):
                raise IOError('Path non-empty')
        else:
            makedirs(self.output_directory)

        for tree in self.trees:
            for fname in tree.fnames:
                to_path = path.join(self.output_directory, *tree.to_subdir)
                if tree.to_subdir and not path.exists(to_path):
                    makedirs(to_path)
                to_loc = path.join(to_path, fname)
                pkg_fname = path.join(tree.pkg_dir, fname)
                if not path.isfile(pkg_fname):
                    continue
                if not to_loc.endswith('setup.py'):
                    print('Writing to: {relative_filepath!r}...'.format(relative_filepath=to_loc))
                with open(pkg_fname, 'rt') as f_src, open(to_loc, 'wt') as f_dst:
                    f_dst.write(OTemplate(f_src.read()).substitute(**self.cmd_args))
        setup_py = path.join(self.output_directory, self.package_name, 'setup.py')
        to_setup_py = path.join(path.dirname(path.dirname(setup_py)), 'setup.py')
        print('Writing to: {relative_filepath!r}...'.format(relative_filepath=to_setup_py))
        move(setup_py, to_setup_py)

    def to_single_file(self):
        if not self.single_file:
            return

        assert len(listdir(self.output_directory)) == 1, "Can't convert to single file project with" \
                                                         "more than __init__.py in module directory"
        src_init_file = path.join(self.output_directory, '__init__.py')
        move(src_init_file, path.dirname(self.output_directory))
        rmdir(self.output_directory)
        move(path.join(path.dirname(self.output_directory), '__init__.py'),
             path.join(path.dirname(self.output_directory), self.package_name + '.py'))

        new_setup_py = ''.join(line for line in fileinput(path.join(path.dirname(self.output_directory), 'setup.py'))
                               if 'packages=' not in line).replace(
            '        package_dir={package_name: package_name}',
            '        py_modules=[{!r}]'.format(self.package_name))
        with open(path.join(path.dirname(self.output_directory), 'setup.py'), 'wt') as f:
            f.write(new_setup_py)
