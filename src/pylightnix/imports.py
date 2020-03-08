# Copyright 2020, Sergey Mironov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" All external dependencies are listed here """

from json import ( loads as json_loads, dumps as json_dumps, dump as json_dump,
    load as json_load )
from time import strftime, strptime, gmtime
from calendar import timegm
from errno import EEXIST
from os import (
    mkdir, makedirs, replace, listdir, rmdir, symlink, rename, remove, environ,
    walk, lstat, chmod, stat, readlink )
from os.path import (
    basename, join, isfile, isdir, islink, relpath, abspath, dirname, split,
    getsize )
from stat import ( S_IWRITE, S_IREAD, S_IRGRP, S_IROTH, S_IXUSR, S_IXGRP,
    S_IXOTH, ST_MODE, S_IWGRP, S_IWRITE, S_IWOTH )
from hashlib import sha256
from copy import deepcopy
from tempfile import mkdtemp
from shutil import rmtree, copyfile
from unicodedata import normalize
from re import sub as re_sub, match as re_match
from distutils.spawn import find_executable
from subprocess import Popen
from urllib.parse import urlparse
from errno import ENOTEMPTY
from threading import get_ident
from contextlib import contextmanager
from collections import OrderedDict, defaultdict
from sys import maxsize
from datetime import datetime
from fnmatch import fnmatch
