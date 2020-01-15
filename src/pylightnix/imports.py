""" All external dependencies are listed here """

from json import ( loads as json_loads, dumps as json_dumps, dump as json_dump, load as json_load )
from time import strftime
from errno import EEXIST
from os import (
    mkdir, makedirs, replace, listdir, rmdir, symlink, remove, environ, walk)
from os.path import (
    basename, join, isfile, isdir, islink, relpath, abspath, dirname, split )
from hashlib import sha256
from copy import deepcopy
from tempfile import mkdtemp
from shutil import rmtree
from unicodedata import normalize
from re import sub as re_sub
