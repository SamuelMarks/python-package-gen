# -*- coding: utf-8 -*-

from collections import deque
from distutils.sysconfig import get_python_lib
from functools import partial
from itertools import islice
from os import listdir, environ, path
from string import Template

try:
    from platform import linux_distribution  # Python 3.5 deprecated this
except ImportError:
    try:
        from distro import linux_distribution  # Recommended this instead
    except ImportError:
        linux_distribution = lambda: (None,) * 3


class OTemplate(Template):
    delimiter = '_0_'
    idpattern = r'[a-z][_a-z0-9]*'


it_consumes = lambda it, n=None: deque(it, maxlen=0) if n is None else next(islice(it, n, n), None)

listfiles = lambda dir_join: filter(
    lambda p: path.isfile(dir_join(p)) and path.splitext(p)[1] not in frozenset(
        ('.pyc', '.pyd', '.so', '.pyo')),
    listdir(dir_join()))

templates_pkg_join = partial(path.join, path.join(get_python_lib(
    plat_specific=True,
    prefix='/usr/local' if not environ.get('VIRTUAL_ENV') and linux_distribution()[0] == 'Ubuntu'
    else environ.get('VIRTUAL_ENV')),
    'python_package_gen', 'templates'))

to_module_name = lambda s: s.replace('-', '_').lower()
