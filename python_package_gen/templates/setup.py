from setuptools import setup, find_packages

if __name__ == '__main__':
    package_name = '_0_package_name'
    setup(
        name=package_name,
        author='_0_author',
        version='_0_version',
        test_suite=package_name + '.tests',
        packages=find_packages(),
        package_dir={package_name: package_name}
    )
