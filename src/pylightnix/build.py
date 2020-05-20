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

from pylightnix.imports import ( sha256, deepcopy, isdir, islink, makedirs,
    join, json_dump, json_load, json_dumps, json_loads, isfile, relpath,
    listdir, rmtree, mkdtemp, replace, environ, split, re_match, ENOTEMPTY,
    get_ident, contextmanager, OrderedDict, lstat, maxsize, readlink,
    getLogger )
from pylightnix.utils import ( dirhash, assert_serializable, assert_valid_dict,
    dicthash, scanref_dict, scanref_list, forcelink, timestring, parsetime,
    datahash, readjson, tryread, encode, dirchmod, dirrm, filero, isrref,
    isdref, traverse_dict, ispromise, isclaim, concat )
from pylightnix.types import ( Dict, List, Any, Tuple, Union, Optional,
    Iterable, IO, Path, Hash, DRef, RRef, RefPath, PromisePath, HashPart,
    Callable, Context, Name, NamedTuple, Build, RConfig, ConfigAttrs,
    Derivation, Stage, Manager, Matcher, Realizer, Set, Closure, Generator,
    Key, TypeVar, BuildArgs, PYLIGHTNIX_PROMISE_TAG, PYLIGHTNIX_CLAIM_TAG,
    Config, RealizeArg, InstantiateArg, Tag, RRefGroup )
from pylightnix.core import ( assert_valid_config, store_config, config_cattrs,
    config_hash, config_name, context_deref, assert_valid_refpath, rref2path )

logger=getLogger(__name__)
info=logger.info
warning=logger.warning
error=logger.error

#  ____        _ _     _
# | __ ) _   _(_) | __| |
# |  _ \| | | | | |/ _` |
# | |_) | |_| | | | (_| |
# |____/ \__,_|_|_|\__,_|

def mkbuildargs(dref:DRef, context:Context, timeprefix:Optional[str],
    iarg:InstantiateArg, rarg:RealizeArg)->BuildArgs:
  assert_valid_config(store_config(dref))
  return BuildArgs(dref, context, timeprefix, iarg, rarg)

def mkbuild(dref:DRef, context:Context, buildtime:bool=True)->Build:
  timeprefix=timestring() if buildtime else None
  return Build(mkbuildargs(dref,context,timeprefix,{},{}))

B=TypeVar('B')

def build_wrapper_(
    f:Callable[[B],None],
    ctr:Callable[[BuildArgs],B],
    buildtime:bool=True)->Realizer:
  """ Build Adapter which convers user-defined realizers which use
  [Build](#pylightnix.types.Build) API into a low-level
  [Realizer](#pylightnix.types.Realizer)

  FIXME: Specify the fact that `B` should be derived from `Build` """
  def _wrapper(dref,context,rarg)->List[Dict[Tag,Path]]:
    timeprefix=timestring() if buildtime else None
    b=ctr(mkbuildargs(dref,context,timeprefix,{},rarg));
    try:
      f(b);
      build_markstop(b) # type:ignore
    except:
      build_markstop(b) # type:ignore
      error(f"Build wrapper of {dref} raised an exception. Remaining "
            f"build directories are: {getattr(b,'outgroups','<unknown>')}")
      raise
    return getattr(b,'outgroups')
  return _wrapper

def build_wrapper(f:Callable[[Build],None], buildtime:bool=True)->Realizer:
  """ Build Adapter which convers user-defined realizers which use
  [Build](#pylightnix.types.Build) API into a low-level
  [Realizer](#pylightnix.types.Realizer) """
  return build_wrapper_(f,Build,buildtime)

def build_config(b:Build)->RConfig:
  """ Return the [RConfig](#pylightnix.types.RConfig) object of the realization
  being built. """
  return store_config(b.dref)

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

def build_setoutgroups(b:Build,
                       nouts:int=1,
                       tags:List[Tag]=[Tag('out')])->List[Dict[Tag,Path]]:
  assert nouts>0, f"Attempt to set {nouts} (<=0) output paths"
  assert len(b.outgroups)==0, f"Build outpaths were already set:\n{b.outgroups}"
  assert len(tags)>0, f"Expecting at least one output tag"
  import pylightnix.core
  tmp=pylightnix.core.PYLIGHTNIX_TMP
  h=config_hash(build_config(b))[:8]
  def _prefix(t):
    return f'{b.timeprefix}_{t}_{h}_' if b.timeprefix is not None else f'{t}_{h}_'
  grs=[{t:Path(mkdtemp(prefix=_prefix(t), dir=tmp)) for t in tags} for _ in range(nouts)]
  for ngrp,g in enumerate(grs):
    for tag,o in g.items():
      if b.timeprefix:
        with open(join(o,'__buildtime__.txt'), 'w') as f:
          f.write(b.timeprefix)
      with open(join(o,'tag.txt'), 'w') as f:
        f.write(tag)
      with open(join(o,'group.txt'), 'w') as f:
        f.write(str(ngrp))
  b.outgroups=grs
  return grs

def build_setoutpaths(b:Build, nouts:int)->List[Path]:
  return [g[Tag('out')] for g in build_setoutgroups(b,nouts,[Tag('out')])]

def build_markstop(b:Build, buildstop:Optional[str]=None)->None:
  buildstop_=timestring() if buildstop is None else buildstop
  for g in b.outgroups:
    for outpath in g.values():
      with open(join(outpath,'__buildstop__.txt'), 'w') as f:
        f.write(buildstop_)

def store_buildelta(rref:RRef)->Optional[float]:
  def _gettime(fn)->Optional[float]:
    ts=tryread(Path(join(rref2path(rref),fn)))
    return parsetime(ts) if ts is not None else None
  bb=_gettime('__buildtime__.txt')
  be=_gettime('__buildstop__.txt')
  return be-bb if bb is not None and be is not None else None

def build_outpaths(b:Build)->List[Path]:
  assert len(b.outgroups)>0, f"Build outpaths were not set"
  return [g[Tag('out')] for g in b.outgroups]

def build_outpath(b:Build)->Path:
  """ Return the output path of the realization being built. Output path is a
  path to valid temporary folder where user may put various build artifacts.
  Later this folder becomes a realization. """
  if len(b.outgroups)==0:
    return build_setoutpaths(b,1)[0]
  paths=build_outpaths(b)
  assert len(paths)==1, f"Build was set to have multiple output paths: {paths}"
  return paths[0]

def build_name(b:Build)->Name:
  """ Return the name of a derivation being built. """
  return Name(config_name(build_config(b)))

def build_deref_(b:Build, dref:DRef)->List[RRefGroup]:
  """ For any [realization](#pylightnix.core.realize) process described with
  it's [Build](#pylightnix.types.Build) handler, `build_deref` queries a
  realization of dependency `dref`.

  `build_deref` is designed to be called from
  [Realizer](#pylightnix.types.Realizer) functions. In other cases,
  [store_deref](#pylightnix.core.store_deref) should be used.  """
  return context_deref(build_context(b), dref)

def build_deref(b:Build, dref:DRef)->RRefGroup:
  rgs=build_deref_(b,dref)
  assert len(rgs)==1
  return rgs[0]

def build_paths(b:Build, refpath:RefPath, tag:Tag=Tag('out'))->List[Path]:
  """ Convert given [RefPath](#pylightnix.types.RefPath) (which may be either a
  regular RefPath or an ex-[PromisePath](#pylightnix.types.PromisePath)) into
  one or many filesystem paths. Conversion refers to the
  [Context](#pylightnix.types.Context) of the current realization process by
  accessing it's [build_context](#pylightnix.build.build_context).

  Typically, we configure stages to match only one realization at once, so the
  returned list often has only one entry. Consider using
  [build_path](#pylightnix.build.build_path) if this fact is known in advance.

  Example:
  ```python
  def config(dep:DRef)->RConfig:
    name = 'example-stage'
    input = [dep,"path","to","input.txt"]
    output = [promise,"output.txt"]
    some_param = 42
    return mkconfig(locals())

  def realize(b:Build)->None:
    c=config_cattrs(b)
    with open(build_path(b, c.input),'r') as finp:
      with open(build_path(b, c.output),'w') as fout:
        fout.write(finp.read())

  def mystage(m:Manager)->DRef:
    dep:DRef=otherstage(m)
    return mkdrv(m, config(dep), match_only(), build_wrapper(realize))
  ```
  """
  assert_valid_refpath(refpath)
  if refpath[0]==b.dref:
    assert len(b.outgroups)>0, (
        f"Attempt to access build outpaths before they are set. Call"
        f"`build_outpath(b,num)` first to set their number." )
    return [Path(join(g[tag], *refpath[1:])) for g in b.outgroups]
  else:
    return [Path(join(rref2path(rg[tag]), *refpath[1:])) for rg in build_deref_(b, refpath[0])]

def build_path(b:Build, refpath:RefPath, tag:Tag=Tag('out'))->Path:
  """ A single-realization version of the [build_paths](#pylightnix.build.build_paths). """
  paths=build_paths(b,refpath,tag)
  assert len(paths)==1
  return paths[0]


