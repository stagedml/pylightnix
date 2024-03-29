from logging import getLogger
logger=getLogger(__name__)
info=logger.info
warning=logger.warning

from pylightnix.imports import *
from pylightnix.types import *
from pylightnix.utils import *
from pylightnix.core import *
from pylightnix.build import *
from pylightnix.bashlike import *
from pylightnix.repl import *
from pylightnix.lens import *
from pylightnix.either import *
from pylightnix.garb import *
from pylightnix.deco import *

try:
  from pylightnix.arch import *
except ImportError as e:
  error(f"{e}; Failed to import pylightnix.arch")

try:
  from pylightnix.stages import *
except ImportError as e:
  error(f"{e}; Failed to import pylightnix.stages")

__version__: str|None
try:
  from pylightnix.version import __version__
except ImportError:
  try:
    from setuptools_scm import get_version
    from os.path import join
    __version__ = get_version(root=join('..','..'), relative_to=__file__)
  except Exception:
    warning("Pylightnix failed to determine it's version. Probably you are "
            "importing the source distribution.")
    __version__ = None
