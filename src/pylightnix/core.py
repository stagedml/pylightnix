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

from pylightnix.imports import (sha256, deepcopy, isdir, islink, makedirs,
                                join, json_dump, json_load, json_dumps,
                                json_loads, isfile, relpath, listdir, rmtree,
                                mkdtemp, replace, environ, split, re_match,
                                ENOTEMPTY, get_ident, contextmanager,
                                OrderedDict, lstat, maxsize, readlink, chain,
                                getLogger, scandir)

from pylightnix.utils import (dirhash, assert_serializable, assert_valid_dict,
                              dicthash, scanref_dict, scanref_list, forcelink,
                              timestring, parsetime, datahash, readjson,
                              tryread, encode, dirchmod, dirrm, filero, isrref,
                              isdref, traverse_dict, tryread_def,
                              tryreadjson_def, isrefpath, kahntsort, dagroots,
                              isselfpath)

from pylightnix.types import (Dict, List, Any, Tuple, Union, Optional,
                              Iterable, IO, Path, SPath, Hash, DRef, RRef,
                              RefPath, HashPart, Callable, Context, Name,
                              NamedTuple, Build, RConfig, ConfigAttrs,
                              Derivation, Stage, Manager, Matcher, Realizer,
                              Set, Closure, Generator, BuildArgs, Config,
                              RealizeArg, InstantiateArg, PYLIGHTNIX_SELF_TAG,
                              Output, EquivClasses, TypeVar, PromiseException)

logger=getLogger(__name__)
info=logger.info
warning=logger.warning

#: *Do not change!*
#: Tracks the version of pylightnix storage
PYLIGHTNIX_STORE_VERSION=0

def storagename():
  return f"store-v{PYLIGHTNIX_STORE_VERSION}"

#: `PYLIGHTNIX_ROOT` contains the path to the root of pylightnix shared data folder.
#:
#: Default is `~/_pylightnix` or `/var/run/_pylightnix` if no `$HOME` is available.
#: Setting `PYLIGHTNIX_ROOT` environment variable overwrites the defaults.
PYLIGHTNIX_ROOT=environ.get('PYLIGHTNIX_ROOT',
  join(environ.get('HOME','/var/run'), '_pylightnix'))


#: `PYLIGHTNIX_TMP` contains the path to the root of temporary folders.
#: Setting `PYLIGHTNIX_TMP` environment variable overwrites the default value of
#: `$PYLIGHTNIX_ROOT/tmp`.
PYLIGHTNIX_TMP=environ.get('PYLIGHTNIX_TMP', join(PYLIGHTNIX_ROOT,'tmp'))

def tempdir(tmp:Optional[Path]=None)->Path:
  if tmp is None:
    assert isinstance(PYLIGHTNIX_TMP, str), \
      f"Default temp folder location is not a string: {PYLIGHTNIX_TMP}"
    return Path(PYLIGHTNIX_TMP)
  else:
    return tmp

#: `PYLIGHTNIX_STORE` contains the path to the main pylightnix store folder.
#:
#: By default, the store is located in `$PYLIGHTNIX_ROOT/store-vXX` folder.
#: Setting `PYLIGHTNIX_STORE` environment variable overwrites the defaults.
PYLIGHTNIX_STORE=join(PYLIGHTNIX_ROOT, storagename())

def storage(S:Optional[SPath]=None)->SPath:
  """ Returns the location to Pylightnix storage, defaulting to
  PYLIGHTNIX_STORE """
  if S is None:
    assert isinstance(PYLIGHTNIX_STORE, str), \
      f"Default storage location is not a string: {PYLIGHTNIX_STORE}"
    return SPath(PYLIGHTNIX_STORE)
  else:
    return S

#: Set the regular expression pattern for valid name characters.
PYLIGHTNIX_NAMEPAT="[a-zA-Z0-9_-]"

#: Reserved file names are treated specially be the core. Users should
#: not normally create or alter files with this names.
PYLIGHTNIX_RESERVED=['context.json','group.json']

def reserved(folder:Path, name:str)->Path:
  assert name in PYLIGHTNIX_RESERVED, \
    f"File name '{name}' expected to be reserved"
  return Path(join(folder,name))

selfref = PYLIGHTNIX_SELF_TAG

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

def path2dref(p:Path)->Optional[DRef]:
  """ Takes either a system path of some realization in the Pylightnix storage
  or a symlink pointing to such path. Return a `DRef` which corresponds to this
  path.

  Note: `path2dref` operates on `p` symbolically. It doesn't actually check the
  presence of such an object in storage """
  if islink(p):
    p=Path(readlink(p))
  _,dref_part=split(p)
  dref=DRef('dref:'+dref_part)
  return dref if isdref(dref) else None

def path2rref(p:Path)->Optional[RRef]:
  """ Takes either a system path of some realization in the Pylightnix storage
  or a symlink pointing to such path. Return `RRef` which corresponds to this
  path.

  Note: `path2rref` operates on `p` symbolically. It doesn't actually check the
  presence of such an object in storage """
  if islink(p):
    p=Path(readlink(p))
  head,h1=split(p)
  _,dref_part=split(head)
  dref=DRef('dref:'+dref_part)
  if not isdref(dref):
    return None
  h2,nm=undref(dref)
  return mkrref(HashPart(h1),HashPart(h2),mkname(nm))

#   ____             __ _
#  / ___|___  _ __  / _(_) __ _
# | |   / _ \| '_ \| |_| |/ _` |
# | |__| (_) | | | |  _| | (_| |
#  \____\___/|_| |_|_| |_|\__, |
#                         |___/


def mkconfig(d:dict)->Config:
  """ Create Config object out of config dictionary. Asserts if the dictionary
  is not JSON-compatible. As a handy hack, filter out `m:Manager` variable
  which likely is an utility [Manager](#pylightnix.types.Manager) object.

  FIXME: Should we assert on invalid Config here?
  """
  return Config(assert_valid_dict(
    {k:v for k,v in d.items()
     if not (k=='m' and 'Manager' in str(type(v)))},'dict'))

def config_dict(cp:Config)->dict:
  return deepcopy(cp.val)

def config_cattrs(c:RConfig)->Any:
  return ConfigAttrs(config_dict(c))

def config_serialize(c:Config)->str:
  return json_dumps(config_dict(c), indent=4)

def config_hash(c:Config)->Hash:
  return datahash([(config_name(c),encode(config_serialize(c)))])

def config_name(c:Config)->Name:
  """ Return short human-readable name of a config """
  return mkname(config_dict(c).get('name','unnamed'))

def config_deps(c:Config)->Set[DRef]:
  drefs,_=scanref_dict(config_dict(c))
  return set(drefs)

def mkrefpath(r:DRef, items:List[str]=[])->RefPath:
  """ Construct a [RefPath](#pylightnix.types.RefPath) out of a reference `ref`
  and a path within the stage's realization """
  assert_valid_dref(r)
  return [str(r)]+items


#  ____  _
# / ___|| |_ ___  _ __ ___
# \___ \| __/ _ \| '__/ _ \
#  ___) | || (_) | | |  __/
# |____/ \__\___/|_|  \___|

def assert_initialized(S:SPath)->None:
  assert isdir(storage(S)), \
    (f"Looks like the Pylightnix store ('{PYLIGHTNIX_STORE}') is not initialized. Did "
     f"you call `initialize`?")
  assert isdir(tempdir()), \
    (f"Looks like the Pylightnix tmp ('{tempdir()}') is not initialized. Did "
     f"you call `initialize`?")
  assert lstat((storage(S))).st_dev == lstat(tempdir()).st_dev, \
    (f"Looks like Pylightnix store and tmp directories belong to different filesystems. "
     f"This case is not supported yet. Consider setting PYLIGHTNIX_TMP to be on the same "
     f"device with PYLIGHTNIX_STORE")

def initialize(custom_store:Optional[str]=None,
                     custom_tmp:Optional[str]=None,
                     check_not_exist:bool=False)->None:
  """ Create the storage and temp direcories if they don't exist. Default
  locations are determined by `PYLIGHTNIX_STORE` and `PYLIGHTNIX_TMP` global
  variables which in turn may be set by either setting environment variables of
  the same name or by direct assigning.

  Parameters:
  - `custom_store:Optional[str]=None`: If not None, create new storage located
    here.
  - `custom_tmp:Optional[str]=None`: If not None, set the temp files directory
    here.
  - `check_not_exist:bool=False`: Set to True to assert on already existing
    storages. Good to become sure that newly created storage is empty.

  See also [assert_initialized](#pylightnix.core.assert_initialized).

  Example:
  ```python
  import pylightnix.core
  pylightnix.core.PYLIGHTNIX_STORE='/tmp/custom_pylightnix_storage'
  pylightnix.core.PYLIGHTNIX_TMP='/tmp/custom_pylightnix_tmp'
  pylightnix.core.initialize()
  ```
  """
  global PYLIGHTNIX_STORE, PYLIGHTNIX_TMP

  if custom_store is not None:
    PYLIGHTNIX_STORE=custom_store
  info(f"Initializing {'' if isdir(PYLIGHTNIX_STORE) else 'non-'}existing "
       f"{PYLIGHTNIX_STORE}")
  makedirs(PYLIGHTNIX_STORE, exist_ok=False if check_not_exist else True)

  if custom_tmp is not None:
    PYLIGHTNIX_TMP=custom_tmp
  makedirs(PYLIGHTNIX_TMP, exist_ok=True)

  assert_initialized(SPath(PYLIGHTNIX_STORE))


def resolve(c:Config, r:DRef)->RConfig:
  """ Replace all Promise tags with DRef `r`. In particular, all PromisePaths
  are converted into RefPaths. """
  d=config_dict(c)
  def _mut(k:Any,val:Any):
    if isselfpath(val):
      return [DRef(r)]+val[1:]
    else:
      return val
  traverse_dict(d,_mut)
  return RConfig(d)


def dref2path(r:DRef,S=None)->Path:
  (dhash,nm)=undref(r)
  return Path(join(storage(S),dhash+'-'+nm))

def rref2path(r:RRef, S=None)->Path:
  (rhash,dhash,nm)=unrref(r)
  return Path(join(storage(S),dhash+'-'+nm,rhash))

def drefcfgpath(r:DRef,S=None)->Path:
  return Path(join(dref2path(r,S),'config.json'))

def rrefctx(r:RRef, S=None)->Context:
  assert_valid_rref(r)
  return readjson(join(rref2path(r,S),'context.json'))


def drefcfg_(r:DRef,S=None)->Config:
  return assert_valid_config(Config(readjson(drefcfgpath(r,S))))

def drefcfg(r:DRef,S=None)->RConfig:
  return resolve(drefcfg_(r,S),r)

def drefattrs(r:DRef, S=None)->Any:
  """ Read the [ConfigAttrs](#pylightnix.types.ConfigAttr) of the storage node `r`.
  Note, that it is a kind of 'syntactic sugar' for `drefcfg`. Both
  functions do the same thing. """
  return config_cattrs(drefcfg(r,S))

def rrefattrs(r:RRef, S=None)->Any:
  """ Read the [ConfigAttrs](#pylightnix.types.ConfigAttr) of the storage node `r`.
  Note, that it is a kind of 'syntactic sugar' for `drefcfg`. Both
  functions do the same thing. """
  return drefattrs(rref2dref(r),S)

def drefdeps1(drefs:Iterable[DRef],S=None)->Set[DRef]:
  """ Return a list of reference's immediate dependencies, not including `drefs`
  themselves. """
  acc=set()
  for dref in drefs:
    acc.update(config_deps(drefcfg_(dref,S)))
  return acc

def rrefdeps1(rrefs:Iterable[RRef],S=None)->Set[RRef]:
  acc=set()
  for rref in rrefs:
    dref=rref2dref(rref)
    for dref_dep in drefdeps1([dref],S):
      acc|=set(context_deref(rrefctx(rref,S),dref_dep))
  return acc

def drefdeps(drefs:Iterable[DRef], S=None)->Set[DRef]:
  """ Return the complete set of `drefs`'s dependencies, not including `drefs`
  themselves. """
  frontier=drefdeps1(drefs,S)
  processed=set()
  while frontier:
    ref = frontier.pop()
    processed.add(ref)
    for dep in drefdeps1([ref],S):
      if dep not in processed:
        frontier.add(dep)
  return processed

def rrefdeps(rrefs:Iterable[RRef],S=None)->Set[RRef]:
  """ Return the complete set of rrefs's dependencies, not including `rrefs`
  themselves.

  TODO: Validate the property that the resulting set IS the minimal complete
  set of RRef dependencies. Now it looks so only by creation (see `realizeSeq`,
  line mark `I`)
  """
  acc:Set=set()
  for rref in rrefs:
    for rref_deps in rrefctx(rref,S).values():
      acc|=set(rref_deps)
  return acc

def alldrefs(S=None)->Iterable[DRef]:
  """ Iterates over all derivations of the storage located at `S`
  (PYLIGHTNIX_STORE env is used by default) """
  store_path_=storage(S)
  for dirname in listdir(store_path_):
    if dirname[-4:]!='.tmp' and isdir(join(store_path_,dirname)):
      yield mkdref(HashPart(dirname[:32]), Name(dirname[32+1:]))

def allrrefs(S=None)->Iterable[RRef]:
  """ Iterates over all realization references in `S` (PYLIGHTNIX_STORE env is
  used by default) """
  for dref in alldrefs(S):
    for rref in drefrrefs(dref,S):
      yield rref

def rootdrefs(S:Optional[SPath]=None)->Set[DRef]:
  """ Return root DRefs of the storage `S` as a set """
  def _inb(x):
    return drefdeps1([x],S)
  topsorted=kahntsort(alldrefs(S), _inb)
  assert topsorted is not None, (
    f"Falied to topologically sort the derivations of {S}. This "
    f"probably means that the storage is damaged")
  return dagroots(topsorted, _inb)

def rootrrefs(S:Optional[SPath]=None)->Set[RRef]:
  """ Return root RRefs of the storage `S` as a set """
  def _inb(x):
    return rrefdeps1([x],S)
  topsorted=kahntsort(allrrefs(S), _inb)
  assert topsorted is not None, (
    f"Falied to topologically sort the realizations of {S}. This "
    f"probably means that the storage is damaged")
  return dagroots(topsorted, _inb)

def rrefdata(rref:RRef,S=None)->Iterable[Path]:
  """ Iterate over top-level artifacts paths, ignoring reserved files. """
  root=rref2path(rref,S)
  for fd in scandir(root):
    if not (fd.is_file() and fd.name in PYLIGHTNIX_RESERVED):
      yield Path(join(root, fd.name))

def drefrrefs(dref:DRef,S=None)->List[RRef]:
  """ Iterate over all realizations of a derivation `dref`. The sort order is
  unspecified. Matchers are not taken into account. """
  (dhash,nm)=undref(dref)
  drefpath=dref2path(dref,S)
  rrefs:List[RRef]=[]
  for f in listdir(drefpath):
    if f[-4:]!='.tmp' and isdir(join(drefpath,f)):
      rrefs.append(mkrref(HashPart(f), dhash, nm))
  return rrefs

def drefrrefsC(dref:DRef, context:Context, S=None)->Iterable[RRef]:
  """ Iterate over realizations of a derivation `dref` that match a specified
  [context](#pylightnix.types.Context). Sorting order is unspecified. """
  for rref in drefrrefs(dref,S):
    context2=rrefctx(rref,S)
    if context_eq(context,context2):
      yield rref

def rrefbtime(rref:RRef, S=None)->Optional[str]:
  """ Return the buildtime of the current RRef in a format specified by the
  [PYLIGHTNIX_TIME](#pylightnix.utils.PYLIGHTNIX_TIME) constant.

  [parsetime](#pylightnix.utils.parsetime) may be used to parse stings into
  UNIX-Epoch seconds.

  Buildtime is the time when the realization process has started. Some
  realizations may not provide this information. """
  return tryread(Path(join(rref2path(rref,S),'__buildtime__.txt')))

def store_gc(keep_drefs:List[DRef],
             keep_rrefs:List[RRef],
             S:SPath)->Tuple[Set[DRef],Set[RRef]]:
  """ Take roots which are in use and should not be removed. Return roots which
  are not used and may be removed. Actual removing is to be done by the user.

  Default location of `S` may be changed.

  See also [rmref](#pylightnix.bashlike.rmref)"""
  assert_initialized(S)
  keep_rrefs_=set(keep_rrefs)
  keep_drefs_=set(keep_drefs)
  closure_rrefs=rrefdeps(keep_rrefs_,S) | keep_rrefs_
  closure_drefs=drefdeps(keep_drefs_,S) | keep_drefs_ | {rref2dref(rref) for rref in closure_rrefs}
  remove_drefs=set()
  remove_rrefs=set()
  for dref in alldrefs(S):
    if dref not in closure_drefs:
      remove_drefs.add(dref)
    for rref in drefrrefs(dref,S):
      if rref not in closure_rrefs:
        remove_rrefs.add(rref)
  return remove_drefs,remove_rrefs


def mkdrv_(c:Config,S:SPath)->DRef:
  """ Create new derivation in storage `S`.

  We attempt to do it atomically by creating temp directory first and then
  renaming it right into it's place in the storage.

  FIXME: Assert or handle possible (but improbable) hash collision [*]
  """
  assert_initialized(S)
  # c=cp.config
  assert_valid_config(c)
  assert_rref_deps(c)

  refname=config_name(c)
  dhash=config_hash(c)

  dref=mkdref(trimhash(dhash),refname)

  o=Path(mkdtemp(prefix=refname, dir=tempdir()))
  with open(join(o,'config.json'), 'w') as f:
    f.write(config_serialize(c))

  filero(Path(join(o,'config.json')))
  drefpath=dref2path(dref,S)
  dreftmp=Path(drefpath+'.tmp')
  replace(o,dreftmp)

  try:
    replace(dreftmp, drefpath)
  except OSError as err:
    if err.errno == ENOTEMPTY:
      # Existing folder means that it has a matched content [*]
      dirrm(dreftmp, ignore_not_found=False)
    else:
      raise
  return dref

def mkrealization(dref:DRef, l:Context, o:Path, S=None)->RRef:
  """ Create the [Realization](#pylightnix.types.RRef) object in the storage
  `S`. Return new Realization reference.

  Parameters:
  - `dref:DRef`: Derivation reference to create the realization of.
  - `l:Context`: Context which stores dependency information.
  - `o:Path`: Path to temporal (build) folder which contains artifacts,
    prepared by the [Realizer](#pylightnix.types.Realizer).
  - `leader`: Tag name and Group identifier of the Group leader. By default,
    we use name `out` and derivation's own rref.

  FIXME: Assert or handle possible but improbable hash collision[*]
  """
  assert_valid_config(drefcfg_(dref,S))
  (dhash,nm)=undref(dref)

  assert isdir(o), (
   f"While realizing {dref}: Outpath is expected to be a path to existing "
   f"directory, but got {o}")

  for fn in PYLIGHTNIX_RESERVED:
    assert not isfile(join(o,fn)), (
      f"While realizing {dref}: output folder '{o}' contains file '{fn}'. "
      f"This name is reserved, please use another name. List of reserved "
      f"names: {PYLIGHTNIX_RESERVED}")

  with open(reserved(o,'context.json'), 'w') as f:
    f.write(context_serialize(l))

  rhash=dirhash(o)
  rref=mkrref(trimhash(rhash),dhash,nm)
  rrefpath=rref2path(rref,S)
  rreftmp=Path(rrefpath+'.tmp')

  replace(o,rreftmp)
  dirchmod(rreftmp,'ro')

  try:
    replace(rreftmp,rrefpath)
  except OSError as err:
    if err.errno == ENOTEMPTY:
      # Folder name contain the hash of the content, so getting here
      # probably[*] means that we already have this object in storage so we
      # just remove temp folder.
      dirrm(rreftmp, ignore_not_found=False)
    else:
      # Attempt to roll-back
      dirchmod(rreftmp,'rw')
      replace(rreftmp,o)
      raise
  return rref

#   ____            _            _
#  / ___|___  _ __ | |_ _____  _| |_
# | |   / _ \| '_ \| __/ _ \ \/ / __|
# | |__| (_) | | | | ||  __/>  <| |_
#  \____\___/|_| |_|\__\___/_/\_\\__|


def mkcontext()->Context:
  return {}


def context_eq(a:Context,b:Context)->bool:
  return json_dumps(a)==json_dumps(b)


def context_add(ctx:Context, dref:DRef, rrefs:List[RRef])->Context:
  assert dref not in ctx, (
    f"Attempting to re-introduce DRef {dref} to context with a "
    f"different realization.\n"
    f" * Old realization: {ctx[dref]}\n"
    f" * New realization: {rrefs}\n")
  return dict(sorted([(dref,list(sorted(rrefs)))]+list(ctx.items())))


def context_deref(context:Context, dref:DRef)->List[RRef]:
  assert dref in context, (
    f"Context {context} doesn't declare {dref} among it's dependencies so we "
    f"can't dereference it.")
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



def mkdrv(m:Manager,
          config:Config,
          matcher:Matcher,
          realizer:Realizer)->DRef:
  """ Run the instantiation of a particular stage. Create a
  [Derivation](#pylightnix.types.Derivation) object out of three main
  components: the Derivation reference, the Matcher and the Realizer. Register
  the derivation in a [Manager](#pylightnix.types.Manager) to aid dependency
  resolution. Return [Derivation reference](#pylightnix.types.DRef) of the
  derivation produced.

  Arguments:
  - `m:Manager`: A Manager to update with a new derivation

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
  dref=mkdrv_(config,m.storage)
  if dref in m.builders:
    if not m.in_redefine:
      warning((f"Overwriting either the matcher or the realizer of derivation "
               f"'{dref}'. It could be intended (e.g. a result of `redefine`), "
               f"but now we see a different situation. Could it be  "
               f"a recursive call to `instantiate`?\n"
               f"Derivation config:\n{drefcfg_(dref,m.storage)}"))
  m.builders[dref]=Derivation(dref=dref, matcher=matcher, realizer=realizer)
  return dref

def instantiate_(m:Manager, stage:Any, *args, **kwargs)->Closure:
  assert not m.in_instantiate, (
    "Recursion detected. `instantiate` should not be called recursively "
    "by stage functions with the same `Manager` as argument")
  m.in_instantiate=True
  try:
    target_dref=stage(m,*args,**kwargs)
  finally:
    m.in_instantiate=False
  assert_have_realizers(m,[target_dref])
  return Closure(target_dref,list(m.builders.values()),m.storage)

def instantiate(stage:Any, *args, S=None, **kwargs)->Closure:
  """ Instantiate takes the [Stage](#pylightnix.types.Stage) function and
  calculates the [Closure](#pylightnix.types.Closure) of it's
  [Derivations](#pylightnix.types.Derivation).
  All new derivations are added to the storage.
  See also [realizeMany](#pylightnix.core.realizeMany)
  """
  return instantiate_(Manager(storage(S)), stage, *args, **kwargs)


RealizeSeqGen = Generator[Tuple[SPath,DRef,Context,Derivation,RealizeArg],
                          Tuple[Optional[Output[RRef]],bool],
                          Output[RRef]]


def realize(closure:Closure, force_rebuild:Union[List[DRef],bool]=[],
                             assert_realized:List[DRef]=[])->RRef:
  """ A simplified version of [realizeMany](#pylightnix.core.realizeMany).
  Expects only one output path. """
  rrefs=realizeMany(closure, force_rebuild, assert_realized)
  assert len(rrefs)==1, (
      f"`realize` is to be used with single-output derivations. Derivation "
      f"{closure.dref} has {len(rrefs)} outputs:\n{rrefs}\n"
      f"Consider using `realizeMany` or `realizeGroups`." )
  return rrefs[0]


def realizeMany(closure:Closure,
                force_rebuild:Union[List[DRef],bool]=[],
                assert_realized:List[DRef]=[],
                realize_args:Dict[DRef,RealizeArg]={})->List[RRef]:
  """ Obtain one or more [Closure](#pylightnix.types.Closure) realizations of a
  stage.

  The function returns [matching](#pylightnix.types.Matcher) realizations
  immediately if they are exist.

  Otherwize, a number of [Realizers](#pylightnix.types.Realizer) are called.

  Example:
  ```python
  def mystage(m:Manager)->DRef:
    ...
    return mkdrv(m, ...)

  clo:Closure=instantiate(mystage)
  rrefgs:List[RRefGroup]=realizeGroups(clo)
  print([mklen(rref).syspath for grp[tag_out()] in rrefgs])
  ```

  Pylightnix contains the following alternatives to `realizeMany`:

  * [realize](#pylightnix.core.realize) - A single-output version
  * [repl_realize](#pylightnix.repl.repl_realize) - A REPL-friendly version
  * [realize_inplace](#pylightnix.inplace.realize_inplace) - A simplified
    version which uses a global derivation Manager.

  - FIXME: Stage's context is calculated inefficiently. Maybe one should track
    dep.tree to avoid calling `drefdeps` within the cycle.
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
    gen=realizeSeq(closure, force_interrupt, assert_realized, realize_args)
    next(gen)
    while True:
      gen.send((None,False)) # Ask for default action
  except StopIteration as e:
    res=e.value
  return res.val


def realizeSeq(closure:Closure,
               force_interrupt:List[DRef]=[],
               assert_realized:List[DRef]=[],
               realize_args:Dict[DRef,RealizeArg]={}
               )->RealizeSeqGen:
  """ Sequentially realize the closure by issuing steps via Python's generator
  interface. `realizeSeq` encodes low-level details of the realization
  algorithm. Consider calling [realizeMany](#pylightnix.core.realizeMany) or
  it's analogs instead.

  FIXME: `assert_realized` may probably be implemented by calling `redefine`
  with appropriate failing realizer on every Derivation. """
  S=closure.storage
  assert_valid_closure(closure)
  force_interrupt_:Set[DRef]=set(force_interrupt)
  context_acc:Context={}
  target_dref=closure.dref
  target_deps=drefdeps([target_dref],S)
  for drv in closure.derivations:
    dref=drv.dref
    rrefs:Optional[Output[RRef]]
    if dref in target_deps or dref==target_dref:
      dref_deps=drefdeps([dref],S)
      dref_context={k:v for k,v in context_acc.items() if k in dref_deps} # I
      if dref in force_interrupt_:
        rrefs,abort=yield (S,dref,dref_context,drv,realize_args.get(dref,{}))
        if abort:
          return Output([])
      else:
        rrefs=drv.matcher(S, Output(drefrrefsC(dref,dref_context,S)))
      if rrefs is None:
        assert dref not in assert_realized, (
          f"Stage '{dref}' was assumed to be already realized. "
          f"Unfortunately, it is not the case. Config:\n"
          f"{drefcfg_(dref)}")
        rrefs_existed=drefrrefsC(dref,dref_context,S)
        rpaths:List[Path]=drv.realizer(S,dref,dref_context,realize_args.get(dref,{})).val
        rrefs_built:List[RRef]=[mkrealization(dref,dref_context,rp,S) for rp in rpaths]
        if len(rpaths)!=len(set(rrefs_built)):
          warning(f"Realizer of {dref} produced duplicated realizations")
        rrefs_matched=drv.matcher(S,Output(drefrrefsC(dref,dref_context,S)))
        assert rrefs_matched is not None, (
          f"The matcher of {dref} is not satisfied with its realizatons. "
          f"The following newly obtained realizations were ignored:\n"
          f"  {rrefs_built}\n"
          f"The following realizations already existed:\n"
          f"  {rrefs_existed}")
        if (set(rrefs_built) & set(rrefs_matched.val)) == set() and \
           (set(rrefs_built) | set(rrefs_matched.val)) != set():
          warning(f"None of the newly obtained {dref} realizations "
                  f"were matched by the matcher. To capture those "
                  f"realizations explicitly, try `matcher([exact(..)])`")
        rrefs=rrefs_matched
      assert rrefs is not None
      context_acc=context_add(context_acc,dref,rrefs.val)
  assert rrefs is not None
  return rrefs


def evaluate(stage, *args, **kwargs)->RRef:
  return realize(instantiate(stage,*args,**kwargs))


def linkrref(rref:RRef,
             destdir:Optional[Path]=None,
             name:Optional[str]=None,
             withtime:bool=False,
             S=None)->Path:
  """ linkkrref creates a symbolic link to a particular realization reference.
  The new link appears in the `destdir` directory if this argument is not None,
  otherwise the current directory is used.

  Informally,
  `{tgtpath}/{timeprefix}{name} --> $PYLIGHTNIX_STORE/{dref}/{rref}`.
  The function overwrites existing symlinks.
  """
  destdir_='.' if destdir is None else destdir
  name_:str=name if name is not None else (
    '_result-'+config_name(drefcfg_(rref2dref(rref),S)) if destdir is None else
    'result-'+config_name(drefcfg_(rref2dref(rref),S)))
  ts:Optional[str]=rrefbtime(rref,S) if withtime else None
  timetag_=f'{ts}_' if ts is not None else ''
  symlink=Path(join(destdir_,f"{timetag_}{name_}"))
  forcelink(Path(relpath(rref2path(rref,S), destdir_)), symlink)
  return symlink


def linkdref(dref:DRef,
             destdir:Optional[Path]=None,
             name:Optional[str]=None,
             S=None)->Path:
  destdir_='.' if destdir is None else destdir
  name_:str=name if name is not None else (
    '_result-'+config_name(drefcfg_(dref,S)) if destdir is None else
    'result-'+config_name(drefcfg_(dref,S)))
  symlink=Path(join(destdir_,name_))
  forcelink(Path(relpath(dref2path(dref,S), destdir_)), symlink)
  return symlink


def linkrrefs(rrefs:Iterable[RRef], destdir:Optional[Path]=None,
              withtime:bool=False,
              S=None)->List[Path]:
  """ A Wrapper around `linkrref` for linking a set of RRefs. """
  acc=[]
  for r in rrefs:
    acc.append(linkrref(r, destdir=destdir, name=None, withtime=withtime, S=S))
  return acc


def mksymlink(rref:RRef, tgtpath:Path, name:str, withtime:bool=True, S=None)->Path:
  """ A wrapper for `linkrref`, for backward compatibility """
  assert isdir(tgtpath), f"Target link directory doesn't exist: '{tgtpath}'"
  return linkrref(rref, destdir=tgtpath, name=name, withtime=withtime, S=S)


def match_ge(n:int):
  def _matcher(S:SPath, rrefs:List[RRef])->Optional[List[RRef]]:
    if len(rrefs)==0:
      return None
    assert len(rrefs)==n, "Expecting exactly {n} matches"
    return rrefs
  return _matcher

def match_predicate(paccept:Callable[[Output[RRef]],bool],
                    passert:Callable[[Output[RRef]],bool]):
  def _matcher(S:SPath, rrefs:Output[RRef])->Optional[Output[RRef]]:
    if passert(rrefs):
      assert False, f"Matching is impossible for {rrefs}"
    if paccept(rrefs):
      return rrefs
    return None
  return _matcher


def match_only():
  return match_predicate(paccept=lambda l: l.n()==1,
                         passert=lambda l: l.n()>=2)

def match_some(n:int):
  return match_predicate(paccept=lambda l: l.n()>=n,
                         passert=lambda l: False)

def cfgsp(c:Config)->List[Tuple[str,RefPath]]:
  selfpaths=[]
  def _mut(key:Any, val:Any):
    nonlocal selfpaths
    if isselfpath(val):
      selfpaths.append((str(key),val))
    return val
  traverse_dict(config_dict(c),_mut)
  return selfpaths



_PATHS = TypeVar('_PATHS', bound=EquivClasses[Path])


def promise_realizer(
  f:Callable[[SPath,DRef,Context,RealizeArg],_PATHS],
  )->Callable[[SPath,DRef,Context,RealizeArg],_PATHS]:
  def _r(S:SPath, dref:DRef, ctx:Context, ra:RealizeArg)->_PATHS:
    ps=f(S,dref,ctx,ra)
    failed=[]
    for key,promisepath in cfgsp(drefcfg_(dref,S)):
      for p in ps.promisers():
        ppath=join(p,*promisepath[1:])
        if not (isfile(ppath) or isdir(ppath) or islink(ppath)):
          failed.append((p,promisepath))
    if len(failed)>0:
      raise PromiseException(dref, failed)
    return ps
  return _r


#     _                      _
#    / \   ___ ___  ___ _ __| |_ ___
#   / _ \ / __/ __|/ _ \ '__| __/ __|
#  / ___ \\__ \__ \  __/ |  | |_\__ \
# /_/   \_\___/___/\___|_|   \__|___/


def assert_valid_refpath(refpath:RefPath)->None:
  error_msg=(f"Value of type {type(refpath)} is not a valid refpath! Expected "
             f"list of strings starting from a valid DRef string, got '{refpath}'")
  assert isrefpath(refpath), error_msg

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

def assert_rref_deps(c:Config)->None:
  _,rrefs=scanref_dict(config_dict(c))
  assert len(rrefs)==0, (
    f"Realization references were found in configuration:\n"
    f"{config_dict(c)}:\n"
    f"Normally derivations should not contain references to "
    f"realizations, because Pylightnix doesn't keep "
    f"records of how did we build it.\n")

def assert_have_realizers(m:Manager, drefs:List[DRef])->None:
  have_drefs=set(m.builders.keys())
  need_drefs=drefdeps(drefs,m.storage) | set(drefs)
  missing=list(need_drefs-have_drefs)
  assert len(missing)==0, (
    f"The following derivations don't have realizers associated with them:\n"
    f"{missing}\n"
    f"Did you mix DRefs from several `Manager` sessions?")

