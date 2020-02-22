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

from pylightnix.types import ( Iterable, List, Union, Optional, DRef, RRef )
from pylightnix.imports import ( isfile, isdir, listdir, join, rmtree, environ,
    Popen )
from pylightnix.core import ( store_dref2path, rref2path, isrref, isdref )
from pylightnix.utils import ( dirchmod )


def lsdref_(r:DRef)->Iterable[str]:
  p=store_dref2path(r)
  for d in listdir(p):
    p2=join(d,p)
    if isdir(p2):
      yield d

def lsrref_(r:RRef, fn:List[str]=[])->Iterable[str]:
  p=join(rref2path(r),*fn)
  for d in listdir(p):
    yield d

def lsrref(r:RRef, fn:List[str]=[])->List[str]:
  return list(lsrref_(r,fn))

def lsref(r:Union[RRef,DRef])->List[str]:
  """ List the contents of `r`. For [DRefs](#pylightnix.types.DRef), return
  realization hashes. For [RRefs](#pylightnix.types.RRef), list artifact files. """
  if isrref(r) and isinstance(r,RRef):
    return list(lsrref(r))
  elif isdref(r) and isinstance(r,DRef):
    return list(lsdref_(r))
  else:
    assert False, f"Invalid reference {r}"

def catrref_(r:RRef, fn:List[str])->Iterable[str]:
  with open(join(rref2path(r),*fn),'r') as f:
    for l in f.readlines():
      yield l

def catref(r:RRef, fn:List[str])->List[str]:
  """ Return the contents of r's artifact file `fn` line by line. """
  if isrref(r) and isinstance(r,RRef):
    return list(catrref_(r,fn))
  else:
    assert False, 'not implemented'

def rmrref(r:RRef)->None:
  dirchmod(rref2path(r),'rw')
  rmtree(rref2path(r))

def rmdref(r:DRef)->None:
  dirchmod(store_dref2path(r),'rw')
  rmtree(store_dref2path(r))

def rmref(r:Union[RRef,DRef])->None:
  """ Forcebly remove a reference from the storage. Removing
  [DRefs](#pylightnix.types.DRef) also removes all their realizations.

  Currently Pylightnix makes no attempts to synchronize an access to the
  storage. In scenarious involving parallelization, users are expected to take
  care of possible race conditions.
  """
  if isrref(r) and isinstance(r,RRef):
    rmrref(r)
  elif isdref(r) and isinstance(r,DRef):
    rmdref(r)
  else:
    assert False, f"Invalid reference {r}"

def shellref(r:Union[RRef,DRef])->None:
  """ Open the directory corresponding to `r` in Unix Shell for inspection. The
  path to shell executable is read from the `SHELL` environment variable,
  defaulting to `/bin/sh`.  """
  cwd:str
  if isrref(r) and isinstance(r,RRef):
    cwd=rref2path(r)
  elif isdref(r) and isinstance(r,DRef):
    cwd=store_dref2path(r)
  else:
    assert False, f"Expecting values of type `RRef` or `DRef`, got {r}"
  Popen([environ.get('SHELL','/bin/sh')], shell=False, cwd=cwd).wait()


