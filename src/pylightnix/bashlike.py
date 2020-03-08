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
    Dict, Tuple, Path, Build, Stage )
from pylightnix.imports import ( isfile, isdir, listdir, join, rmtree, environ,
    Popen, rename, getsize, fnmatch )
from pylightnix.core import ( store_dref2path, rref2path, isrref, isdref,
    store_drefs, store_rrefs_, store_config, config_name, store_buildtime,
    instantiate, store_cfgpath, rref2dref )
from pylightnix.utils import ( dirchmod, dirrm, dirsize, parsetime, timestring )


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

def shell(r:Union[Build,RRef,DRef,Path,str,None]=None)->None:
  """ Open the Unix Shell in the directory associated with the argument passed.
  Path to the shell executable is read from the `SHELL` environment variable,
  defaulting to `/bin/sh`. If `r` is None, open the shell in the root of the
  Pylightnix storage.

  The function is expected to be run in REPL Python shells like IPython.
  """
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

def shellref(r:Union[RRef,DRef,None]=None)->None:
  """ Alias for [shell](#pylightnix.bashlike.shell). Deprecated. """
  shell(r)


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


def find(name:Optional[Union[Stage,str]]=None, newer:Optional[float]=None)->List[RRef]:
  """ Return [RRefs](#pylightnix.types.RRef) found in Pylightnix sotrage which
  match all of the criteria provided. Without arguments return all RRefs.

  Arguments:
  - `name:Optional[Union[Stage,str]]=None` match RRefs which have `name` in
    their name.  Matching is done by `fnmatch` Python function which supports
    shell-like glob expressions with '*' and '?' symbols. If name is a
    [Stage](#pylightnix.types.Stage) then it is instantiated and it's name is
    taken.
  - `newer:Optional[float]=None` match RRefs which are newer than this number of
    seconds starting from the UNIX Epoch. Zero and negative numbers count
    backward from the current time.
  """
  rrefs=[]
  name_=None
  if name is not None:
    if isinstance(name,str):
      name_=name
    else:
      stage=name
      name_=config_name(store_config(instantiate(stage).dref))
  for dref in store_drefs():
    for rref in store_rrefs_(dref):
      if name_ is not None:
        if not fnmatch(config_name(store_config(rref)),name_):
          continue
      if newer is not None:
        if newer<=0:
          reftime=parsetime(timestring())
        else:
          reftime=newer
        btstr=store_buildtime(rref)
        btime=parsetime(btstr) if btstr is not None else None
        if btime is not None and reftime is not None:
          if btime < reftime:
            continue
      rrefs.append(rref)
  return rrefs

def diff(stageA:Union[RRef,DRef,Stage], stageB:Union[RRef,DRef,Stage])->None:
  """ Run system's `diff` utility to print the difference between configs of 2
  stages passed. """
  def _cfgpathof(s)->Path:
    if isrref(s):
      return store_cfgpath(rref2dref(RRef(s)))
    elif isdref(s):
      return store_cfgpath(DRef(s))
    else:
      return store_cfgpath(instantiate(s).dref)

  Popen(['diff', '-u', _cfgpathof(stageA), _cfgpathof(stageB)], shell=False, cwd='/').wait()



