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
                                getLogger, scandir, threading_local)

from pylightnix.utils import (dirhash, assert_serializable, assert_valid_dict,
                              dicthash, scanref_dict, scanref_list, forcelink,
                              timestring, parsetime, datahash, readjson,
                              tryread, encode, dirchmod, dirrm, filero, isrref,
                              isdref, traverse_dict, tryread_def,
                              tryreadjson_def, isrefpath, kahntsort, dagroots,
                              isselfpath, selfref)

from pylightnix.types import (StorageSettings, Dict, List, Any, Tuple, Union,
                              Optional, Iterable, IO, Path, SPath, Hash, DRef,
                              RRef, RefPath, HashPart, Callable, Context, Name,
                              NamedTuple, Build, RConfig, ConfigAttrs,
                              Derivation, Stage, Registry, Matcher, MatcherO,
                              Realizer, RealizerO, Set, Closure, Generator,
                              BuildArgs, Config, RealizeArg, InstantiateArg,
                              Output, TypeVar, PromiseException, StageResult,
                              Tuple, Iterator)


#: *Do not change!*
#: Tracks the version of pylightnix storage
PYLIGHTNIX_STORE_VERSION=0

#: Set the regular expression pattern for valid name characters.
PYLIGHTNIX_NAMEPAT="[a-zA-Z0-9_-]"

#: Reserved file names are treated specially be the core. Users should
#: not normally create or alter files with these names.
PYLIGHTNIX_RESERVED=['context.json','group.json']


logger=getLogger(__name__)
info=logger.info
warning=logger.warning

#: Thread-local storage for [current_registry](#pylightnix.core.current_registry)
#: to store its state.
TL=threading_local()

def tlregistry(M:Optional[Registry])->Optional[Registry]:
  """ Return the currently active [Registry](#pylightnix.types.Registry) """
  global TL
  tlm=getattr(TL,'registry',None)
  return M if M else tlm
def tlstorage(S:Optional[StorageSettings])->Optional[StorageSettings]:
  """ Return the currently active
  [StorageSettings](#pylightnix.types.StorageSettings) """
  tlm=tlregistry(None)
  tls=getattr(TL,'storage',None)
  return S if S else (tls if tls else (tlm.S if tlm else None))


def storagename():
  """ Return the name of Pylightnix storage filder. """
  return f"store-v{PYLIGHTNIX_STORE_VERSION}"

def fsroot(S:Optional[StorageSettings]=None)->Path:
  """ `fsroot` contains the path to the root of pylightnix shared data folder.
  Default is `~/_pylightnix` or `/var/run/_pylightnix` if no `$HOME` is
  available.  Setting `PYLIGHTNIX_ROOT` environment variable overwrites the
  defaults.  """
  S=tlstorage(S)
  if S is not None and S.root is not None:
    return S.root
  else:
    return Path(environ.get('PYLIGHTNIX_ROOT',
      join(environ.get('HOME','/var/run'), '_pylightnix')))

def fstmpdir(S:Optional[StorageSettings]=None)->Path:
  """ Return the location of current Pylightnix temporary folder, defaulting to
  the path set by PYLIGHTNIX_TMP environment variable. """
  S=tlstorage(S)
  if S is not None and S.tmpdir is not None:
    return S.tmpdir
  else:
    return Path(environ.get('PYLIGHTNIX_TMP', join(fsroot(S),'tmp')))

def fsstorage(S:Optional[StorageSettings]=None)->Path:
  """ Return the location of current Pylightnix storage folder, defaulting to
  the path set by PYLIGHTNIX_STORAGE environment variable. """
  S=tlstorage(S)
  if S is not None and S.storage is not None:
    return S.storage
  else:
    return Path(environ.get('PYLIGHTNIX_STORAGE',
                            join(fsroot(S),storagename())))

def assert_valid_storage(S:Optional[StorageSettings]=None)->None:
  assert isdir(fsstorage(S)), \
    (f"Looks like the Pylightnix storage ('{fsstorage(S)}') does not "
     f"exist. Consider calling `fsinit` first.")
  assert isdir(fstmpdir(S)), \
    (f"Looks like the Pylightnix tmp ('{fstmpdir(S)}') does not exist. "
     f"Consider calling `fsinit` first.")
  assert lstat((fsstorage(S))).st_dev == lstat(fstmpdir(S)).st_dev, \
    (f"Pylightnix storage ({fsstorage(S)}) and temp ({fstmpdir(S)}) "
     f"directories belong to different filesystems. This case is not "
     f"supported yet.")

def mkSS(root:str, stordir:Optional[str]=None, tmpdir:Optional[str]=None
         )->StorageSettings:
  """ Constructor for [StorageSettings](#pylightnix.types.StorageSettings)"""
  return StorageSettings(Path(root),
                         Path(stordir) if stordir else None,
                         Path(tmpdir) if tmpdir else None)

def mkregistry(S:Optional[StorageSettings]=None)->Registry:
  return Registry(tlstorage(S))

def setstorage(S:Optional[StorageSettings])->Optional[StorageSettings]:
  global TL
  old=getattr(TL,'storage',None)
  setattr(TL,'storage',S)
  return old

def setregistry(r:Optional[Registry])->Optional[Registry]:
  global TL
  old=getattr(TL,'registry',None)
  setattr(TL,'registry',r)
  return old

def fsinit(ss:Optional[Union[str,StorageSettings]]=None,
           check_not_exist:bool=False,
           remove_existing:bool=False,
           use_as_default:bool=True)->None:
  """ Imperatively create the filesystem storage and temp direcory if they don't
  exist.  Default locations may be altered by `PYLIGHTNIX_STORAGE` and
  `PYLIGHTNIX_TMP` env variables. """
  P='_pylightnix'
  S:Optional[StorageSettings]=\
    mkSS(Path(join(ss,P) if not ss.endswith(P) else ss)) \
    if isinstance(ss,str) else ss
  if remove_existing:
    dirrm(fsstorage(S))
    dirrm(fstmpdir(S))
    makedirs(fsstorage(S), exist_ok=False)
    makedirs(fstmpdir(S), exist_ok=False)
  else:
    makedirs(fsstorage(S), exist_ok=False if check_not_exist else True)
    makedirs(fstmpdir(S), exist_ok=False if check_not_exist else True)
  if use_as_default:
    setstorage(S)
  assert_valid_storage(S)

def reserved(folder:Path, name:str)->Path:
  assert name in PYLIGHTNIX_RESERVED, \
    f"File name '{name}' expected to be reserved"
  return Path(join(folder,name))

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
  """ Create a [Config](#pylightnix.types.Config) object out of config
  dictionary. Asserts if the dictionary is not JSON-compatible. As a handy hack,
  filter out `r:Registry` variable which likely is an utility
  [Registry](#pylightnix.types.Registry) object.
  """
  d2={k:v for k,v in d.items()
     if not (k=='r' and 'Registry' in str(type(v)))}
  assert_valid_dict(d2,'dict')
  cfg=Config(d2)
  assert_valid_config(cfg)
  return cfg

def cfgdict(cp:Config)->dict:
  return deepcopy(cp.val)

def cfgcattrs(c:RConfig)->Any:
  return ConfigAttrs(cfgdict(c))

def cfgserialize(c:Config)->str:
  return json_dumps(cfgdict(c), indent=4)

def cfghash(c:Config)->Hash:
  return datahash([(cfgname(c),encode(cfgserialize(c)))])

def cfgname(c:Config)->Name:
  """ Return a `name` field of a config `c`, defaulting to string "unnmaed". """
  return mkname(cfgdict(c).get('name','unnamed'))

def cfgdeps(c:Config)->Set[DRef]:
  drefs,_=scanref_dict(cfgdict(c))
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


def resolve(c:Config, r:DRef)->RConfig:
  """ Replace all Promise tags with DRef `r`. In particular, all PromisePaths
  are converted into RefPaths. """
  d=cfgdict(c)
  def _mut(k:Any,val:Any):
    if isselfpath(val):
      return [DRef(r)]+val[1:]
    else:
      return val
  traverse_dict(d,_mut)
  return RConfig(d)


def dref2path(r:DRef,S=None)->Path:
  (dhash,nm)=undref(r)
  return Path(join(fsstorage(S),dhash+'-'+nm))

def rref2path(r:RRef, S=None)->Path:
  (rhash,dhash,nm)=unrref(r)
  return Path(join(fsstorage(S),dhash+'-'+nm,rhash))

def rrefpath2path(r:RRef, refpath:RefPath, S=None)->Path:
  assert isinstance(refpath[0],DRef) and rref2dref(r)==refpath[0]
  return Path(join(rref2path(r),*refpath[1:]))

def drefcfgpath(r:DRef,S=None)->Path:
  return Path(join(dref2path(r,S),'config.json'))

def rrefctx(r:RRef, S=None)->Context:
  """ Return the realization context. """
  assert_valid_rref(r)
  ctx=readjson(join(rref2path(r,S),'context.json'))
  assert isinstance(ctx,dict)
  return ctx

def drefcfg_(dref:DRef,S=None)->Config:
  """ Return `dref` configuration, selfrefs are _not_ resolved """
  cfg=readjson(drefcfgpath(dref,S))
  assert isinstance(cfg,dict)
  c=Config(cfg)
  assert_valid_config(c)
  return c

def drefcfg(dref:DRef,S=None)->RConfig:
  """ Return `dref` configuration, selfrefs are resolved """
  return resolve(drefcfg_(dref,S),dref)

def drefattrs(r:DRef, S=None)->Any:
  """ Read the [ConfigAttrs](#pylightnix.types.ConfigAttr) of the storage node `r`.
  Note, that it is a kind of 'syntactic sugar' for `drefcfg`. Both
  functions do the same thing. """
  return cfgcattrs(drefcfg(r,S))

def rrefattrs(r:RRef, S=None)->Any:
  """ Read the [ConfigAttrs](#pylightnix.types.ConfigAttr) of the storage node `r`.
  Note, that it is a kind of 'syntactic sugar' for `drefcfg`. Both
  functions do the same thing. """
  return drefattrs(rref2dref(r),S)

def drefdeps1(drefs:Iterable[DRef],S=None)->Set[DRef]:
  """ Return a set of reference's immediate dependencies, not including `drefs`
  themselves. """
  acc=set()
  for dref in drefs:
    acc.update(cfgdeps(drefcfg_(dref,S)))
  return acc

def rrefdeps1(rrefs:Iterable[RRef],S=None)->Set[RRef]:
  """ Return a set of reference's immediate dependencies, not including `rrefs`
  themselves. """
  acc=set()
  for rref in rrefs:
    dref=rref2dref(rref)
    for dref_dep in drefdeps1([dref],S):
      acc|=set(context_deref(rrefctx(rref,S),dref_dep))
  return acc

def drefdeps(drefs:Iterable[DRef],S=None)->Set[DRef]:
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
  store_path_=fsstorage(S)
  for dirname in listdir(store_path_):
    if dirname[-4:]!='.tmp' and isdir(join(store_path_,dirname)):
      yield mkdref(HashPart(dirname[:32]), Name(dirname[32+1:]))

def allrrefs(S=None)->Iterable[RRef]:
  """ Iterates over all realization references in `S` (PYLIGHTNIX_STORE env is
  used by default) """
  for dref in alldrefs(S):
    for rref in drefrrefs(dref,S):
      yield rref

def rootdrefs(S:Optional[StorageSettings]=None)->Set[DRef]:
  """ Return root DRefs of the storage `S` as a set """
  def _inb(x):
    return drefdeps1([x],S=S)
  topsorted=kahntsort(alldrefs(S), _inb)
  assert topsorted is not None, (
    f"Falied to topologically sort the derivations of {S}. This "
    f"probably means that the storage ({S if S else 'default'}) is damaged")
  return dagroots(topsorted, _inb)

def rootrrefs(S:Optional[StorageSettings]=None)->Set[RRef]:
  """ Return root RRefs of the storage `S` as a set """
  def _inb(x):
    return rrefdeps1([x],S=S)
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

def drefrrefs(dref:DRef,S=None)->Set[RRef]:
  """ Iterate over all realizations of a derivation `dref`. The sort order is
  unspecified. Matchers are not taken into account. """
  (dhash,nm)=undref(dref)
  drefpath=dref2path(dref,S)
  rrefs:Set[RRef]=set()
  for f in listdir(drefpath):
    if f[-4:]!='.tmp' and isdir(join(drefpath,f)):
      rrefs.add(mkrref(HashPart(f), dhash, nm))
  return rrefs

def drefrrefsC(dref:DRef, context:Context, S=None)->Iterable[RRef]:
  """ Iterate over realizations of a derivation `dref` that match the specified
  [context](#pylightnix.types.Context). Sorting order is unspecified. """
  for rref in drefrrefs(dref,S):
    context2=rrefctx(rref,S)
    if context_eq(context,context2):
      yield rref

def store_gc(keep_drefs:List[DRef],
             keep_rrefs:List[RRef],
             S:Optional[StorageSettings]=None)->Tuple[Set[DRef],Set[RRef]]:
  """ Take roots which are in use and should not be removed. Return roots which
  are not used and may be removed. Actual removing is to be done by the user.

  Default location of `S` may be changed.

  See also [rmref](#pylightnix.bashlike.rmref)"""
  clo_drefs=drefdeps(set(keep_drefs),S) | set(keep_drefs)
  clo_rrefs=rrefdeps(set(keep_rrefs),S) | set(keep_rrefs)

  clo_drefs2=clo_drefs | {rref2dref(rref) for rref in clo_rrefs}
  clo_rrefs2=clo_rrefs | \
    set.union(set(),*[drefrrefs(dref,S) for dref in clo_drefs]) # type:ignore
  remove_drefs=set()
  remove_rrefs=set()
  for dref in alldrefs(S):
    if dref not in clo_drefs2:
      remove_drefs.add(dref)
      for rref in drefrrefs(dref,S):
        remove_rrefs.add(rref)
    else:
      for rref in drefrrefs(dref,S):
        if rref not in clo_rrefs2:
          remove_rrefs.add(rref)
  return remove_drefs,remove_rrefs


def mkdrv_(c:Config,S=None)->DRef:
  """ See [mkdrv](#pylightnix.core.mkdrv) """

  # FIXME: Assert or handle possible (but improbable) hash collision [*]
  # FIXME: Could the replace fail if two processes call it simultaneously?
  assert_valid_storage(S)
  assert_valid_config(c)
  assert_rref_deps(c)

  refname=cfgname(c)
  dhash=cfghash(c)

  dref=mkdref(trimhash(dhash),refname)

  o=Path(mkdtemp(prefix=refname, dir=fstmpdir(S)))
  with open(join(o,'config.json'), 'w') as f:
    f.write(cfgserialize(c))

  filero(Path(join(o,'config.json')))
  drefpath=dref2path(dref,S)
  dreftmp=Path(drefpath+'.tmp')
  replace(o,dreftmp) # [**]

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
  """ Inserts the newly-obtaind [Stage](#pylightnix.types.Stage) artifacts into
  the Storage, return the [realization reference](#pylightnix.types.RRef). Not
  intended to be called by user.

  Parameters:
  - `dref:DRef`: Derivation reference to create the realization of.
  - `l:Context`: Context which stores dependency information.
  - `o:Path`: Path to temporal (build) folder which contains artifacts,
    prepared by the [Realizer](#pylightnix.types.Realizer).
  - `leader`: Tag name and Group identifier of the Group leader. By default,
    we use name `out` and derivation's own rref.
  """

  # FIXME: Assert or handle possible but improbable hash collision[*]
  # FIXME: Timestamps are not overwritten, because they are not hashed

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
      warning(f'Realization collision: {rref} already exist, unhashed files '
              f'(__*__.*) may differ.')
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

def context_add(ctx:Context, dref:DRef, rrefs:Optional[List[RRef]])->Context:
  """ Add a pair `(dref,rrefs)` into a context `ctx`. `rrefs` are supposed to
  form (a subset of) the realizations of `dref`.
  Return a new context. """
  assert dref not in ctx, (
    f"Attempting to re-introduce DRef {dref} to context with a "
    f"different realization.\n"
    f" * Old realization: {ctx[dref]}\n"
    f" * New realization: {rrefs}\n")
  return dict(sorted([(dref,list(sorted(rrefs)) if rrefs else None)]+list(ctx.items())))

def context_deref(context:Context, dref:DRef)->List[RRef]:
  """ TODO: Should it return Output (aka `UniformList`) rather than Python list?
  """
  assert dref in context, (
    f"Context {context} doesn't declare {dref} among it's dependencies so we "
    f"can't dereference it.")
  return context[dref]

def context_derefpath(context:Context,
                      refpath:RefPath,
                      S=None)->List[Path]:
  assert isinstance(refpath[0],DRef)
  rrefs=context_deref(context,refpath[0])
  return [Path(join(rref2path(r,S), *refpath[1:])) for r in rrefs]


def context_serialize(c:Context)->str:
  assert_valid_context(c)
  return json_dumps(c, indent=4)

#  _____           _                _
# |_   _|__  _ __ | | _____   _____| |
#   | |/ _ \| '_ \| |/ _ \ \ / / _ \ |
#   | | (_) | |_) | |  __/\ V /  __/ |
#   |_|\___/| .__/|_|\___| \_/ \___|_|
#           |_|


def output_validate(dref:DRef, o:Output[Path], S=None)->List[Path]:
    failed=[]
    for key,promisepath in cfgsp(drefcfg_(dref,S)):
      for p in o.val:
        ppath=join(p,*promisepath[1:])
        if not (isfile(ppath) or isdir(ppath) or islink(ppath)):
          failed.append((p,promisepath))
    if len(failed)>0:
      raise PromiseException(dref, failed)
    return o.val


def output_realizer(f:RealizerO)->Realizer:
  def _r(S:Optional[StorageSettings], dref:DRef, ctx:Context,
         ra:RealizeArg)->List[Path]:
    return output_validate(dref,f(S,dref,ctx,ra),S=S)
  return _r

def output_matcher(r:MatcherO)->Matcher:
  def _m(S:Optional[StorageSettings],rrefs:List[RRef])->Optional[List[RRef]]:
    res=r(S,Output(rrefs))
    return res.val if res is not None else None
  return _m

def mkdrv(config:Config,
          matcher:Matcher,
          realizer:Realizer,
          r:Optional[Registry]=None)->DRef:
  """ Construct a [Derivation](#pylightnix.types.Derivation) object out of
  [Config](#pylightnix.types.Config), [Matcher](#pylightnix.types.Matcher) and
  [Realizer](#pylightnix.types.Realizer). Register the derivation in the
  dependency-resolution [Registry](#pylightnix.types.Registry). Return [Derivation
  references](#pylightnix.types.DRef) of the newly-obtained derivation.

  Arguments:
  - `r:Registry`: A Registry to update with a new derivation

  Example:
  ```python
  def somestage(r:Registry)->DRef:
    def _realizer(b:Build):
      with open(join(build_outpath(b),'artifact'),'w') as f:
        f.write(...)
    return mkdrv(r,mkconfig({'name':'mystage'}), match_only(), build_wrapper(_realizer))

  rref:RRef=realize1(instantiate(somestage))
  ```
  """
  # FIXME: check that all config's dependencies are known to the Registry
  r=tlregistry(r)
  assert r is not None, "Default registry is not set"
  dref=mkdrv_(config,S=r.S)
  if dref in r.builders:
    warning(f"Overwriting the derivation of '{dref}'. This could be a "
            f"result of calling the same `mkdrv` twice with the same Registry.")
  r.builders[dref]=Derivation(dref, matcher, realizer)
  return dref

@contextmanager
def current_registry(r:Registry)->Iterator[Registry]:
  """ Sets the default global [Registry](#pylightnix.types.Registry) for the
  inner scoped code. Internally calls
  [current_storage(r.S)](#pylightnix.core.current_storage)"""
  global TL
  old=setregistry(r)
  try:
    with current_storage(r.S):
      yield TL.registry
  finally:
    setregistry(old)

@contextmanager
def current_storage(S:Optional[StorageSettings])->Iterator[Optional[StorageSettings]]:
  """ Sets the global default
  [StorageSettings](#pylightnix.types.StorageSettings) for the inner scoped code
  """
  old=setstorage(S)
  try:
    yield S
  finally:
    setstorage(old)


def mkclosure(result:Any,r:Registry)->Closure:
  targets,_=scanref_dict({'result':result})
  assert len(targets)>0, f"No DRefs to instantiate in {result}"
  assert_have_realizers(r,targets)
  return Closure(result,targets,list(r.builders.values()),S=r.S)


_A=TypeVar('_A')
def instantiate(stage:Union[_A,Callable[...,Any]], # <-- [*]
                *args:Any,
                S:Optional[StorageSettings]=None,
                r:Optional[Registry]=None,
                **kwargs:Any)->Tuple[_A,Closure]:
  """ Scans a Python [DRef](#pylightnix.types.DRef) container (list, dict alike)
  or evaluates the [Stage](#pylightnix.types.Stage) function by calling it.

  Returns the [Closure](#pylightnix.types.Closure) formed out of nested
  [Derivations](#pylightnix.types.Derivation). The closure returned is ready to
  be [realized](#pylightnix.core.realize).

  Arguments:
  - `stage`: `Stage` function to call or `DRef` container to scan.
  - `r:Optional[Registry]=None`: [Registry](#pylightnix.types.Registry) to
     register derivations in.
  - `S:Optional[StorageSettings]=None`:
    [StorageSettings](#pylightnix.types.StorageSettings) specifies the locations
    of the on-disk derivation data folders. Should match `r.S` if `r` is passed.

  Returns:
  - `DRef` container holding references to the newly registered derivations.
  """
  # FIXME: mypy can't typecheck _A in place of Any for some reason [*]
  r=tlregistry(r)
  if r is None:
    r=mkregistry(S)
  else:
    if S is None:
      S=r.S
    else:
      assert S==r.S, (
        f"S should match the Registry's if specified. 'S={S}' while "
        f"registry has '{r.S}'")
  assert not r.in_instantiate, (
    "Recursion detected. `instantiate` should not be called recursively "
    "by stage functions with the same `Registry` as argument")
  r.in_instantiate=True
  try:
    if callable(stage):
      result=stage(*args,r=r,**kwargs)
    else:
      # FIXME: Put `assert isdref(stage)` and check
      # assert isdref(stage)
      result=stage
  finally:
    r.in_instantiate=False
  return result,mkclosure(result,r)


RealizeSeqGen = Generator[
  Tuple[Optional[StorageSettings],DRef,Context,Derivation,RealizeArg],
  Tuple[Optional[List[RRef]],bool],
  Context]


def realize1(closure:Union[Closure,Tuple[StageResult,Closure]],
             force_rebuild:Union[List[DRef],bool]=[],
             assert_realized:List[DRef]=[],
             realize_args:Dict[DRef,RealizeArg]={},
             dry_run:bool=False,
             )->RRef:
  """ [Realize](#pylightnix.core.realize) a closure, assuming that it returns a
  single realization. """

  # FIXME: Stage's context is calculated inefficiently. Maybe one should track
  # dep.tree to avoid calling `drefdeps` within the cycle.
  # FIXME: Update derivation's matcher after forced rebuilds. Matchers should
  # remember and reproduce user's preferences.
  rrefs=realizeMany(closure, force_rebuild,
                    assert_realized, realize_args, dry_run)
  assert len(rrefs)==1, (
    f"`realize1` is to be used with a single-output derivation. "
    f"The current target has {len(rrefs)} outputs:\n{rrefs}\n"
    f"Consider using `realizeMany`." )
  return rrefs[0]


def realizeMany(closure:Union[Closure,Tuple[StageResult,Closure]],
                force_rebuild:Union[List[DRef],bool]=[],
                assert_realized:List[DRef]=[],
                realize_args:Dict[DRef,RealizeArg]={},
                dry_run:bool=False,
                )->List[RRef]:
  """ [Realize](#pylightnix.core.realize) a closure, assuming that it returns a
  list of realizations. """
  r,_,ctx=realize(closure, force_rebuild, assert_realized, realize_args, dry_run)
  assert isdref(r), f"realizeMany expects a single dref target, not {r}"
  return ctx[DRef(r)]

def unpack_closure_arg_(arg:Union[Closure,Tuple[StageResult,Closure]]
                        )->Tuple[StageResult,Closure]:
  closure_:Closure
  if isinstance(arg,tuple) and len(arg)==2:
    result_=arg[0]
    closure_=arg[1] # type:ignore
  else:
    closure_=arg # type:ignore
    result_=closure_.result
  return (result_,closure_)


def realize(closure:Union[Closure,Tuple[StageResult,Closure]],
            force_rebuild:Union[List[DRef],bool]=[],
            assert_realized:List[DRef]=[],
            realize_args:Dict[DRef,RealizeArg]={},
            dry_run:bool=False
            )->Tuple[StageResult,Closure,Context]:
  """ Takes the instantiated [Closure](#pylightnix.types.Closure) and evaluates
  its targets. Calls the realizers if derivation
  [matchers](#pylightnix.types.Matcher) require so.

  Returns the target [DRefs](#pylightnix.types.DRef), optionally packed in a
  Python structure like list or dict, the dependency
  [Closure](#pylightnix.types.Closure) holding the complete set of derivation
  references, and the
  resulting [Context](#pylightnix.types.Context).

  `realize` is the most generic version of the realization algorithm. The
  simplified or specialized versions are [realizeU](#pylightnix.deco.realizeU),
  [realize1](#pylightnix.core.realize1),
  [realizeMany](#pylightnix.core.realizeMany),
  [repl_realize](#pylightnix.repl.repl_realize).

  Example:
  ```python
  def mystage(r:Registry)->DRef:
    ...
    return mkdrv(r, ...)

  rrefs=realize1(instantiate(mystage))
  print(mklen(rref).syspath)
  ```
  """
  # FIXME: define a Closure as a datatype and simplify the below line
  result_,closure_=unpack_closure_arg_(closure)
  force_interrupt:List[DRef]
  if isinstance(force_rebuild,bool):
    force_interrupt=closure_.targets if force_rebuild else []
  elif isinstance(force_rebuild,list):
    force_interrupt=force_rebuild
  else:
    assert False, "Ivalid type of `force_rebuild` argument"
  try:
    gen=realizeSeq(closure_, force_interrupt, assert_realized, realize_args,
                   dry_run)
    next(gen)
    while True:
      gen.send((None,False)) # Ask for the default action
  except StopIteration as e:
    ctx=e.value
  return result_,closure_,ctx


def realizeSeq(closure:Closure,
               force_interrupt:List[DRef]=[],
               assert_realized:List[DRef]=[],
               realize_args:Dict[DRef,RealizeArg]={},
               dry_run:bool=False
               )->RealizeSeqGen:
  """ `realizeSeq` encodes low-level details of the realization algorithm.
  Sequentially realize the closure by issuing steps via Python's generator
  interface. Consider calling [realize](#pylightnix.core.realize) or it's
  analogs instead.

  FIXME: try to implement `assert_realized` by calling `redefine` with
  appropriate failing realizer on every Derivation. """
  S=closure.S
  assert_valid_closure(closure)
  force_interrupt_:Set[DRef]=set(force_interrupt)
  context_acc:Context={}
  target_drefs=closure.targets
  target_deps=drefdeps(target_drefs,S)
  for drv in closure.derivations:
    dref=drv.dref
    rrefs:Optional[List[RRef]]
    if dref in target_deps or dref in target_drefs:
      dref_deps=drefdeps([dref],S)
      dref_context={k:v for k,v in context_acc.items() if k in dref_deps} # I
      if dref in force_interrupt_:
        rrefs,abort=yield (S,dref,dref_context,drv,realize_args.get(dref,{}))
        if abort:
          return {}
      else:
        rrefs=drv.matcher(S, list(drefrrefsC(dref,dref_context,S)))
      if rrefs is None and not dry_run:
        assert dref not in assert_realized, (
          f"Stage '{dref}' was assumed to be already realized. "
          f"Unfortunately, it is not the case. Config:\n"
          f"{drefcfg_(dref)}")
        rrefs_existed=drefrrefsC(dref,dref_context,S)
        rpaths:List[Path]=drv.realizer(S,dref,dref_context,
                                       realize_args.get(dref,{}))
        rrefs_built:List[RRef]=[mkrealization(dref,dref_context,rp,S)
                                for rp in rpaths]
        if len(rpaths)!=len(set(rrefs_built)):
          warning(f"Realizer of {dref} produced duplicated realizations")
        rrefs_matched=drv.matcher(S,list(drefrrefsC(dref,dref_context,S)))
        assert rrefs_matched is not None, (
          f"The matcher of '{dref}' is not satisfied with its realizatons. "
          f"The following newly obtained realizations were ignored:\n"
          f"  {rrefs_built}\n"
          f"The following realizations currently exist:\n"
          f"  {list(rrefs_existed)}")
        if (set(rrefs_built) & set(rrefs_matched)) == set() and \
           (set(rrefs_built) | set(rrefs_matched)) != set():
          warning(f"None of the newly obtained {dref} realizations "
                  f"were matched by the matcher. To capture those "
                  f"realizations explicitly, try `matcher([exact(..)])`")
        rrefs=rrefs_matched
      context_acc=context_add(context_acc,dref,rrefs)
  assert dry_run or all((context_acc[t] is not None) for t in closure.targets)
  return context_acc


def evaluate(stage, *args, **kwargs)->RRef:
  return realize1(instantiate(stage,*args,**kwargs))

Key = Callable[[Optional[StorageSettings], RRef],Optional[Union[int,float,str]]]

def texthash()->Key:
  def _key(S, rref:RRef)->Optional[Union[int,float,str]]:
    return str(unrref(rref)[0])
  return _key

def latest()->Key:
  def _key(S, rref:RRef)->Optional[Union[int,float,str]]:
    try:
      with open(join(rref2path(rref, S=S),'__buildstart__.txt'),'r') as f:
        t=parsetime(f.read())
        return float(0 if t is None else t)
    except OSError as e:
      return float(0)
  return _key

def exact(expected:List[RRef])->Key:
  def _key(S, rref:RRef)->Optional[Union[int,float,str]]:
    return 1 if rref in expected else None
  return _key

def match(key:Key,
          trim:Callable[[List[RRef]],Optional[List[RRef]]],
          mnext:Optional[Matcher]=None,
          )->Matcher:
  """ Create a [Matcher](#pylightnix.types.Matcher) by combining different
  sorting keys and selecting a top-n threshold.

  Only realizations which have [tag](#pylightnix.types.Tag) 'out' (which is a
  default tag name) participate in matching. After the matching, Pylightnix
  adds all non-'out' realizations which share [group](#pylightnix.types.Group)
  with at least one matched realization.

  Arguments:
  - `keys`: List of [Key](#pylightnix.types.Key) functions. Defaults ot
  """
  def _matcher(S:Optional[StorageSettings],
               rrefs:List[RRef])->Optional[List[RRef]]:
    # Match only among realizations tagged as 'out'
    keymap={rref:key(S,rref) for rref in rrefs}

    # Apply filters and filter outputs
    res=trim(sorted(filter(lambda rref: keymap[rref] is not None, rrefs),
                    key=lambda rref: keymap[rref], reverse=True)) # type:ignore
    return (mnext(S,res) if res else None) if mnext else res
  return _matcher

def match_all(S,rrefs):
  return rrefs if len(rrefs)>0 else None

def match_some(n:int=1, key=None):
  assert n>=0
  _key=key if key is not None else texthash()
  def _trim(rrefs):
    return rrefs[:n] if len(rrefs)>=n else None
  return match(_key, _trim, match_all)

def match_only():
  def _trim(rrefs):
    if len(rrefs)>1:
      assert False, (
        f"Matcher `match_only` expected to see no more than one realization "
        f"of '{rref2dref(rrefs[0])}', but there are {len(rrefs)} of them. "
        f"Consider using a better matcher.")
    return rrefs[:1] if len(rrefs)==1 else None
  return match(texthash(), _trim)

def match_latest(n:int=1)->Matcher:
  return match_some(n, key=latest())

def match_exact(rrefs:List[RRef]):
  return match_some(n=len(rrefs), key=exact(rrefs))


def cfgsp(c:Config)->List[Tuple[str,RefPath]]:
  """ Returns the list of self-references (aka self-paths) in the config. """
  selfpaths=[]
  def _mut(key:Any, val:Any):
    nonlocal selfpaths
    if isselfpath(val):
      selfpaths.append((str(key),val))
    return val
  traverse_dict(cfgdict(c),_mut)
  return selfpaths


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
  assert_valid_name(cfgname(c))
  assert_valid_dict(cfgdict(c), 'Config')
  return c

def assert_valid_name(s:Name)->None:
  assert re_match(f"^{PYLIGHTNIX_NAMEPAT}+$", s), \
      f"Expected a name which matches /^{PYLIGHTNIX_NAMEPAT}+$/, got '{s}'."

def assert_valid_rref(ref:str)->None:
  error_msg=(f'Value "{ref}" is not a valid realization reference! Expected '
             f'a string of form \'rref:HASH-HASH-name\'')
  assert isrref(ref), error_msg

def assert_valid_hashpart(hp:HashPart)->None:
  assert len(hp)==32, f"HashPart should have length of 32, but " \
                      f"len({hp})=={len(hp)}"
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
  assert all([dref in [d.dref for d in closure.derivations] \
             for dref in closure.targets]), \
    "Closure should contain target derivation"

def assert_rref_deps(c:Config)->None:
  _,rrefs=scanref_dict(cfgdict(c))
  assert len(rrefs)==0, (
    f"Realization references were found in configuration:\n"
    f"{cfgdict(c)}:\n"
    f"Normally derivations should not contain references to "
    f"realizations, because Pylightnix doesn't keep "
    f"records of how did we build it.\n")

def assert_have_realizers(r:Registry, drefs:List[DRef])->None:
  have_drefs=set(r.builders.keys())
  need_drefs=drefdeps(drefs,r.S) | set(drefs)
  missing=list(need_drefs-have_drefs)
  assert len(missing)==0, (
    f"The following derivations don't have realizers associated with them:\n"
    f"{missing}\n"
    f"Did you mix DRefs from several `Registry` sessions?")

