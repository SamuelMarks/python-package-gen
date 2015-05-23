from os import path, walk, makedirs, mkdir
from functools import partial

from utils import OTemplate


class Scaffold(object):
    def __init__(self, cmd_args):
        cmd_args['package_name'] = cmd_args['name']
        cmd_args['output_directory'] = path.realpath(cmd_args['output_directory'])
        if path.basename(path.normpath(cmd_args['output_directory'])) != cmd_args['package_name']:
            cmd_args['output_directory'] = path.join(cmd_args['output_directory'], cmd_args['package_name'])

        tuple(setattr(self, k, v) for k, v in cmd_args.iteritems())  # Yay: Ruby!
        self.cmd_args = cmd_args

        self.tree = self.gen_tree()

    def gen_tree(self):
        root_join = partial(path.join, self.output_directory)
        return (
            root_join(self.package_name + '.py' if self.single_file
                      else path.join(self.package_name, '__init__.py')),
            root_join('setup.py'),
            root_join('.gitignore'),
            root_join('requirements.txt')
        )

    def create_files_and_folders(self):
        print('Outputting to output_directory:', self.output_directory)

        if path.isdir(self.output_directory):
            if next(walk('.')) != ('.', [], []) and not (lambda _input: _input.lower() in ('true', 't'))(
                    raw_input('This output_directory has files in it. Write anyway?: [False]')):
                raise IOError('Path non-empty')
        else:
            makedirs(self.output_directory)

        if not path.exists(self.tree[0]):
            mkdir(path.dirname(self.tree[0]))

        templates_join = partial(path.join, path.dirname(path.realpath(__file__)), 'templates')
        for filepath in self.tree:
            dirname, filename = path.split(filepath)
            print 'Writing to: "{filename}" within: "{dirname}"...'.format(filename=filename, dirname=dirname)
            # open(filepath, 'a+').close()  # touch
            print 'filename: ', filename, "self.package_name: ", self.package_name
            with open(filepath, 'w') as f0:
                with open(templates_join('__init__.py') if filename[:-3] == self.package_name
                          else templates_join(path.basename(filepath)), 'r') as f1:
                    f0.write(OTemplate(f1.read()).substitute(**self.cmd_args))

    def to_single_file(self):
        if not self.single_file:
            return
        raise NotImplemented()
