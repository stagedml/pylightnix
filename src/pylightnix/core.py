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
Core Pylightnix definitions
"""

from pylightnix.imports import ( sha256, deepcopy, isdir, islink, makedirs,
    join, json_dump, json_load, json_dumps, json_loads, isfile, relpath,
    listdir, rmtree, mkdtemp, replace, environ, split, re_match, ENOTEMPTY,
    get_ident, contextmanager, OrderedDict, lstat, maxsize, readlink )
from pylightnix.utils import ( dirhash, assert_serializable, assert_valid_dict,
    dicthash, scanref_dict, scanref_list, forcelink, timestring, parsetime,
    datahash, readjson, tryread, encode, dirchmod, dirrm, filero, isrref,
    isdref, traverse_dict, ispromise, isclaim )
from pylightnix.types import (
    Dict, List, Any, Tuple, Union, Optional, Iterable, IO, Path, Hash, DRef,
    RRef, RefPath, PromisePath, HashPart, Callable, Context, Name, NamedTuple,
    Build, RConfig, ConfigAttrs, Derivation, Stage, Manager, Matcher, Realizer,
    Set, Closure, Generator, Key, TypeVar, BuildArgs, PYLIGHTNIX_PROMISE_TAG,
    PYLIGHTNIX_CLAIM_TAG, Config, RealizeArg, InstantiateArg )

#: *Do not change!*
#: Tracks the version of pylightnix storage
PYLIGHTNIX_STORE_VERSION = 0

#: `PYLIGHTNIX_ROOT` contains the path to the root of pylightnix shared data folder.
#:
#: Default is `~/_pylightnix` or `/var/run/_pylightnix` if no `$HOME` is available.
#: Setting `PYLIGHTNIX_ROOT` environment variable overwrites the defaults.
PYLIGHTNIX_ROOT = environ.get('PYLIGHTNIX_ROOT', join(environ.get('HOME','/var/run'),'_pylightnix'))


#: `PYLIGHTNIX_TMP` contains the path to the root of temporary folders.
#: Setting `PYLIGHTNIX_TMP` environment variable overwrites the default value of
#: `$PYLIGHTNIX_ROOT/tmp`.
PYLIGHTNIX_TMP = environ.get('PYLIGHTNIX_TMP', join(PYLIGHTNIX_ROOT,'tmp'))

#: `PYLIGHTNIX_STORE` contains the path to the main pylightnix store folder.
#:
#: By default, the store is located in `$PYLIGHTNIX_ROOT/store-vXX` folder.
#: Setting `PYLIGHTNIX_STORE` environment variable overwrites the defaults.
PYLIGHTNIX_STORE = join(PYLIGHTNIX_ROOT, f'store-v{PYLIGHTNIX_STORE_VERSION}')

#: Set the regular expression pattern for valid name characters.
PYLIGHTNIX_NAMEPAT = "[a-zA-Z0-9_-]"

#  ____       __
# |  _ \ ___ / _|___
# | |_) / _ \ |_/ __|
# |  _ <  __/  _\__ \
# |_| \_\___|_| |___/

def trimhash(h:Hash)->HashPart:
  """ Trim a hash to get `HashPart` objects which are used in referencing """
  return HashPart(h[:32])

def mkdref(dhash:HashPart, refname:Name)->DRef:
  assert_valid_hashpart(dhash)
  assert_valid_name(refname)
  return DRef('dref:'+dhash+'-'+refname)

def rref2dref(rref:RRef)->DRef:
  return mkdref(*unrref(rref)[1:])

def undref(r:DRef)->Tuple[HashPart, Name]:
  assert_valid_dref(r)
  return (HashPart(r[5:5+32]), Name(r[5+32+1:]))

def mkrref(rhash:HashPart, dhash:HashPart, refname:Name)->RRef:
  assert_valid_name(refname)
  assert_valid_hashpart(rhash)
  assert_valid_hashpart(dhash)
  return RRef('rref:'+rhash+'-'+dhash+'-'+refname)

def unrref(r:RRef)->Tuple[HashPart, HashPart, Name]:
  assert_valid_rref(r)
  return (HashPart(r[5:5+32]), HashPart(r[5+32+1:5+32+1+32]), Name(r[5+32+1+32+1:]))

def mkname(s:str)->Name:
  assert_valid_name(Name(s))
  return Name(s)

def path2rref(p:Path)->RRef:
  if islink(p):
    p=Path(readlink(p))
  head,h1=split(p)
  _,dref=split(head)
  h2,nm=undref(DRef('dref:'+dref))
  return mkrref(HashPart(h1),HashPart(h2),mkname(nm))


#   ____             __ _
#  / ___|___  _ __  / _(_) __ _
# | |   / _ \| '_ \| |_| |/ _` |
# | |__| (_) | | | |  _| | (_| |
#  \____\___/|_| |_|_| |_|\__, |
#                         |___/


def mkconfig(d:dict)->Config:
  return Config(assert_valid_dict(d,'dict'))

def config_dict(cp:Config)->dict:
  return deepcopy(cp.val)

def config_cattrs(c:RConfig)->Any:
  return ConfigAttrs(config_dict(c))

def config_serialize(c:Config)->str:
  return json_dumps(config_dict(c), indent=4)

def config_hash(c:Config)->Hash:
  return datahash([encode(config_serialize(c))])

def config_name(c:Config)->Name:
  """ Return short human-readable name of a config """
  return mkname(config_dict(c).get('name','unnamed'))

def config_deps(c:RConfig)->Set[DRef]:
  drefs,_=scanref_dict(config_dict(c))
  return set(drefs)

def config_substitutePromises(c:Config, r:DRef)->RConfig:
  """ Replace all Promise tags with DRef `r`. In particular, all PromisePaths
  are converted into RefPaths. """
  d=config_dict(c)
  def _mut(k:Any,val:Any):
    if ispromise(val) or isclaim(val):
      return [DRef(r)]+val[1:]
    else:
      return val
  traverse_dict(d,_mut)
  return RConfig(d)

def config_promises(c:Config, r:DRef)->List[Tuple[str,PromisePath]]:
  promises=[]
  def _mut(key:Any, val:Any):
    nonlocal promises
    if ispromise(val):
      promises.append((str(key),val))
    return val
  traverse_dict(config_dict(c),_mut)
  return promises

#  ____  _
# / ___|| |_ ___  _ __ ___
# \___ \| __/ _ \| '__/ _ \
#  ___) | || (_) | | |  __/
# |____/ \__\___/|_|  \___|

def assert_store_initialized()->None:
  assert isdir(PYLIGHTNIX_STORE), \
    (f"Looks like the Pylightnix store ('{PYLIGHTNIX_STORE}') is not initialized. Did "
     f"you call `store_initialize`?")
  assert isdir(PYLIGHTNIX_TMP), \
    (f"Looks like the Pylightnix tmp ('{PYLIGHTNIX_TMP}') is not initialized. Did "
     f"you call `store_initialize`?")
  assert lstat(PYLIGHTNIX_STORE).st_dev == lstat(PYLIGHTNIX_TMP).st_dev, \
    (f"Looks like Pylightnix store and tmp directories belong to different filesystems. "
     f"This case is not supported yet. Consider setting PYLIGHTNIX_TMP to be on the same "
     f"device with PYLIGHTNIX_STORE")

def store_initialize(custom_store:Optional[str]=None, custom_tmp:Optional[str]=None, check_not_exist:bool=False)->None:
  """ Create the storage and temp direcories if they don't exist. Default
  locations are determined by `PYLIGHTNIX_STORE` and `PYLIGHTNIX_TMP` global
  variables which in turn may be set by either setting environment variables of
  the same name or by direct assigning.

  Parameters:
  - `custom_store`: If not None, create new storage located here.
  - `custom_tmp`: If not None, set the temp files directory here.
  - `check_not_exist`: Set to True to assert on already existing storages

  See also [assert_store_initialized](#pylightnix.core.assert_store_initialized).

  Example:
  ```python
  import pylightnix.core
  pylightnix.core.PYLIGHTNIX_STORE='/tmp/custom_pylightnix_storage'
  pylightnix.core.PYLIGHTNIX_TMP='/tmp/custom_pylightnix_tmp'
  pylightnix.core.store_initialize()
  ```
  """
  global PYLIGHTNIX_STORE, PYLIGHTNIX_TMP

  if custom_store is not None:
    PYLIGHTNIX_STORE=custom_store
  print(f"Initializing {'' if isdir(PYLIGHTNIX_STORE) else 'non-'}existing {PYLIGHTNIX_STORE}")
  makedirs(PYLIGHTNIX_STORE, exist_ok=False if check_not_exist else True)

  if custom_tmp is not None:
    PYLIGHTNIX_TMP=custom_tmp
  makedirs(PYLIGHTNIX_TMP, exist_ok=True)

  assert_store_initialized()

def store_dref2path(r:DRef)->Path:
  (dhash,nm)=undref(r)
  return Path(join(PYLIGHTNIX_STORE,dhash+'-'+nm))

def rref2path(r:RRef)->Path:
  (rhash,dhash,nm)=unrref(r)
  return Path(join(PYLIGHTNIX_STORE,dhash+'-'+nm,rhash))

def mkrefpath(r:DRef, items:List[str]=[])->RefPath:
  """ Construct a [RefPath](#pylightnix.types.RefPath) out of a reference `ref`
  and a path within the stage's realization """
  assert_valid_dref(r)
  return [str(r)]+items

def store_cfgpath(r:DRef)->Path:
  return Path(join(store_dref2path(r),'config.json'))

def store_config_(r:DRef)->Config:
  return assert_valid_config(Config(readjson(store_cfgpath(r))))

def store_config(r:Union[DRef,RRef])->RConfig:
  """ Read the [Config](#pylightnix.types.Config) of the derivation and
  [resolve](#pylightnix.core.config_substitutePromises) it from promises and
  claims. """
  assert isrref(r) or isdref(r), (
      f"Invalid reference {r}. Expected either RRef or DRef." )
  if isrref(r):
    dref=rref2dref(RRef(r))
  else:
    dref=DRef(r)
  return config_substitutePromises(store_config_(dref),dref)

def store_context(r:RRef)->Context:
  """
  FIXME: Either do `context_add(ctx, rref2dref(r), [r])` or document it's absense
  """
  assert_valid_rref(r)
  return readjson(join(rref2path(r),'context.json'))

def store_cattrs(r:Union[DRef,RRef])->Any:
  """ Read the [ConfigAttrs](#pylightnix.types.ConfigAttr) of the storage node `r`.
  Note, that it is a kind of 'syntactic sugar' for `store_config`. Both
  functions do the same thing. """
  return config_cattrs(store_config(r))

def store_deps(drefs:Iterable[DRef])->Set[DRef]:
  """ Return a list of reference's immediate dependencies, not including `refs`
  themselves. """
  acc=set()
  for dref in drefs:
    acc.update(config_deps(store_config(dref))-{dref})
  return acc

def store_deepdeps(roots:Iterable[DRef])->Set[DRef]:
  """ Return the complete set of `roots`'s dependencies, not including `roots`
  themselves. """
  frontier=store_deps(roots)
  processed=set()
  while frontier:
    ref = frontier.pop()
    processed.add(ref)
    for dep in store_deps([ref]):
      if not dep in processed:
        frontier.add(dep)
  return processed

def store_deepdepRrefs(roots:Iterable[RRef])->Set[RRef]:
  """ Return the complete set of root's dependencies, not including `roots`
  themselves.
  """
  acc:Set=set()
  for rref in roots:
    for rref_deps in store_context(rref).values():
      acc|=set(rref_deps)
  return acc

def store_drefs()->Iterable[DRef]:
  """ Iterates over all derivations of the storage """
  for dirname in listdir(PYLIGHTNIX_STORE):
    if dirname[-4:]!='.tmp' and isdir(join(PYLIGHTNIX_STORE,dirname)):
      yield mkdref(HashPart(dirname[:32]), Name(dirname[32+1:]))

def store_rrefs_(dref:DRef)->Iterable[RRef]:
  """ Iterate over all realizations of a derivation `dref`. The sort order is
  unspecified. """
  (dhash,nm)=undref(dref)
  drefpath=store_dref2path(dref)
  for f in listdir(drefpath):
    if f[-4:]!='.tmp' and isdir(join(drefpath,f)):
      yield mkrref(HashPart(f), dhash, nm)

def store_rrefs(dref:DRef, context:Context)->Iterable[RRef]:
  """ Iterate over realizations of a derivation `dref`, which match a
  [context](#pylightnix.types.Context). The sort order is unspecified. """
  for rref in store_rrefs_(dref):
    context2=store_context(rref)
    if context_eq(context,context2):
      yield rref

def store_deref_(context_holder:RRef, dref:DRef)->List[RRef]:
  return context_deref(store_context(context_holder), dref)

def store_deref(context_holder:RRef, dref:DRef)->RRef:
  """ For any realization `context_holder` and it's dependency `dref`, `store_deref`
  queries the realization reference of this dependency.

  See also [build_deref](#pylightnix.core.build_deref)"""
  rrefs=store_deref_(context_holder, dref)
  assert len(rrefs)==1
  return rrefs[0]

def store_buildtime(rref:RRef)->Optional[str]:
  """ Return the buildtime of the current RRef in a format specified by the
  [PYLIGHTNIX_TIME](#pylightnix.utils.PYLIGHTNIX_TIME) constant.

  [parsetime](#pylightnix.utils.parsetime) may be used to parse stings into
  UNIX-Epoch seconds.

  Buildtime is the time when the realization process has started. Some
  realizations may not provide this information. """
  return tryread(Path(join(rref2path(rref),'__buildtime__.txt')))

def store_gc(keep_drefs:List[DRef], keep_rrefs:List[RRef])->Tuple[Set[DRef],Set[RRef]]:
  """ Take roots which are in use and should not be removed. Return roots which
  are not used and may be removed. Actual removing is to be done by the user.

  See also [rmref](#pylightnix.bashlike.rmref)"""
  assert_store_initialized()
  keep_rrefs_=set(keep_rrefs)
  keep_drefs_=set(keep_drefs)
  closure_rrefs=store_deepdepRrefs(keep_rrefs_) | keep_rrefs_
  closure_drefs=store_deepdeps(keep_drefs_) | keep_drefs_ | {rref2dref(rref) for rref in closure_rrefs}
  remove_drefs=set()
  remove_rrefs=set()
  for dref in store_drefs():
    if dref not in closure_drefs:
      remove_drefs.add(dref)
    for rref in store_rrefs_(dref):
      if rref not in closure_rrefs:
        remove_rrefs.add(rref)
  return remove_drefs,remove_rrefs


def store_instantiate(c:Config)->DRef:
  """ Place new instantiation into the storage. We attempt to do it atomically
  by moving the directory right into it's place.

  FIXME: Assert or handle possible (but improbable) hash collision (*)
  """
  assert_store_initialized()
  # c=cp.config
  assert_valid_config(c)
  warn_rref_deps(c)

  refname=config_name(c)
  dhash=config_hash(c)

  dref=mkdref(trimhash(dhash),refname)

  o=Path(mkdtemp(prefix=refname, dir=PYLIGHTNIX_TMP))
  with open(join(o,'config.json'), 'w') as f:
    f.write(config_serialize(c))

  filero(Path(join(o,'config.json')))
  drefpath=store_dref2path(dref)
  dreftmp=Path(drefpath+'.tmp')
  replace(o,dreftmp)

  try:
    replace(dreftmp, drefpath)
  except OSError as err:
    if err.errno == ENOTEMPTY:
      # Existing folder means that it has a matched content (*)
      dirrm(dreftmp, ignore_not_found=False)
    else:
      raise
  return dref

def store_realize(dref:DRef, l:Context, o:Path)->RRef:
  """
  FIXME: Assert or handle possible but improbable hash collision (*)
  """
  c=store_config(dref)
  assert_valid_config(c)
  (dhash,nm)=undref(dref)

  assert isdir(o), (
     f"While realizing {dref}: Outpath is expected to be a path to existing "
     f"directory, but got {o}")
  assert not isfile(join(o,'context.json')), (
     f"While realizing {dref}: one of build artifacts has name 'context.json'. "
     f"This name is reserved, please rename the artifact.")
  with open(join(o,'context.json'), 'w') as f:
    f.write(context_serialize(l))

  rhash=dirhash(o)
  rref=mkrref(trimhash(rhash),dhash,nm)
  rrefpath=rref2path(rref)
  rreftmp=Path(rrefpath+'.tmp')

  replace(o,rreftmp)
  dirchmod(rreftmp,'ro')

  try:
    replace(rreftmp,rrefpath)
  except OSError as err:
    if err.errno == ENOTEMPTY:
      # Existing folder means that it has a matched content (*)
      dirrm(rreftmp, ignore_not_found=False)
    else:
      # Attempt to roll-back
      dirchmod(rreftmp,'rw')
      replace(rreftmp,o)
      raise
  return rref

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
  def _wrapper(dref,context,rarg)->List[Path]:
    timeprefix=timestring() if buildtime else None
    b=ctr(mkbuildargs(dref,context,timeprefix,{},rarg));
    try:
      f(b);
      return list(getattr(b,'outpaths'))
    except:
      print(f'Build wrapper of {dref} raised an exception. Remaining '
            f'build directories are: {getattr(b,"outpaths","<unknown>")}')
      raise
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

def build_setoutpaths(b:Build, nouts:int)->List[Path]:
  assert nouts>0, f"Attempt to set {nouts} (<=0) output paths"
  assert len(b.outpaths)==0, f"Build outpaths were already set to {b.outpaths}"
  prefix=f'{b.timeprefix}_{config_hash(build_config(b))[:8]}_'
  outpaths=[Path(mkdtemp(prefix=prefix, dir=PYLIGHTNIX_TMP)) for _ in range(nouts)]
  if b.timeprefix is not None:
    for outpath in outpaths:
      with open(join(outpath,'__buildtime__.txt'), 'w') as f:
        f.write(b.timeprefix)
  b.outpaths=outpaths
  return b.outpaths

def build_outpaths(b:Build)->List[Path]:
  assert len(b.outpaths)>0, f"Build outpaths were not set"
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
  """ Convert given [RefPath](#pylightnix.types.RefPath) (which may be either a
  regular RefPath or an ex-[PromisePath](#pylightnix.types.PromisePath)) into
  one or many filesystem paths. Conversion refers to the
  [Context](#pylightnix.types.Context) of the current realization process by
  accessing it's [build_context](#pylightnix.core.build_context).

  Typically, we configure stages to match only one realization at once, so the
  returned list often has only one entry. Consider using
  [build_path](#pylightnix.core.build_path) if this fact is known in advance.

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
    assert len(b.outpaths), (
        f"Attempt to access build outpaths before they are set. Call"
        f"`build_outpath(b,num)` first to set their number." )
    return [Path(join(path, *refpath[1:])) for path in b.outpaths]
  else:
    return [Path(join(rref2path(rref), *refpath[1:])) for rref in build_deref_(b, refpath[0])]

def build_path(b:Build, refpath:RefPath)->Path:
  """ A single-realization version of the [build_paths](#pylightnix.core.build_paths). """
  paths=build_paths(b,refpath)
  assert len(paths)==1
  return paths[0]

#   ____            _            _
#  / ___|___  _ __ | |_ _____  _| |_
# | |   / _ \| '_ \| __/ _ \ \/ / __|
# | |__| (_) | | | | ||  __/>  <| |_
#  \____\___/|_| |_|\__\___/_/\_\\__|


def mkcontext()->Context:
  return {}


def context_eq(a:Context,b:Context)->bool:
  return json_dumps(a)==json_dumps(b)

def context_add(context:Context, dref:DRef, rrefs:List[RRef])->Context:
  assert dref not in context, (
    f"Attempting to re-introduce DRef {dref} to context with "
    f"different realization.\n"
    f" * Old realization: {context[dref]}\n"
    f" * New realization: {rrefs}\n" )
  context[dref]=rrefs
  return context

def context_deref(context:Context, dref:DRef)->List[RRef]:
  assert dref in context, (
      f"Context {context} doesn't declare {dref} among it's dependencies so we "
      f"can't dereference it." )
  return context[dref]

def context_serialize(c:Context)->str:
  assert_valid_context(c)
  return json_dumps(c, indent=4)

#  _____           _                _
# |_   _|__  _ __ | | _____   _____| |
#   | |/ _ \| '_ \| |/ _ \ \ / / _ \ |
#   | | (_) | |_) | |  __/\ V /  __/ |
#   |_|\___/| .__/|_|\___| \_/ \___|_|
#           |_|


#: Promise is a magic constant required to create
#: [PromisePath](#pylightnix.types.PromisePath), where it is used as a start
#: marker. Promise paths do exist only during
#: [instantiation](#pylightnix.core.instantiate) pass. The core replaces all
#: PromisePaths with corresponding [RefPaths](#pylightnix.type.RefPath)
#: automatically before it starts the realization pass (see
#: [store_config](#pylightnix.core.store_config)).
#:
#: Ex-PromisePaths may be later converted into filesystem paths by
#: [build_path](#pylightnix.core.build_path) or by
#: [Lenses](#pylightnix.lens.Lens) as usual.
promise = PYLIGHTNIX_PROMISE_TAG

#: Claim is a [promise](#pylightnix.core.promise) which is not checked by the
#: Pylightnix. All other properties of promises are valid for claims.  All
#: PromisPaths which start from `claim` are substituted with corresponding
#: RefPaths by Pylightnix and may be later converted into system paths.
claim = PYLIGHTNIX_CLAIM_TAG

def assert_promise_fulfilled(k:str, p:PromisePath, o:Path)->None:
  ppath=join(o,*p[1:])
  assert isfile(ppath) or isdir(ppath) or islink(ppath), (
      f"Promise '{k}' of {p[0]} is not fulfilled. "
      f"{ppath} is expected to be a file or a directory.")


def mkdrv(m:Manager,
          config:Config,
          matcher:Matcher,
          realizer:Realizer,
          check_promises:bool=True)->DRef:
  """ Run the instantiation of a particular stage. Create a
  [Derivation](#pylightnix.types.Derivation) object out of three main
  components: the Derivation reference, the Matcher and the Realizer. Register
  the derivation in a [Manager](#pylightnix.types.Manager) to aid dependency
  resolution. Return [Derivation reference](#pylightnix.types.DRef) of the
  derivation produced.

  Arguments:
  - `check_promises:bool=True`: Make sure that all
    [PromisePath](#pylightnix.types.PromisePaths) of stage's configuration
    correspond to existing files or firectories.

  Example:
  ```python
  def somestage(m:Manager)->DRef:
    def _realizer(b:Build):
      with open(join(build_outpath(b),'artifact'),'w') as f:
        f.write(...)
    return mkdrv(m,mkconfig({'name':'mystage'}), match_only(), build_wrapper(_realizer))

  rref:RRef=realize(instantiate(somestage))
  ```
  """
  dref=store_instantiate(config)
  if dref in m.builders:
    print((f"Overwriting either the matcher or the realizer of '{dref}'. "
           f"RConfig:\n{store_config_(dref)}"))

  def _promise_aware(realizer)->Realizer:
    def _realizer(dref:DRef,ctx:Context,rarg:RealizeArg)->List[Path]:
      outpaths=realizer(dref,ctx,rarg)
      for key,refpath in config_promises(store_config_(dref),dref):
        for o in outpaths:
          assert_promise_fulfilled(key,refpath,o)
      return outpaths
    return _realizer

  m.builders[dref]=Derivation(dref=dref,
                              matcher=matcher,
                              realizer=_promise_aware(realizer) if check_promises else realizer)
  return dref

#: `PYLIGHTNIX_RECURSION` encodes the state of [recursion
#: manager](#pylightnix.core.recursion_manager), do not modify!
PYLIGHTNIX_RECURSION:Dict[Any,List[str]]={}

@contextmanager
def recursion_manager(funcname:str):
  """ Recursion manager is a helper context manager which detects and prevents
  unwanted recursions. Currently, the following kinds of recursions are catched:

  - `instantiate() -> <config> -> instantiate()`. Instantiate stores Derivation
    in Manager and returns a DRef as a proof that given Manager contains given
    Derivation. Recursive call to instantiate would break this idea by
    introducing nested Managers.
  - `realize() -> <realizer> -> realize()`. Sometimes this recursion is OK,
    but in some cases it may lead to infinite loop, so we deny it completely for now.
  - `realize() -> <realizer> -> instantiate()`. Instantiate produces new DRefs,
    while realize should only work with existing DRefs which form a Closure.
  """
  global PYLIGHTNIX_RECURSION
  if get_ident() not in PYLIGHTNIX_RECURSION:
    PYLIGHTNIX_RECURSION[get_ident()]=[]
  error_msg=(f"Recursion manager alert, during an attempt to call '{funcname}'. "
             f"Contents of the recursion stack: {PYLIGHTNIX_RECURSION[get_ident()]}")
  if funcname=='instantiate':
    assert 'instantiate' not in PYLIGHTNIX_RECURSION[get_ident()], error_msg
  elif funcname=='realize':
    assert 'instantiate' not in PYLIGHTNIX_RECURSION[get_ident()], error_msg
    assert 'realize' not in PYLIGHTNIX_RECURSION[get_ident()], error_msg
  else:
    assert False, f"recursion_manager doesn't contain '{funcname}' rules"
  PYLIGHTNIX_RECURSION[get_ident()].append(funcname)
  try:
    yield ()
  finally:
    del PYLIGHTNIX_RECURSION[get_ident()][-1]

def instantiate_(m:Manager, stage:Any, *args, **kwargs)->Closure:
  with recursion_manager('instantiate'):
    target_dref=stage(m,*args,**kwargs)
    assert_have_realizers(m, [target_dref])
    return Closure(target_dref,list(m.builders.values()))

def instantiate(stage:Any, *args, **kwargs)->Closure:
  """ Instantiate takes the [Stage](#pylightnix.types.Stage) function and
  calculates the [Closure](#pylightnix.types.Closure) of it's
  [Derivations](#pylightnix.types.Derivation).
  All new derivations are added to the storage.
  See also [realizeMany](#pylightnix.core.realizeMany)
  """
  return instantiate_(Manager(), stage, *args, **kwargs)

RealizeSeqGen = Generator[Tuple[DRef,Context,Derivation,RealizeArg],Tuple[Optional[List[RRef]],bool],List[RRef]]

def realize(closure:Closure, force_rebuild:Union[List[DRef],bool]=[],
                             assert_realized:List[DRef]=[])->RRef:
  """ A simplified version of [realizeMany](#pylightnix.core.realizeMany).
  Expects only one output path. """
  rrefs=realizeMany(closure, force_rebuild, assert_realized)
  assert len(rrefs)==1, (
      f"`realize` is to be used with single-output derivations. Derivation "
      f"{closure.dref} has {len(rrefs)} outputs:\n{rrefs}\n"
      f"Consider calling `realizeMany` with it." )
  return rrefs[0]

def realizeMany(closure:Closure, force_rebuild:Union[List[DRef],bool]=[],
                                 assert_realized:List[DRef]=[],
                                 realize_args:Dict[DRef,RealizeArg]={})->List[RRef]:
  """ Obtain one or more realizations of a stage's
  [Closure](#pylightnix.types.Closure).

  If [matching](#pylightnix.types.Matcher) realizations do exist in the
  storage, and if user doesn't ask to forcebly rebuild the stage, `realizeMany`
  returns the references immediately.

  Otherwize, it calls [Realizers](#pylightnix.types.Realizer) of the Closure to
  get desired realizations of the closure top-level derivation.

  Returned value is a list realization references
  [realizations](#pylightnix.types.RRef). Every RRef may be [converted
  to system path](#pylightnix.core.rref2path) of the folder which
  contains build artifacts.

  In order to create each realization, realizeMany moves it's build artifacts
  into the storage by executing `os.replace` function which are assumed to be
  atomic. `realizeMany` also assumes that derivation's config is present in the
  storage at this moment (See e.g. [rmref](#pylightnix.bashlike.rmref))

  Example:
  ```python
  def mystage(m:Manager)->DRef:
    ...
    return mkdrv(m, ...)

  clo:Closure=instantiate(mystage)
  rrefs:List[RRef]=realizeMany(clo)
  print('Available realizations:', [rref2path(rref) for rref in rrefs])
  ```

  `realizeMany` has the following analogs:

  * [realize](#pylightnix.core.realize) - A single-output version
  * [repl_realize](#pylightnix.repl.repl_realize) - A REPL-friendly version
  * [realize_inplace](#pylightnix.inplace.realize_inplace) - A simplified
    version which uses a global derivation Manager.

  - FIXME: Stage's context is calculated inefficiently. Maybe one should track
    dep.tree to avoid calling `store_deepdeps` within the cycle.
  - FIXME: Update derivation's matcher after forced rebuilds. Matchers should
    remember and reproduce user's preferences.
  """
  force_interrupt:List[DRef]=[]
  if isinstance(force_rebuild,bool):
    if force_rebuild:
      force_interrupt=[closure.dref]
  elif isinstance(force_rebuild,list):
    force_interrupt=force_rebuild
  else:
    assert False, "Ivalid type of `force_rebuild` argument"
  try:
    gen=realizeSeq(closure,force_interrupt=force_interrupt,
                           assert_realized=assert_realized,
                           realize_args=realize_args)
    next(gen)
    while True:
      gen.send((None,False)) # Ask for default action
  except StopIteration as e:
    res=e.value
  return res

def realizeSeq(closure:Closure, force_interrupt:List[DRef]=[],
                                assert_realized:List[DRef]=[],
                                realize_args:Dict[DRef,RealizeArg]={})->RealizeSeqGen:
  """ Sequentially realize the closure by issuing steps via Python's generator
  interface. `realizeSeq` encodes low-level details of the realization
  algorithm. Consider calling [realizeMany](#pylightnix.core.realizeMany) or
  it's analogs instead.

  FIXME: `assert_realized` may probably be a implemented by calling `redefine`
  with appropriate failing realizer on every Derivation. """
  assert_valid_closure(closure)
  force_interrupt_:Set[DRef]=set(force_interrupt)
  with recursion_manager('realize'):
    context_acc:Context={}
    target_dref=closure.dref
    target_deps=store_deepdeps([target_dref])
    for drv in closure.derivations:
      dref=drv.dref
      if dref in target_deps or dref==target_dref:
        c=store_config(dref)
        dref_deps=store_deepdeps([dref])
        dref_context={k:v for k,v in context_acc.items() if k in dref_deps}
        if dref in force_interrupt_:
          rrefs,abort=yield (dref,dref_context,drv,realize_args.get(dref,{}))
          if abort:
            return []
        else:
          rrefs=drv.matcher(dref,dref_context)
        if rrefs is None:
          assert dref not in assert_realized, (
            f"Stage '{dref}' was assumed to be already realized. "
            f"Unfortunately, it is not the case. Config:\n"
            f"{store_config(dref)}"
            )
          paths=drv.realizer(dref,dref_context,realize_args.get(dref,{}))
          rrefs_built=[store_realize(dref,dref_context,path) for path in paths]
          rrefs_matched=drv.matcher(dref,dref_context)
          assert rrefs_matched is not None, (
            f"Derivation {dref}: Matcher repeatedly asked the core to "
            f"realize. Probably, realizer doesn't match the matcher. "
            f"In particular, the follwoing just-built rrefs are "
            f"unmatched: {rrefs_built}" )
          if (set(rrefs_built) & set(rrefs_matched)) == set() and \
             (set(rrefs_built) | set(rrefs_matched)) != set():
            print(f"Warning: None of the newly obtained realizations of "
                  f"{dref} were matched by the matcher. To capture those "
                  f"realizations explicitly, try `matcher([exact(..)])`")
          rrefs=rrefs_matched
        context_acc=context_add(context_acc,dref,rrefs)
    assert rrefs is not None
    return rrefs


def mksymlink(rref:RRef, tgtpath:Path, name:str, withtime=True)->Path:
  """ Create a symlink pointing to realization `rref`. Other arguments define
  symlink name and location. Informally,
  `{tgtpath}/{timeprefix}{name} --> $PYLIGHTNIX_STORE/{dref}/{rref}`.
  Overwrite existing symlinks.
  """
  assert_valid_rref(rref)
  assert isdir(tgtpath), f"Target link directory doesn't exist: '{tgtpath}'"
  ts:Optional[str]=store_buildtime(rref) if withtime else None
  timetag=f'{ts}_' if ts is not None else ''
  symlink=Path(join(tgtpath,f'{timetag}{name}'))
  forcelink(Path(relpath(rref2path(rref), tgtpath)), symlink)
  return symlink


#  __  __       _       _
# |  \/  | __ _| |_ ___| |__   ___ _ __ ___
# | |\/| |/ _` | __/ __| '_ \ / _ \ '__/ __|
# | |  | | (_| | || (__| | | |  __/ |  \__ \
# |_|  |_|\__,_|\__\___|_| |_|\___|_|  |___/


def match(keys:List[Key],
          rmin:Optional[int]=1,
          rmax:Optional[int]=1,
          exclusive:bool=False)->Matcher:
  """ Create a [Matcher](#pylightnix.types.Matcher) by combining different
  sorting keys and selecting a top-n threshold.

  Arguments:
  - `keys`: List of [Key](#pylightnix.types.Key) functions. Defaults ot
  - `rmin`: An integer selecting the minimum number of realizations to accept.
    If non-None, Realizer is expected to produce at least this number of
    realizations.
  - `rmax`: An integer selecting the maximum number of realizations to return
    (realizer is free to produce more realizations)
  - `exclusive`: If true, asserts if the number of realizations exceeds `rmax`
  """
  assert (rmin or 0) <= (rmax or maxsize)
  assert not (len(keys)>0 and (rmax is None)), (
    "Specifying non-default sorting keys has no effect without specifying `rmax`.")
  assert not ((rmax is None) and exclusive), (
    "Specifying `exclusive` has no effect without specifying `rmax`.")
  keys=keys+[texthash()]
  def _matcher(dref:DRef, context:Context)->Optional[List[RRef]]:
    keymap={}
    rrefs=list(store_rrefs(dref, context))
    for rref in rrefs:
      keymap[rref]=[k(rref) for k in keys]
    res=sorted(filter(lambda rref: None not in keymap[rref], rrefs),
          key=lambda rref:keymap[rref], reverse=True)
    if rmin is not None:
      if not rmin<=len(res):
        return None
    if rmax is not None:
      if not len(res)<=rmax:
        assert not exclusive
        res=res[:rmax]
    return res
  return _matcher


def latest()->Key:
  def _key(rref:RRef)->Optional[Union[int,float,str]]:
    try:
      with open(join(rref2path(rref),'__buildtime__.txt'),'r') as f:
        t=parsetime(f.read())
        return float(0 if t is None else t)
    except OSError as e:
      return float(0)
  return _key

def exact(expected:List[RRef])->Key:
  def _key(rref:RRef)->Optional[Union[int,float,str]]:
    return 1 if rref in expected else None
  return _key

def best(filename:str)->Key:
  def _key(rref:RRef)->Optional[Union[int,float,str]]:
    try:
      with open(join(rref2path(rref),filename),'r') as f:
        return float(f.readline())
    except OSError as e:
      return float('-inf')
    except ValueError as e:
      return float('-inf')
  return _key


def texthash()->Key:
  def _key(rref:RRef)->Optional[Union[int,float,str]]:
    return str(unrref(rref)[0])
  return _key

def match_n(n:int=1, keys=[])->Matcher:
  """ Return a [Matcher](#pylightnix.types.Matcher) which matchs with any
  number of realizations which is greater or equal than `n`. """
  return match(keys, rmin=n, rmax=n, exclusive=False)

def match_latest(n:int=1)->Matcher:
  return match_n(n, keys=[latest()])

def match_best(filename:str, n:int=1)->Matcher:
  """ Return a [Matcher](#pylightnix.types.Matcher) which checks contexts of
  realizations and then compares them based on stage-specific scores. For each
  realization, score is read from artifact file named `filename` that should
  contain a single float number. Realization with largest score wins.  """
  return match_n(n, keys=[best(filename)])

def match_all()->Matcher:
  """ Return a [Matcher](#pylightnix.types.Matcher) which matchs with **ANY**
  number of realizations, including zero. """
  return match([], rmin=None, rmax=None, exclusive=False)

def match_some(n:int=1)->Matcher:
  """ Return a [Matcher](#pylightnix.types.Matcher) which matchs with any
  number of realizations which is greater or equal than `n`. """
  return match([], rmin=n, rmax=None, exclusive=False)

def match_only()->Matcher:
  """ Return a [Matcher](#pylightnix.types.Matcher) which expects no more than
  one realization for every [derivation](#pylightnix.types.DRef), given the
  [context](#pylightnix.types.Context). """
  return match([], rmin=1, rmax=1, exclusive=True)


#     _                      _
#    / \   ___ ___  ___ _ __| |_ ___
#   / _ \ / __/ __|/ _ \ '__| __/ __|
#  / ___ \\__ \__ \  __/ |  | |_\__ \
# /_/   \_\___/___/\___|_|   \__|___/


def assert_valid_refpath(refpath:RefPath)->None:
  error_msg=(f"Value of type {type(refpath)} is not a valid refpath! Expected "
             f"list of strings starting from a valid DRef string, got '{refpath}'")
  assert len(refpath)>0, error_msg
  assert_valid_dref(refpath[0])

def assert_valid_config(c:Config)->Config:
  assert c is not None, "Expected `Config` object, but None was passed"
  assert_valid_name(config_name(c))
  assert_valid_dict(config_dict(c), 'Config')
  return c

def assert_valid_name(s:Name)->None:
  assert re_match(f"^{PYLIGHTNIX_NAMEPAT}+$", s), \
      f"Expected a name which matches /^{PYLIGHTNIX_NAMEPAT}+$/, got '{s}'."

def assert_valid_rref(ref:str)->None:
  error_msg=(f'Value "{ref}" is not a valid realization reference! Expected '
             f'a string of form \'rref:HASH-HASH-name\'')
  assert isrref(ref), error_msg

def assert_valid_hashpart(hp:HashPart)->None:
  assert len(hp)==32, f"HashPart should have length of 32, but len({hp})=={len(hp)}"
  for s in ['-','_','/']:
    assert s not in hp, f"Invalid symbol '{s}' found in {hp}"

def assert_valid_dref(ref:str)->None:
  error_msg=(f'Value "{ref}" is not a valid derivation reference! Expected '
             f'a string of form \'dref:HASH-name\'')
  assert isdref(ref), error_msg

def assert_valid_hash(h:Hash)->None:
  """ Asserts if it's `Hash` argument is ill-formed. """
  assert len(h)==64, f"HashPart should have length of 64, but len({h})=={len(h)}"
  for s in ['-','_','/']:
    assert s not in h, f"Invalid symbol '{s}' found in {h}"

def assert_valid_context(c:Context)->None:
  assert_serializable(c)
  for dref,rrefs in c.items():
    assert_valid_dref(dref)
    for rref in rrefs:
      assert_valid_rref(rref)

def assert_valid_closure(closure:Closure)->None:
  assert len(closure.derivations)>0, \
      "Closure can not be empty"
  assert closure.dref in [d.dref for d in closure.derivations], \
      "Closure should contain target derivation"

def warn_rref_deps(c:Config)->None:
  _,rrefs=scanref_dict(config_dict(c))
  if len(rrefs)>0:
    print(f"Warning: RRef dependencies were found in config {config_dict(c)}:\n{rrefs}")

# def assert_no_rref_deps(c:RConfig)->None:
#   _,rrefs=scanref_dict(config_dict(c))
#   assert len(rrefs)==0, (
#       f"RRef dependencies are forbidden, but config {config_dict(c)} containes {rrefs}")

def assert_have_realizers(m:Manager, drefs:List[DRef])->None:
  have_drefs=set(m.builders.keys())
  need_drefs=store_deepdeps(drefs)|set(drefs)
  missing=list(need_drefs-have_drefs)
  assert len(missing)==0, (
      f"Some derivations don't have realizers associated with them:\n"
      f"{missing}\n"
      f"Did you take those DRefs from another manager?")

def assert_recursion_manager_empty():
  global PYLIGHTNIX_RECURSION
  stack=PYLIGHTNIX_RECURSION.get(get_ident(),[])
  assert len(stack)==0

