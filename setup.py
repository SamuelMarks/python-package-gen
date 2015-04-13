from setuptools import setup, find_packages
from os import path
from functools import partial
from pip import __file__ as pip_loc

if __name__ == '__main__':
    package_name = 'python_package_gen'

    templates_join = partial(path.join, path.dirname(__file__), package_name, 'templates')
    # Still experimenting with: `get_installed_distributions(local_only=True)`

    install_to = path.join(path.dirname(path.dirname(pip_loc)), package_name, 'templates')

    setup(
        name=package_name,
        author='Samuel Marks',
        version='0.3.1',
        test_suite=package_name + '.tests',
        packages=find_packages(),
        package_dir={package_name: package_name},
        data_files=[(install_to, [
            templates_join('.gitignore'), templates_join('logging.conf'), templates_join('requirements.txt')])]
    )
