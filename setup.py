from setuptools import setup, find_packages
from os import path
from functools import partial
from pip import __file__ as pip_loc
from itertools import imap, ifilter
from ast import parse

if __name__ == '__main__':
    package_name = 'python_package_gen'

    templates_join = partial(path.join, path.dirname(__file__), package_name, 'templates')
    # Still experimenting with: `get_installed_distributions(local_only=True)`

    install_to = path.join(path.dirname(path.dirname(pip_loc)), package_name, 'templates')
    get_vals = lambda var0, var1: tuple(imap(lambda buf: next(imap(lambda e: e.value.s, parse(buf).body)),
                                             ifilter(lambda line: line.startswith(var0) or line.startswith(var1), f)))

    with open(path.join(package_name, '__init__.py')) as f:
        __author__, __version__ = get_vals('__version__', '__author__')

    setup(
        name=package_name,
        author=__author__,
        version=__version__,
        test_suite=package_name + '.tests',
        packages=find_packages(),
        package_dir={package_name: package_name},
        data_files=[(install_to, [
            templates_join('.gitignore'), templates_join('logging.conf'), templates_join('requirements.txt')])]
    )
