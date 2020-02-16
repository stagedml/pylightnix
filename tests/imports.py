from os import makedirs, replace, listdir, stat, chmod, system
from stat import S_IEXEC, S_IWRITE, S_IREAD
from os.path import (basename, join, isfile, isdir, islink, relpath, abspath,
                     dirname )
from shutil import rmtree
from tempfile import gettempdir

from hypothesis import given, assume, example, note, settings, event
from hypothesis.strategies import ( text, decimals, integers, characters,
                                    from_regex, dictionaries, one_of, lists,
                                    recursive, none, booleans, floats,
                                    composite, binary )
from string import printable
from distutils.spawn import find_executable

from subprocess import Popen, run, PIPE

from re import compile as re_compile

from typing import Any, List, Optional, Callable
from contextlib import contextmanager

from tempfile import TemporaryDirectory

from time import strftime, strptime, gmtime
from calendar import timegm

from random import randint

from time import sleep

def get_executable(name:str, not_found_message:str)->str:
  e=find_executable(name)
  assert e is not None, not_found_message
  return e

# from pylightnix import (
#     Config, Model, model_outpath, model_save, store_initialize, mknode,
#     store_deps, store_deepdeps, store_gc )
# from pylightnix import ( assert_valid_ref, assert_store_initialized )

