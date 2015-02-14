from setuptools import setup, find_packages
from python_package_gen import __version__, __author__

if __name__ == '__main__':
    package_name = 'python_package_gen'
    setup(
        name=package_name,
        author=__author__,
        version=__version__,
        test_suite=package_name + '.tests',
        packages=find_packages(),
        package_dir={package_name: package_name}
    )
