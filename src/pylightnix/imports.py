""" All external dependencies are listed here """

from json import ( loads as json_loads, dumps as json_dumps, dump as json_dump, load as json_load )
from time import strftime, strptime, gmtime
from calendar import timegm
from errno import EEXIST
from os import (
    mkdir, makedirs, replace, listdir, rmdir, symlink, rename, remove, environ, walk)
from os.path import (
    basename, join, isfile, isdir, islink, relpath, abspath, dirname, split )
from hashlib import sha256
from copy import deepcopy
from tempfile import mkdtemp
from shutil import rmtree
from unicodedata import normalize
from re import sub as re_sub, match as re_match
from distutils.spawn import find_executable
from subprocess import Popen
from urllib.parse import urlparse
from errno import ENOTEMPTY
from threading import get_ident
from contextlib import contextmanager
from collections import OrderedDict

