from collections import deque
from itertools import islice
from string import Template


class OTemplate(Template):
    delimiter = '_0_'
    idpattern = r'[a-z][_a-z0-9]*'


it_consumes = lambda it, n=None: deque(it, maxlen=0) if n is None else next(islice(it, n, n), None)
