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
                              Manager, Matcher, Realizer, Set, Closure,
                              Generator, TypeVar, BuildArgs, Config, RealizeArg,
                              InstantiateArg, SupportsAbs)

from pylightnix.core import (assert_valid_config, config_cattrs,
                             config_hash, config_name, context_deref,
                             assert_valid_refpath, rref2path, drefdeps1,
                             config_dict, drefcfg)

from pylightnix.repl import (ReplHelper, repl_continue, ERR_INVALID_RH,
                             ERR_INACTIVE_RH)

logger=getLogger(__name__)
info=logger.info
warning=logger.warning
error=logger.error

#  ____        _ _     _
# | __ ) _   _(_) | __| |
# |  _ \| | | | | |/ _` |
# | |_) | |_| | | | (_| |
# |____/ \__,_|_|_|\__,_|


class BuildError(Exception):
  """ Exception class for build errors """
  def __init__(self,
               S:SPath,
               dref:DRef,
               outpaths:List[Path],
               exception:Exception,
               msg:str=''):
    """ Initialize BUildError instance. """
    super().__init__(msg)
    self.storage=S
    self.dref=dref
    self.exception=exception
    self.outpaths:List[Path]=outpaths
  def __str__(self):
    return f"Failed to realize '{self.dref}': {self.exception}"

def mkbuildargs(S:SPath, dref:DRef, context:Context, starttime:Optional[str],
                iarg:InstantiateArg, rarg:RealizeArg)->BuildArgs:
  assert_valid_config(drefcfg(dref,S))
  return BuildArgs(S, dref, context, starttime, iarg, rarg)

def mkbuild(S:SPath, dref:DRef, context:Context, buildtime:bool=True)->Build:
  timeprefix=timestring() if buildtime else None
  return Build(mkbuildargs(S,dref,context,timeprefix,{},{}))

_B=TypeVar('_B')
def build_wrapper_(f:Callable[[_B],None],
                   ctr:Callable[[BuildArgs],_B],
                   starttime:Optional[str]=None,
                   stoptime:Optional[str]=None)->Realizer:
  """ Build Adapter which convers user-defined realizers which use
  [Build](#pylightnix.types.Build) API into a low-level
  [Realizer](#pylightnix.types.Realizer)

  FIXME: Find out how to Specify the fact that `B` has to be derived from
         `Build`. Maybe just replace `B` with `Build` and require deriving from
         it? [*]
  """

  assert starttime is None or isinstance(starttime,str)
  assert stoptime is None or isinstance(stoptime,str)

  def _wrapper(S:SPath,dref,context,rarg)->List[Path]:
    b=ctr(mkbuildargs(S,dref,context,starttime,{},rarg))
    try:
      f(b)
      build_markstop(b,stoptime) # type:ignore
    except KeyboardInterrupt:
      build_markstop(b,stoptime) # type:ignore
      raise
    except Exception as e:
      build_markstop(b,stoptime) # type:ignore
      error(f"Build wrapper of {dref} raised an exception. Remaining "
            f"build directories are: {getattr(b,'outgroups','<unknown>')}")
      raise BuildError(S,dref,getattr(b,'outgroups',[]), e)
    return getattr(b,'outpaths') # [*]
  return _wrapper

def build_wrapper(f:Callable[[Build],None],
                  starttime:Optional[str]=None,
                  stoptime:Optional[str]=None)->Realizer:
  """ Build Adapter which convers user-defined realizers which use
  [Build](#pylightnix.types.Build) API into a low-level
  [Realizer](#pylightnix.types.Realizer) """
  return build_wrapper_(f,Build,starttime,stoptime)

def build_config(b:Build)->RConfig:
  """ Return the [Config](#pylightnix.types.RConfig) object of the realization
  being built. """
  return drefcfg(b.dref, b.storage)

def build_context(b:Build)->Context:
  """ Return the [Context](#pylightnix.types.Context) object of the realization
  being built. """
  return b.context

def build_cattrs(b:Build)->Any:
  """ Cache and return `ConfigAttrs`. Cache allows realizers to update it's
  value during the build process, e.g. to use it as a storage. """
  if b.cattrs_cache is None:
    b.cattrs_cache=config_cattrs(build_config(b))
  return b.cattrs_cache

def build_setoutpaths(b:Build,
                      nouts:int)->List[Path]:
  assert nouts>0
  assert len(b.outpaths)==0, \
    f"Build outpaths were already set:\n{b.outpaths}"
  # assert all([len(tags)>0 for tags in tagset]), \
  #   f"Every group of tags should have at least one tag, got {tagset}"
  import pylightnix.core
  tmp=pylightnix.core.PYLIGHTNIX_TMP
  h=config_hash(build_config(b))[:8]
  def _prefix():
    return f'{b.timeprefix}_{h}_' if b.timeprefix is not None else f'{h}_'
  paths=[Path(mkdtemp(prefix=_prefix(), dir=tmp)) for _ in range(nouts)]
  for o in paths:
    if b.timeprefix:
      with open(join(o,'__buildtime__.txt'), 'w') as f:
        f.write(b.timeprefix)
  b.outpaths=paths
  return paths

# def build_setoutpaths(b:Build, nouts:int)->List[Path]:
#   return [g[Tag('out')] for g in
#           build_setoutgroups(b,[[Tag('out')] for _ in range(nouts)])]

def build_markstop(b:Build, buildstop:Optional[str])->None:
  buildstop_=timestring() if buildstop is None else buildstop
  for outpath in b.outpaths:
    with open(join(outpath,'__buildstop__.txt'), 'w') as f:
      f.write(buildstop_)

def store_buildelta(rref:RRef,S=None)->Optional[float]:
  def _gettime(fn)->Optional[float]:
    ts=tryread(Path(join(rref2path(rref,S),fn)))
    return parsetime(ts) if ts is not None else None
  bb=_gettime('__buildtime__.txt')
  be=_gettime('__buildstop__.txt')
  return be-bb if bb is not None and be is not None else None

def build_outpaths(b:Build)->List[Path]:
  assert len(b.outpaths)>0, (
    f"Attempting to access output paths, but they were not declared. "
    f"Did you call `build_setoutpaths`?")
  return b.outpaths

def build_outpath(b:Build)->Path:
  """ Return the output path of the realization being built. Output path is a
  path to valid temporary folder where user may put various build artifacts.
  Later this folder becomes a realization. """
  if len(b.outpaths)==0:
    return build_setoutpaths(b,1)[0]
  paths=build_outpaths(b)
  assert len(paths)==1, f"Build was set to have multiple output paths: {paths}"
  return paths[0]

def build_name(b:Build)->Name:
  """ Return the name of a derivation being built. """
  return Name(config_name(build_config(b)))

def build_deref_(b:Build, dref:DRef)->List[RRef]:
  """ For any [realization](#pylightnix.core.realize) process described with
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
    assert len(b.outpaths)>0, (
      "Attempt to access build outpaths before they are set. Call"
      "`build_setoutpath(b,num)` first to set their number." )
    return [Path(join(path, *refpath[1:])) for path in b.outpaths]
  else:
    return [Path(join(rref2path(rref,b.storage), *refpath[1:]))
            for rref in build_deref_(b, refpath[0])]

def build_path(b:Build, refpath:RefPath)->Path:
  """ A single-realization version of the [build_paths](#pylightnix.build.build_paths). """
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
  be=config_dict(build_config(b))
  for k,v in be.items():
    if isrefpath(v):
      syspaths=build_paths(b,v)
      if len(syspaths)==1:
        v=syspaths[0]
    acc[str(k)]=str(v)
  return acc


def repl_continueBuild(b:Build, rh:Optional[ReplHelper]=None)->Optional[RRef]:
  return repl_continue(out_paths=b.outpaths, rh=rh)


def repl_buildargs(rh:Optional[ReplHelper]=None, buildtime:bool=True)->BuildArgs:
  import pylightnix.repl
  if rh is None:
    rh=pylightnix.repl.PYLIGHTNIX_REPL_HELPER
  assert rh is not None, ERR_INVALID_RH
  assert rh.context is not None, ERR_INACTIVE_RH
  assert rh.dref is not None, ERR_INACTIVE_RH
  assert rh.rarg is not None, ERR_INACTIVE_RH
  assert rh.storage is not None, ERR_INACTIVE_RH
  timeprefix=timestring() if buildtime else None
  return mkbuildargs(rh.storage, rh.dref, rh.context, timeprefix, {}, rh.rarg)


def repl_build(rh:Optional[ReplHelper]=None, buildtime:bool=True)->Build:
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
  return Build(repl_buildargs(rh, buildtime))

# def either_wrapper(f:Callable[[Build],None],
#                    ctr:Callable[[BuildArgs],Build],
#                    buildtime:bool=True,
#                    nouts:int=1)->Realizer:
#   """ This wrapper implements poor-man's `(EitherT Error)` monad on stages.
#   With this wrapper, stages could become either LEFT (if rasied an error) or
#   RIGHT (after normal completion). If the stage turns LEFT, then so will be any
#   of it's dependant stages. """
#   def _either(b:Build)->None:
#     build_setoutpaths(b, nouts)
#     # Write the specified build status to every output
#     def _mark_status(status:str, e:Optional[str]=None)->None:
#       for o in build_outpaths(b):
#         writestr(join(o,'status_either.txt'), status)
#         if e is not None:
#           writestr(join(o,'exception.txt'), e)
#     # Scan all immediate dependecnies of this build, propagate 'LEFT' status
#     for dref in drefdeps1([b.dref]):
#       for rg in context_deref(b.context, dref):
#         rref = rg[Tag('out')]
#         status=tryreadstr_def(join(rref2path(rref),'status_either.txt'), 'RIGHT')
#         if status=='RIGHT':
#           continue
#         elif status=='LEFT':
#           _mark_status('LEFT')
#           return
#         else:
#           assert False, f"Invalid either status {status}"
#     # Execute the original build
#     try:
#       f(b)
#       _mark_status('RIGHT')
#     except KeyboardInterrupt:
#       raise
#     except Exception:
#       _mark_status('LEFT', format_exc())
#   realizer=build_wrapper_(_either, ctr, buildtime)
#   return realizer


