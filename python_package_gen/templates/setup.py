from setuptools import setup, find_packages
from _0_package_name import __version__, __author__

if __name__ == '__main__':
    package_name = '_0_package_name'
    setup(
        name=package_name,
        author=__author__,
        version=__version__,
        test_suite=package_name + '.tests',
        packages=find_packages(),
        package_dir={package_name: package_name}
    )
