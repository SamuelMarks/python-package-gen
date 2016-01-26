from os import path, walk, makedirs, listdir, rmdir
from functools import partial
from shutil import copyfile, move
from fileinput import input as fileinput
from pip import __file__ as pip_loc
from utils import OTemplate


class Scaffold(object):
    def __init__(self, cmd_args):
        cmd_args['package_name'] = cmd_args['name'].replace('-', '_')
        cmd_args['output_directory'] = path.join(cmd_args['output_directory'], cmd_args['package_name'])

        tuple(setattr(self, k, v) for k, v in cmd_args.iteritems())  # Yay: Ruby!
        self.cmd_args = cmd_args

        self.tree = self.gen_tree()

    def gen_tree(self):
        """
        :returns ((src_dir, dest_dir))
        """
        root_join = partial(path.join, self.output_directory)

        _data_conf_dir = partial(path.join, path.join(path.dirname(path.dirname(pip_loc)),
                                                      'python_package_gen', 'templates', 'config'))
        _data_tpl_dir = partial(path.join, path.join(path.dirname(path.dirname(pip_loc)),
                                                     'python_package_gen', 'templates'))

        listfiles = lambda dir_join: filter(
                lambda p: path.splitext(p)[1] not in frozenset(('.pyc', '.pyd', '.so', '.pyo')) and
                          path.isfile(dir_join(p)) and path.isfile(dir_join(p)),
                listdir(dir_join()))
        return (
            tuple((_data_tpl_dir(f), root_join(f) if f == '__init__.py' else path.join(path.dirname(root_join()), f))
                  for f in listfiles(_data_tpl_dir)) +
            tuple((_data_conf_dir(f), path.join(path.dirname(root_join()), f))
                  for f in listfiles(_data_conf_dir)))

    def create_files_and_folders(self):
        print 'Output directory: {!r}'.format(path.dirname(self.output_directory))

        if path.isdir(self.output_directory):
            if next(walk('.')) != ('.', [], []) and not (lambda _input: _input.lower() in ('true', 't'))(
                    raw_input('This output_directory has files in it. Write anyway?: [False]')):
                raise IOError('Path non-empty')
        else:
            makedirs(self.output_directory)

        for src, dst in self.tree:
            print 'Writing to: {relative_filepath!r}...'.format(
                    relative_filepath=dst[len(self.output_directory) - len(self.package_name):])
            with open(src, 'rt') as f_src, open(dst, 'wt') as f_dst:
                f_dst.write(OTemplate(f_src.read()).substitute(**self.cmd_args))

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

        new_setup_py = ''.join(
                [line for line in fileinput(path.join(path.dirname(self.output_directory), 'setup.py'))
                 if 'packages=' not in line]).replace('        package_dir={package_name: package_name}',
                                                      '        py_modules=[{!r}]'.format(self.package_name))
        with open(path.join(path.dirname(self.output_directory), 'setup.py'), 'wt') as f:
            f.write(new_setup_py)
