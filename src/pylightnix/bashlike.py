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

""" Simple functions imitating unix shell tools.  """

from pylightnix.types import ( Iterable, List, Union, Optional, DRef, RRef,
    Dict, Tuple, Path, Build )
from pylightnix.imports import ( isfile, isdir, listdir, join, rmtree, environ,
    Popen, rename, getsize )
from pylightnix.core import ( store_dref2path, rref2path, isrref, isdref,
    store_drefs, store_rrefs_ )
from pylightnix.utils import ( dirchmod, dirrm, dirsize )


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
  if isrref(r):
    return list(lsrref(RRef(r)))
  elif isdref(r):
    return list(lsdref_(DRef(r)))
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

def rmref(r:Union[RRef,DRef])->None:
  """ Forcebly remove a reference from the storage. Removing
  [DRefs](#pylightnix.types.DRef) also removes all their realizations.

  Currently Pylightnix makes no attempts to synchronize an access to the
  storage. In scenarious involving parallelization, users are expected to take
  care of possible race conditions.
  """
  if isrref(r):
    dirrm(rref2path(RRef(r)))
  elif isdref(r):
    dirrm(store_dref2path(DRef(r)))
  else:
    assert False, f"Invalid reference {r}"

def shellref(r:Union[RRef,DRef,None]=None)->None:
  """ Alias for [shell](#pylightnix.bashlike.shell). Deprecated. """
  shell(r)

def shell(r:Union[Build,RRef,DRef,Path,str,None]=None)->None:
  """ Open the directory corresponding to `r` in Unix Shell for inspection. The
  path to shell executable is read from the `SHELL` environment variable,
  defaulting to `/bin/sh`. If `r` is None, open the shell in the root of the
  Pylightnix storage. """
  cwd:str
  if r is None:
    import pylightnix.core
    cwd=pylightnix.core.PYLIGHTNIX_STORE
  elif isrref(r):
    cwd=rref2path(RRef(r))
  elif isdref(r):
    cwd=store_dref2path(DRef(r))
  elif isinstance(r,Build):
    assert len(r.outpaths)>0, (
      "Shell function requires at least one build output path to be defined" )
    cwd=r.outpaths[0]
  elif isdir(r):
    cwd=str(r)
  else:
    assert False, f"Expecting `RRef`, `DRef`, a directory path (either a string or a `Path`), or None, got {r}"
  Popen([environ.get('SHELL','/bin/sh')], shell=False, cwd=cwd).wait()


def du()->Dict[DRef,Tuple[int,Dict[RRef,int]]]:
  """ Calculates the disk usage, in bytes. For every derivation, return it's
  total disk usage and disk usages per realizations. Note, that total disk usage
  of a derivation is slightly bigger than sum of it's realization's usages."""
  res={}
  for dref in store_drefs():
    rref_res={}
    dref_total=0
    for rref in store_rrefs_(dref):
      usage=dirsize(rref2path(rref))
      rref_res[rref]=usage
      dref_total+=usage
    dref_total+=getsize(join(store_dref2path(dref),'config.json'))
    res[dref]=(dref_total,rref_res)
  return res




