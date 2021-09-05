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

from pylightnix.types import (Iterable, List, Union, Optional, DRef, RRef,
    Dict, Tuple, Path, Stage, StorageSettings, RefPath)
from pylightnix.imports import (isfile, isdir, listdir, join, rmtree, environ,
    Popen, rename, getsize, fnmatch, dirname, relpath)
from pylightnix.core import (dref2path, rref2path, isrref, isdref,
    alldrefs, drefrrefs, drefcfg_, cfgname,
    instantiate, drefcfgpath, rref2dref, fsstorage)
from pylightnix.utils import (dirchmod, dirrm, dirsize, parsetime, timestring,
                              forcelink, isrefpath)

from pylightnix.build import (Build, rrefbstart)

def lsdref_(r:DRef, S=None)->Iterable[str]:
  p=dref2path(r,S=S)
  for d in listdir(p):
    p2=join(d,p)
    if isdir(p2):
      yield d

def lsrref_(r:RRef, fn:List[str]=[], S=None)->Iterable[str]:
  p=join(rref2path(r,S=S),*fn)
  for d in listdir(p):
    yield d

def lsrref(r:RRef, fn:List[str]=[], S=None)->List[str]:
  return list(lsrref_(r,fn,S=S))

def lsref(r:Union[RRef,DRef], S=None)->List[str]:
  """ List the contents of `r`. For [DRefs](#pylightnix.types.DRef), return
  realization hashes. For [RRefs](#pylightnix.types.RRef), list artifact files.
  """
  if isrref(r):
    return list(lsrref(RRef(r),S=S))
  elif isdref(r):
    return list(lsdref_(DRef(r),S=S))
  else:
    assert False, f"Invalid reference {r}"

def catrref_(r:RRef, fn:List[str], S=None)->Iterable[str]:
  with open(join(rref2path(r,S=S),*fn),'r') as f:
    for l in f.readlines():
      yield l

def catref(r:Union[RRef,RefPath,Path], fn:List[str]=[], S=None)->List[str]:
  """ Return the contents of r's artifact line by line. `fn` is a list of
  folders, relative to rref's root. """
  if isinstance(r,str) and isfile(r):
    return open(r,'r').readlines()
  elif isrref(r) and isinstance(r,RRef):
    return list(catrref_(r,fn,S=S))
  else:
    assert False, 'not implemented'

def rmref(r:Union[RRef,DRef], S=None)->None:
  """ Forcebly remove a reference from the storage. Removing
  [DRefs](#pylightnix.types.DRef) also removes all their realizations.

  Currently Pylightnix makes no attempts to synchronize an access to the
  storage. In scenarious involving parallelization, users are expected to take
  care of possible race conditions.
  """
  if isrref(r):
    dirrm(rref2path(RRef(r),S=S), ignore_not_found=False)
  elif isdref(r):
    dirrm(dref2path(DRef(r),S=S), ignore_not_found=False)
  else:
    assert False, f"Invalid reference {r}"

def shell(r:Union[RRef,DRef,Build,Path,str,None]=None, S=None)->None:
  """ Open the Unix Shell in the directory associated with the argument passed.
  Path to the shell executable is read from the `SHELL` environment variable,
  defaulting to `/bin/sh`. If `r` is None, open the shell in the root of the
  Pylightnix storage.

  The function is expected to be run in REPL Python shells like IPython.
  """
  cwd:str
  if r is None:
    cwd=fsstorage(S)
  elif isrref(r):
    cwd=rref2path(RRef(r),S=S)
  elif isdref(r):
    cwd=dref2path(DRef(r), S=S)
  elif isinstance(r,Build):
    assert r.outpaths is not None and len(r.outpaths.val)>0, (
      "Shell function requires at least one build output path to be defined" )
    cwd=r.outpaths.val[0]
  elif isdir(r):
    cwd=str(r)
  elif isfile(r):
    cwd=dirname(str(r))
  else:
    assert False, (
      f"Expecting `RRef`, `DRef`, a directory or file path (either a string or "
      f"a `Path`), or None. Got {r}")
  Popen([environ.get('SHELL','/bin/sh')], shell=False, cwd=cwd).wait()


def shellref(r:Union[RRef,DRef,None]=None, S=None)->None:
  """ Alias for [shell](#pylightnix.bashlike.shell). Deprecated. """
  shell(r, S=S)


def du(S=None)->Dict[DRef,Tuple[int,Dict[RRef,int]]]:
  """ Calculates the disk usage, in bytes. For every derivation, return it's
  total disk usage and disk usages per realizations. Note, that total disk usage
  of a derivation is slightly bigger than sum of it's realization's usages."""
  res={}
  for dref in alldrefs(S=S):
    rref_res={}
    dref_total=0
    for rref in drefrrefs(dref, S=S):
      usage=dirsize(rref2path(rref, S=S))
      rref_res[rref]=usage
      dref_total+=usage
    dref_total+=getsize(join(dref2path(dref,S=S),'config.json'))
    res[dref]=(dref_total,rref_res)
  return res


def find(name:Optional[Union[Stage,str]]=None,
         newer:Optional[float]=None,
         S:Optional[StorageSettings]=None)->List[RRef]:
  """ Find [RRefs](#pylightnix.types.RRef) in Pylightnix sotrage which
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

  FIXME: If name is a stage, then this function instantiates this stage before
  searching. Thus, the storage is moified, which may be a undesired
  behaviour
  """
  rrefs=[]
  name_=None
  if name is not None:
    if isinstance(name,str):
      name_=name
    else:
      stage=name
      drefs=instantiate(stage,S=S)[1].targets
      assert len(drefs)==1, \
        f"Only a one-target stages is supported as a name argument"
      name_=cfgname(drefcfg_(drefs[0], S=S))
  for dref in alldrefs(S=S):
    for rref in drefrrefs(dref,S=S):
      if name_ is not None:
        if not fnmatch(cfgname(drefcfg_(rref2dref(rref),S=S)),name_):
          continue
      if newer is not None:
        if newer<=0:
          reftime=parsetime(timestring())
          assert reftime is not None
          reftime-=abs(newer)
        else:
          reftime=newer
        # FIXME: repair buildtime search
        # btstr=rrefbtime(rref)
        # if btstr is None:
        #   continue
        # btime=parsetime(btstr) if btstr is not None else None
        # if btime is not None:
        #   if btime < reftime:
        #     continue
      rrefs.append(rref)
  return rrefs

def diff(stageA:Union[RRef,DRef,Stage],
         stageB:Union[RRef,DRef,Stage],
         S=None)->None:
  """ Run system's `diff` utility to print the difference between configs of 2
  stages passed.

  Note: if argument is a Stage, it is instantiated first
  """
  def _cfgpathof(s)->Path:
    if isrref(s):
      return drefcfgpath(rref2dref(RRef(s)),S=S)
    elif isdref(s):
      return drefcfgpath(DRef(s),S=S)
    else:
      drefs=instantiate(s,S=S)[1].targets
      assert len(drefs)==1
      return drefcfgpath(drefs[0],S=S)

  Popen(['diff', '-u', _cfgpathof(stageA), _cfgpathof(stageB)],
        shell=False, cwd='/').wait()



def linkrref(rref:RRef,
             destdir:Optional[Path]=None,
             format:str='_rref_%(T)s_%(N)s',
             S=None)->Path:
  """ linkkrref creates a symbolic link to a particular realization reference.
  The new link appears in the `destdir` directory if this argument is not None,
  otherwise the current directory is used.

  Format accepts the following Python pattern tags:
  - `%(T)s` replaced with the build time
  - `%(N)s` replaced with the config name

  Informally, `linkrref` creates the link:
  `{tgtpath}/{format} --> $PYLIGHTNIX_STORE/{dref}/{rref}`.

  The function overwrites existing symlinks.
  """
  timetag_:str=rrefbstart(rref,S) or ''
  nametag_:str=cfgname(drefcfg_(rref2dref(rref),S))
  destdir_=destdir if destdir is not None else '.'
  symlink=Path(join(destdir_,format %{'T':timetag_,'N':nametag_}))
  forcelink(Path(relpath(rref2path(rref,S), destdir_)), symlink)
  return symlink


def linkdref(dref:DRef,
             destdir:Optional[Path]=None,
             format:str='_rref_%(N)s',
             S=None)->Path:
  nametag_:str=cfgname(drefcfg_(dref,S))
  destdir_=destdir if destdir is not None else '.'
  symlink=Path(join(destdir_,format %{'N':nametag_}))
  forcelink(Path(relpath(dref2path(dref,S), destdir_)), symlink)
  return symlink


def linkrrefs(rrefs:Iterable[RRef], destdir:Optional[Path]=None,
              format:str='_rref_%(T)s_%(N)s',
              S=None)->List[Path]:
  """ A Wrapper around `linkrref` for linking a set of RRefs. """
  acc=[]
  for r in rrefs:
    acc.append(linkrref(r, destdir=destdir, format=format, S=S))
  return acc

