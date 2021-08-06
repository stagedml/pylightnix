from pylightnix.imports import *
from pylightnix.types import *
from pylightnix.utils import *
from pylightnix.core import *
from pylightnix.build import *
from pylightnix.stages import *
from pylightnix.inplace import *
from pylightnix.bashlike import *
from pylightnix.repl import *
from pylightnix.lens import *
from pylightnix.either import *
# from pylightnix.groups import *
# from pylightnix.matchers import *

try:
  from pylightnix.version import __version__
except ImportError:
  from setuptools_scm import get_version
  from os.path import join
  __version__ = get_version(root=join('..','..'), relative_to=__file__)
