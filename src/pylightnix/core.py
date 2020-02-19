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

from pylightnix.imports import ( sha256, deepcopy, isdir, makedirs, join,
    json_dump, json_load, json_dumps, json_loads, isfile, relpath, listdir,
    rmtree, mkdtemp, replace, environ, split, re_match, ENOTEMPTY, get_ident,
    contextmanager, OrderedDict, lstat, maxsize )
from pylightnix.utils import (
    dirhash, assert_serializable, assert_valid_dict, dicthash, scanref_dict,
    scanref_list, forcelink, timestring, parsetime, datahash, readjson,
    tryread, encode, dirchmod, dirrm, filero )
from pylightnix.types import (
    Dict, List, Any, Tuple, Union, Optional, Iterable, IO, Path, Hash, DRef,
    RRef, RefPath, HashPart, Callable, Context, Name, NamedTuple, Build,
    Config, ConfigAttrs, Derivation, Stage, Manager, Matcher, Realizer, Set,
    Closure, Generator, Key, TypeVar )

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



#   ____             __ _
#  / ___|___  _ __  / _(_) __ _
# | |   / _ \| '_ \| |_| |/ _` |
# | |__| (_) | | | |  _| | (_| |
#  \____\___/|_| |_|_| |_|\__, |
#                         |___/

def mkconfig(d:dict)->Config:
  assert_valid_dict(d,'dict')
  return Config(d)

def config_dict(c:Config)->dict:
  return deepcopy(c.__dict__)

def config_cattrs(c:Config)->Any:
  return ConfigAttrs(config_dict(c))

def config_serialize(c:Config)->str:
  return json_dumps(config_dict(c), indent=4)

def config_hash(c:Config)->Hash:
  return datahash([encode(config_serialize(c))])

def config_name(c:Config)->Name:
  """ Return short human-readable name of a config """
  return mkname(config_dict(c).get('name','unnamed'))

def config_deps(c:Config)->List[DRef]:
  drefs,_=scanref_dict(config_dict(c))
  assert_no_rref_deps(c)
  return list(set(drefs))

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

def store_config(r:Union[DRef,RRef])->Config:
  """ Read the [Config](#pylightnix.types.Config) of the derivatoin referenced by `r`. """
  assert r[:4]=='rref' or r[:4]=='dref', (
      f"Invalid reference type {r}. Expected either RRef or DRef." )
  if r[:4]=='rref':
    return Config(readjson(join(store_dref2path(rref2dref(RRef(r))),'config.json')))
  else:
    return Config(readjson(join(store_dref2path(DRef(r)),'config.json')))

def store_context(r:RRef)->Context:
  assert_valid_rref(r)
  return readjson(join(rref2path(r),'context.json'))

def store_cattrs(r:Union[DRef,RRef])->Any:
  """ Read the [ConfigAttrs](#pylightnix.types.ConfigAttr) of the storage node `r`.
  Note, that it is a kind of 'syntactic sugar' for `store_config`. Both
  functions do the same thing. """
  return config_cattrs(store_config(r))

def store_deps(refs:List[DRef])->List[DRef]:
  """ Return a list of reference's immediate dependencies, not including `refs`
  themselves. """
  acc=set()
  for r in refs:
    acc.update(config_deps(store_config(r)))
  return list(acc)

def store_deepdeps(roots:List[DRef])->Set[DRef]:
  """ Return an exhaustive list of `roots`'s dependencies, not including `roots`
  themselves. """
  frontier=set(store_deps(roots))
  processed=set()
  while frontier:
    ref = frontier.pop()
    processed.add(ref)
    for dep in store_deps([ref]):
      if not dep in processed:
        frontier.add(dep)
  return processed

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
  [context]($pylightnix.types.Context). The sort order is unspecified. """
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

def store_gc(refs_in_use:List[DRef])->List[DRef]:
  """ Take roots which are in use and should not be removed. Return roots which
  are not used and may be removed. Actual removing is to be done by user-defined
  application. """
  assert_store_initialized()
  to_delete=[]
  roots_with_deps=set(store_deepdeps(refs_in_use)) | set(refs_in_use)
  for dref in store_drefs():
    if not dref in roots_with_deps:
      to_delete.append(dref)
  return to_delete


def store_instantiate(c:Config)->DRef:
  """ Place new instantiation into the storage. We attempt to do it atomically
  by moving the directory right into it's place.

  FIXME: Assert or handle possible (but improbable) hash collision (*)
  """
  assert_store_initialized()

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


def mkbuild(dref:DRef, context:Context, buildtime:bool=True)->Build:
  c=store_config(dref)
  assert_valid_config(c)
  timeprefix=timestring()
  cattrs=store_cattrs(dref)
  return Build(dref, cattrs, context, timeprefix, buildtime)

B=TypeVar('B')

def build_wrapper_(
    f:Callable[[B],None],
    buildtime:bool,
    constructor:Callable[[DRef,Context,bool],B],
    outpaths_accessor:Callable[[B],List[Path]])->Realizer:
  def _wrapper(dref,context)->List[Path]:
    b=constructor(dref,context,buildtime); f(b); return outpaths_accessor(b)
  return _wrapper

def build_wrapper(
    f:Callable[[Build],None],
    buildtime:bool=True):
  def _outs(b:Build)->List[Path]:
    return b.outpaths
  return build_wrapper_(f,buildtime,mkbuild,_outs)

def build_config(b:Build)->Config:
  """ Return the [Config](#pylightnix.types.Config) object of the realization
  being built. """
  return store_config(b.dref)

def build_context(b:Build)->Context:
  """ Return the [Context](#pylightnix.types.Context) object of the realization
  being built. """
  return b.context

def build_cattrs(b:Build)->Any:
  return b.cattrs

def build_outpaths(b:Build, nouts:int=1)->List[Path]:
  if len(b.outpaths)==0:
    prefix=f'{b.timeprefix}_{config_hash(build_config(b))[:8]}_'
    outpaths=[Path(mkdtemp(prefix=prefix, dir=PYLIGHTNIX_TMP)) for _ in range(nouts)]
    if b.buildtime:
      for outpath in outpaths:
        with open(join(outpath,'__buildtime__.txt'), 'w') as f:
          f.write(b.timeprefix)
    b.outpaths=outpaths
  assert len(b.outpaths)==nouts, (
      f"Build helper doesn't support changing the number of outputs dynamically. "
      f"This instance has been already initialized with {len(b.outpaths)} outputs, but "
      f"now was asked to return {nouts} outputs")
  return b.outpaths

def build_outpath(b:Build)->Path:
  """ Return the output path of the realization being built. Output path is a
  path to valid temporary folder where user may put various build artifacts.
  Later this folder becomes a realization. """
  paths=build_outpaths(b, nouts=1)
  assert len(paths)==1
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
  """ Return a system path, corresponding to RefPath `refpath`"""
  assert_valid_refpath(refpath)
  return [Path(join(rref2path(path), *refpath[1:])) for path in build_deref_(b, refpath[0])]

def build_path(b:Build, refpath:RefPath)->Path:
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

def mkdrv(m:Manager, config:Config, matcher:Matcher, realizer:Realizer)->DRef:
  assert_valid_config(config)
  dref=store_instantiate(config)
  if dref in m.builders:
    print(f"Overwriting matcher or realizer of derivation {dref}, configured "
          f"as:\n{config_dict(store_config(dref))}")
  m.builders[dref]=Derivation(dref,matcher,realizer)
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
    assert_no_rref_deps(store_config(target_dref))
    assert_have_realizers(m, [target_dref])
    return Closure(target_dref,list(m.builders.values()))

def instantiate(stage:Any, *args, **kwargs)->Closure:
  """ Instantiate takes the [Stage](#pylightnix.types.Stage) function and
  produces calculates the [Closure](#pylightnix.types.Closure) of it's
  [Derivation](#pylightnix.types.Derivation).

  Instantiate's work is somewhat similar to the type-checking in the compiler's
  pipeline.

  User-defined [Instantiators](pylightnix.types.Instantiator) calculate stage
  configs during the instantiation. This calculations fall under certain
  restrictions. In particular, it shouldn't start new instantiations or
  realizations recursively, and it shouldn't access stage realizations in the
  storage.

  New derivations are added to the storage by moving a temporary folder inside
  the storage folder.
  """
  return instantiate_(Manager(), stage, *args, **kwargs)

RealizeSeqGen = Generator[Tuple[DRef,Context,Derivation],Tuple[Optional[List[RRef]],bool],List[RRef]]

def realize(closure:Closure, force_rebuild:List[DRef]=[])->RRef:
  """ A simplified version of [realizeMany](#pylightnix.core.realizeMany).
  Expects only one result. """
  rrefs=realizeMany(closure, force_rebuild)
  assert len(rrefs)==1, (
      f"realize is to be used with single-output derivations, but derivation "
      f"{closure.dref} has {len(rrefs)} outputs:\n{rrefs}\n"
      f"Consider using `realizeMany`." )
  return rrefs[0]

def realizeMany(closure:Closure, force_rebuild:List[DRef]=[])->List[RRef]:
  """ Obtain one or many realizations of a stage's
  [Closure](#pylightnix.types.Closure).

  If [matching](#pylightnix.types.Matcher) realizations do exist in the storage,
  and user doesn't ask for rebuild, realizeMany returns immediately.

  Otherwize, it calls one or many [Realizers](#pylightnix.types.Realizer) to
  get the desiared realizations.

  Returned value is a list references to new
  [realizations](#pylightnix.types.RRef). Every realization may be [converted
  to system path](#pylightnix.core.rref2path) pointing to the folder which
  contains build artifacts.

  To create each new realization, realizeMany moves it's build artifacts inside
  the storage by executing `os.replace` function which are meant to be atomic.
  `realizeMany` assumes that derivation's config is present in the storage at
  the moment of replacing (See e.g. [rmref](#pylightnix.bashlike.rmref))

  - FIXME: Stage's context is calculated inefficiently. Maybe one should track
    dep.tree to avoid calling `store_deepdeps` within the cycle.
  - FIXME: Update derivation's matcher after forced rebuilds. Matchers should
    remember and reproduce user's preferences.
  """
  try:
    gen=realizeSeq(closure,force_interrupt=force_rebuild)
    next(gen)
    while True:
      gen.send((None,False)) # Ask for default action
  except StopIteration as e:
    res=e.value
  return res

def realizeSeq(closure:Closure, force_interrupt:List[DRef]=[])->RealizeSeqGen:
  """ Sequentially realize the closure by issuing steps via Python's generator
  interface """
  assert_valid_closure(closure)
  force_interrupt_:Set[DRef]=set(force_interrupt)
  with recursion_manager('realize'):
    context:Context={}
    target_dref=closure.dref
    target_deps=store_deepdeps([target_dref])
    for drv in closure.derivations:
      dref=drv.dref
      if dref in target_deps or dref==target_dref:
        c=store_config(dref)
        dref_deps=store_deepdeps([dref])
        dref_context={k:v for k,v in context.items() if k in dref_deps}
        if dref in force_interrupt_:
          rrefs,abort=yield (dref,dref_context,drv)
          if abort:
            return []
        else:
          rrefs=drv.matcher(dref,dref_context)
        if rrefs is None:
          paths=drv.realizer(dref,context)
          rrefs_built=[store_realize(dref,context,path) for path in paths]
          rrefs_matched=drv.matcher(dref,context)
          assert rrefs_matched is not None, (
            f"Derivation {dref}: Matcher repeatedly asked the core to "
            "realize. Probably, realizer doesn't match the matcher" )
          if (set(rrefs_built) & set(rrefs_matched)) == set() and \
             (set(rrefs_built) | set(rrefs_matched)) != set():
            print(f"Warning: None of the newly obtained realizations of "
                  f"{dref} were matched by the matcher. To capture those "
                  f"realizations explicitly, try `matcher([exact(..)])`")
          rrefs=rrefs_matched
        context=context_add(context,dref,rrefs)
    assert rrefs is not None
    return rrefs

def mksymlink(rref:RRef, tgtpath:Path, name:str, withtime=True)->Path:
  """ Create a symlink pointing to realization `rref`. Other arguments define
  symlink name and location. Informally,
  `{tgtpath}/{timeprefix}{name} --> $PYLIGHTNIX_STORE/{rref2dref(rref)}/{rref}` """
  assert_valid_rref(rref)
  assert isdir(tgtpath), f"store_link(): `tgt` dir '{tgtpath}' doesn't exist"
  ts:Optional[str]
  if withtime:
    ts=tryread(Path(join(rref2path(rref),'__buildtime__.txt')))
  else:
    ts=None
  timeprefix=f'{ts}_' if ts is not None else ''
  symlink=Path(join(tgtpath,f'{timeprefix}{name}'))
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
  """ Create a matcher by combining different sorting keys and selecting a
  top-n threshold.

  Parameters:
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

def assert_valid_config(c:Config):
  assert c is not None, "Expected `Config` object, but None was passed"
  assert_valid_name(config_name(c))
  assert_valid_dict(c.__dict__, 'Config')

def assert_valid_name(s:Name)->None:
  assert re_match(f"^{PYLIGHTNIX_NAMEPAT}+$", s), \
      f"Expected a name which matches /^{PYLIGHTNIX_NAMEPAT}+$/, got '{s}'."

def isrref(ref:str)->bool:
  return len(ref)>5 and ref[:5]=='rref:'

def assert_valid_rref(ref:str)->None:
  error_msg=(f'Value of {ref} is not a valid instance reference! Expected '
             f'a string of form \'dref:HASH-HASH-name\'')
  assert isrref(ref), error_msg

def assert_valid_hashpart(hp:HashPart)->None:
  assert len(hp)==32, f"HashPart should have length of 32, but len({hp})=={len(hp)}"
  for s in ['-','_','/']:
    assert s not in hp, f"Invalid symbol '{s}' found in {hp}"

def isdref(ref:str)->bool:
  return len(ref)>0 and ref[:5]=='dref:'

def assert_valid_dref(ref:str)->None:
  error_msg=(f'Value of {ref} is not a valid derivation reference! Expected '
             f'a string of form \'dref:HASH_HASH-name\'')
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

def assert_no_rref_deps(c:Config)->None:
  _,rrefs=scanref_dict(config_dict(c))
  assert len(rrefs)==0, (
      f"RRef dependencies are forbidden, but config {config_dict(c)} containes {rrefs}")

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

