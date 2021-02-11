# Copyright 2021, Sergey Mironov
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

""" Functions for moving parts of the storage to and from archives.  """

from pylightnix.imports import (Popen, dirname, basename, remove, join,
                                relpath, rename, splitext)
from pylightnix.types import (RRef, List, Dict, Path)
from pylightnix.core import (store_deepdeps, store_deepdepRrefs, rref2path)
from pylightnix.utils import (try_executable)



APACK=try_executable('apack',
                     'PYLIGHTNIX_APACK',
                     '`apack` executable not found. Please install `atool` system '
                     'pacakge or set PYLIGHTNIX_APACK env var.',
                     '`arch.pack` procedure will fail.')


def rsort(rrefs:List[RRef], deps:Dict[RRef,List[RRef]])->List[RRef]:
  assert False, "Not implemented"


def pack(roots:List[RRef], out:Path)->None:
  tmp=splitext(out)[0]+'_tmp'+splitext(out)[1]
  rrefs=store_deepdepRrefs(roots)
  try:
    remove(tmp)
  except KeyboardInterrupt:
    raise
  except Exception:
    pass
  import pylightnix.core
  store_holder=dirname(pylightnix.core.PYLIGHTNIX_STORE)
  for rref in rrefs | set(roots):
    p=Popen([APACK(), tmp, relpath(rref2path(rref), start=store_holder)],
            cwd=store_holder)
    p.wait()
  rename(tmp,out)


def unpack(file_path:Path)->None:
  assert False, "Not implemented"



