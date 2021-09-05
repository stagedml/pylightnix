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

"""
Built-in realization wrapper named `Build` provides helpful functions like
temporary build directory management, time counting, etc.
"""

from pylightnix.imports import (sha256, deepcopy, isdir, islink, makedirs, join,
                                json_dump, json_load, json_dumps, json_loads,
                                isfile, relpath, listdir, rmtree, mkdtemp,
                                replace, split, re_match, ENOTEMPTY, get_ident,
                                contextmanager, OrderedDict, lstat, maxsize,
                                readlink, getLogger, format_exc, environ)

from pylightnix.utils import (dirhash, assert_serializable, assert_valid_dict,
                              dicthash, scanref_dict, scanref_list, forcelink,
                              timestring, parsetime, datahash, readjson,
                              tryread, encode, dirchmod, dirrm, filero, isrref,
                              isdref, traverse_dict, concat, writestr, readstr,
                              tryreadstr_def, isrefpath)

from pylightnix.types import (Dict, List, Any, Tuple, Union, Optional, Iterable,
                              IO, Path, SPath, Hash, DRef, RRef, RefPath,
                              HashPart, Callable, Context, Name, NamedTuple,
                              Build, RConfig, ConfigAttrs, Derivation, Stage,
                              Registry, Matcher, Realizer, RealizerO, Set,
                              Closure, Generator, TypeVar, BuildArgs, Config,
                              RealizeArg, InstantiateArg, SupportsAbs, Output,
                              PylightnixException, StorageSettings)

from pylightnix.core import (assert_valid_config, cfgcattrs,
                             cfghash, cfgname, context_deref,
                             assert_valid_refpath, rref2path, drefdeps1,
                             cfgdict, drefcfg, output_realizer, fstmpdir)

from pylightnix.repl import (ReplHelper, repl_continue, ERR_INVALID_RH,
                             ERR_INACTIVE_RH, repl_cancel)

logger=getLogger(__name__)
info=logger.info
warning=logger.warning
error=logger.error

#  ____        _ _     _
# | __ ) _   _(_) | __| |
# |  _ \| | | | | |/ _` |
# | |_) | |_| | | | (_| |
# |____/ \__,_|_|_|\__,_|


class BuildError(PylightnixException):
  """ Exception class for build errors """
  def __init__(self,
               S:Optional[StorageSettings],
               dref:DRef,
               outpaths:Optional[Output[Path]],
               exception:Exception,
               msg:str=''):
    """ Initialize BuildError instance. """
    super().__init__(msg)
    self.S=S
    self.dref=dref
    self.exception=exception
    self.outpaths:List[Path]=outpaths.val if outpaths else []
  def __str__(self):
    return f"Failed to realize1 '{self.dref}': {self.exception}"

def mkbuildargs(S:Optional[StorageSettings], dref:DRef, context:Context,
                starttime:Optional[str], stoptime:Optional[str],
                iarg:InstantiateArg, rarg:RealizeArg)->BuildArgs:
  assert_valid_config(drefcfg(dref,S))
  return BuildArgs(S, dref, context, starttime, stoptime, iarg, rarg)

_B=TypeVar('_B', bound=Build)
def build_wrapper_(f:Callable[[_B],None],
                   ctr:Callable[[BuildArgs],_B],
                   nouts:Optional[int]=1,
                   starttime:Optional[str]='AUTO',
                   stoptime:Optional[str]='AUTO')->Realizer:
  """ Build Adapter which convers user-defined realizers which use
  [Build](#pylightnix.types.Build) API into a low-level
  [Realizer](#pylightnix.types.Realizer)
  """

  assert starttime is None or isinstance(starttime,str)
  assert stoptime is None or isinstance(stoptime,str)

  def _wrapper(S:Optional[StorageSettings],dref,context,rarg)->Output:
    b=ctr(mkbuildargs(S,dref,context,starttime,stoptime,{},rarg))
    if nouts is not None:
      build_markstart(b,nouts)
    try:
      f(b)
    except KeyboardInterrupt:
      build_markstop_noexcept(b) # type:ignore
      raise
    except Exception as e:
      build_markstop_noexcept(b) # type:ignore
      error(f"Build wrapper of {dref} raised an exception. Remaining "
            f"build directories are: {b.outpaths.val if b.outpaths else '?'}")
      raise BuildError(S,dref,b.outpaths,e)
    assert b.outpaths is not None, \
      "Builder should produce at least one output path"
    build_markstop(b) # type:ignore
    return b.outpaths
  return output_realizer(_wrapper)

def build_wrapper(f:Callable[[Build],None],
                  nouts:Optional[int]=1,
                  starttime:Optional[str]='AUTO',
                  stoptime:Optional[str]='AUTO')->Realizer:
  """ Build Adapter which convers user-defined realizers which use
  [Build](#pylightnix.types.Build) API into a low-level
  [Realizer](#pylightnix.types.Realizer) """
  return build_wrapper_(f,Build,nouts,starttime,stoptime)

def build_config(b:Build)->RConfig:
  """ Return the [Config](#pylightnix.types.RConfig) object of the realization
  being built. """
  return drefcfg(b.dref, b.S)

def build_context(b:Build)->Context:
  """ Return the [Context](#pylightnix.types.Context) object of the realization
  being built. """
  return b.context

def build_cattrs(b:Build)->Any:
  """ Cache and return `ConfigAttrs`. Cache allows realizers to update it's
  value during the build process, e.g. to use it as a storage. """
  if b.cattrs_cache is None:
    b.cattrs_cache=cfgcattrs(build_config(b))
  return b.cattrs_cache

def build_markstart(b:Build, nouts:int)->List[Path]:
  assert nouts>0
  assert b.outpaths is None, \
    f"Attempt to repeatedly set build output paths. "\
    f"Previously set to:\n{b.outpaths}"
  tmp=fstmpdir(b.S)
  h=cfghash(build_config(b))[:8]
  if b.starttime is not None:
    starttime=timestring() if b.starttime=='AUTO' else b.starttime
    paths=[Path(mkdtemp(prefix=f'{starttime}_{h}_', dir=tmp))
           for _ in range(nouts)]
    for o in paths:
      with open(join(o,'__buildstart__.txt'), 'w') as f:
        f.write(starttime)
  else:
    paths=[Path(mkdtemp(prefix=f'{h}_', dir=tmp)) for _ in range(nouts)]
  b.outpaths=Output(paths)
  return paths

def build_markstop(b:Build)->None:
  if b.stoptime is not None:
    stoptime=timestring() if b.stoptime=='AUTO' else b.stoptime
    for outpath in (b.outpaths.val if b.outpaths else []):
      with open(join(outpath,'__buildstop__.txt'), 'w') as f:
        f.write(stoptime)

def build_markstop_noexcept(b:Build)->None:
  try:
    build_markstop(b)
  except:
    pass

def rrefbstart(rref:RRef, S=None)->Optional[str]:
  """ Return the buildtime of the current RRef in a format specified by the
  [PYLIGHTNIX_TIME](#pylightnix.utils.PYLIGHTNIX_TIME) constant.

  [parsetime](#pylightnix.utils.parsetime) may be used to parse stings into
  UNIX-Epoch seconds.

  Buildtime is the time when the realization process was started. Some
  realizations may not provide this information. """
  return tryread(Path(join(rref2path(rref,S),'__buildstart__.txt')))

def rrefbstop(rref:RRef, S=None)->Optional[str]:
  """ Return the buildtime of the current RRef in a format specified by the
  [PYLIGHTNIX_TIME](#pylightnix.utils.PYLIGHTNIX_TIME) constant.

  [parsetime](#pylightnix.utils.parsetime) may be used to parse stings into
  UNIX-Epoch seconds.

  Buildtime is the time when the realization process was started. Some
  realizations may not provide this information. """
  return tryread(Path(join(rref2path(rref,S),'__buildstop__.txt')))

def rrefbdelta(rref:RRef,S=None)->Optional[float]:
  def _parsetime(ts)->Optional[float]:
    return parsetime(ts) if ts is not None else None
  bb=_parsetime(rrefbstart(rref,S))
  be=_parsetime(rrefbstop(rref,S))
  return be-bb if bb is not None and be is not None else None

def build_outpaths(b:Build)->List[Path]:
  assert b.outpaths is not None, (
    f"Attempting to access output paths, but they were not declared. "
    f"Did you set the number of build outputs or call `build_markstart`?")
  return b.outpaths.val

def build_outpath(b:Build)->Path:
  """ Return the output path of the realization being built. Output path is a
  path to valid temporary folder where user may put various build artifacts.
  Later this folder becomes a realization. """
  paths=build_outpaths(b)
  assert len(paths)==1, f"Build was set to have multiple output paths: {paths}"
  return paths[0]

def build_name(b:Build)->Name:
  """ Return the name of a derivation being built. """
  return Name(cfgname(build_config(b)))

def build_deref_(b:Build, dref:DRef)->List[RRef]:
  """ For any [realization](#pylightnix.core.realize1) process described with
  it's [Build](#pylightnix.types.Build) handler, `build_deref` queries a
  realization of dependency `dref`.

  `build_deref` is designed to be called from
  [Realizer](#pylightnix.types.Realizer) functions. In other cases,
  [store_deref](#pylightnix.core.store_deref) should be used.  """
  return context_deref(build_context(b), dref)

def build_deref(b:Build, dref:DRef)->RRef:
  rrefs=build_deref_(b,dref)
  assert len(rrefs)==1
  return rrefs[0]

def build_paths(b:Build, refpath:RefPath)->List[Path]:
  assert_valid_refpath(refpath)
  if refpath[0]==b.dref:
    assert b.outpaths is not None, (
      "Attempt to access build outpaths before they are set. Call"
      "`build_markstart(b,num)` first to set their number." )
    return [Path(join(path, *refpath[1:])) for path in b.outpaths.val]
  else:
    return [Path(join(rref2path(rref,b.S), *refpath[1:]))
            for rref in build_deref_(b, DRef(refpath[0]))]

def build_path(b:Build, refpath:RefPath)->Path:
  """ A single-realization version of the
  [build_paths](#pylightnix.build.build_paths). """
  paths=build_paths(b,refpath)
  assert len(paths)==1
  return paths[0]


def build_environ(b:Build, env:Optional[Any]=None)->dict:
  """ Prepare environment by adding Build's config to the environment as
  variables. The function resolves all singular RefPaths into system paths
  using current Build's context.

  FIXME: Use bash-array syntax for multi-ouput paths """

  if env is None:
    env=environ
  acc=dict(deepcopy(env))
  be=cfgdict(build_config(b))
  for k,v in be.items():
    if isrefpath(v):
      syspaths=build_paths(b,v)
      if len(syspaths)==1:
        v=syspaths[0]
    acc[str(k)]=str(v)
  return acc


def repl_continueBuild(b:Build, rh:Optional[ReplHelper]=None)->Optional[RRef]:
  build_markstop(b)
  return repl_continue(out_paths=b.outpaths.val if b.outpaths else [], rh=rh)


def repl_buildargs(rh:Optional[ReplHelper]=None)->BuildArgs:
  import pylightnix.repl
  if rh is None:
    rh=pylightnix.repl.PYLIGHTNIX_REPL_HELPER
  assert rh is not None, ERR_INVALID_RH
  assert rh.context is not None, ERR_INACTIVE_RH
  assert rh.dref is not None, ERR_INACTIVE_RH
  assert rh.rarg is not None, ERR_INACTIVE_RH
  assert rh.S is not None, ERR_INACTIVE_RH
  return mkbuildargs(rh.S,rh.dref,rh.context,'AUTO','AUTO',{},rh.rarg)


def repl_build(rh:Optional[ReplHelper]=None, nouts:Optional[int]=1)->Build:
  """ Return `Build` object for using in repl-based debugging

  Example:
  ```
  from stages import some_stage, some_stage_build, some_stage_train

  rh=repl_realize(instantiate(some_stage))
  b=repl_build(rh)
  some_stage_build(b) # Debug as needed
  some_stage_train(b) # Debug as needed
  ```
  """
  b=Build(repl_buildargs(rh))
  if nouts is not None:
    build_markstart(b,nouts)
  return b

def repl_cancelBuild(b:Build, rh:Optional[ReplHelper]=None)->None:
  build_markstop(b)
  repl_cancel(rh)
  for o in (b.outpaths.val if b.outpaths else []):
    dirrm(o)


