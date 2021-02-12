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
                                getLogger)

from pylightnix.utils import (dirhash, assert_serializable, assert_valid_dict,
                              dicthash, scanref_dict, scanref_list, forcelink,
                              timestring, parsetime, datahash, readjson,
                              tryread, encode, dirchmod, dirrm, filero, isrref,
                              isdref, traverse_dict, ispromise, isclaim,
                              tryread_def, tryreadjson_def, isrefpath)

from pylightnix.types import (Dict, List, Any, Tuple, Union, Optional,
                              Iterable, IO, Path, SPath, Hash, DRef, RRef,
                              RefPath, PromisePath, HashPart, Callable,
                              Context, Name, NamedTuple, Build, RConfig,
                              ConfigAttrs, Derivation, Stage, Manager, Matcher,
                              Realizer, Set, Closure, Generator, Key,
                              BuildArgs, PYLIGHTNIX_PROMISE_TAG,
                              PYLIGHTNIX_CLAIM_TAG, Config, RealizeArg,
                              InstantiateArg, Tag, Group, RRefGroup)

logger=getLogger(__name__)
info=logger.info
warning=logger.warning

#: *Do not change!*
#: Tracks the version of pylightnix storage
PYLIGHTNIX_STORE_VERSION=0

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

#: `PYLIGHTNIX_STORE` contains the path to the main pylightnix store folder.
#:
#: By default, the store is located in `$PYLIGHTNIX_ROOT/store-vXX` folder.
#: Setting `PYLIGHTNIX_STORE` environment variable overwrites the defaults.
PYLIGHTNIX_STORE=join(PYLIGHTNIX_ROOT, f'store-v{PYLIGHTNIX_STORE_VERSION}')

def storage(S:Optional[SPath]=None)->SPath:
  """ Returns the location to Pylightnix storage, defaulting to
  PYLIGHTNIX_STORE """
  return SPath(PYLIGHTNIX_STORE) if S is None else S

#: Set the regular expression pattern for valid name characters.
PYLIGHTNIX_NAMEPAT="[a-zA-Z0-9_-]"

#: Reserved file names are treated specially be the core. Users should
#: not normally create or alter files with this names.
PYLIGHTNIX_RESERVED=['context.json','group.json']

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

def mktag(s:str)->Tag:
  for c in ['\n',' ']:
    assert c not in s
  return Tag(s)

def tag_out()->Tag:
  """ Pre-defined default Tag name """
  return mktag('out')

def mkgroup(s:str)->Group:
  for c in ['\n',' ']:
    assert c not in s
  return Group(s)

#   ____             __ _
#  / ___|___  _ __  / _(_) __ _
# | |   / _ \| '_ \| |_| |/ _` |
# | |__| (_) | | | |  _| | (_| |
#  \____\___/|_| |_|_| |_|\__, |
#                         |___/


def mkconfig(d:dict)->Config:
  """ FIXME: Should we assert on invalid Config here? """
  return Config(assert_valid_dict(d,'dict'))

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

def store_initialize(custom_store:Optional[str]=None,
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
  info(f"Initializing {'' if isdir(PYLIGHTNIX_STORE) else 'non-'}existing "
       f"{PYLIGHTNIX_STORE}")
  makedirs(PYLIGHTNIX_STORE, exist_ok=False if check_not_exist else True)

  if custom_tmp is not None:
    PYLIGHTNIX_TMP=custom_tmp
  makedirs(PYLIGHTNIX_TMP, exist_ok=True)

  assert_store_initialized()

def store_dref2path(r:DRef,S=None)->Path:
  (dhash,nm)=undref(r)
  return Path(join(storage(S),dhash+'-'+nm))

def store_rref2path(r:RRef, S=None)->Path:
  (rhash,dhash,nm)=unrref(r)
  return Path(join(storage(S),dhash+'-'+nm,rhash))

def store_cfgpath(r:DRef,S=None)->Path:
  return Path(join(store_dref2path(r,S),'config.json'))

def store_config_(r:DRef,S=None)->Config:
  return assert_valid_config(Config(readjson(store_cfgpath(r,S))))

def store_config(r:Union[DRef,RRef],S=None)->RConfig:
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

def store_context(r:RRef, S=None)->Context:
  """
  FIXME: Either do `context_add(ctx, rref2dref(r), [r])` or document it's absense
  """
  assert_valid_rref(r)
  return readjson(join(store_rref2path(r,S),'context.json'))

def store_cattrs(r:Union[DRef,RRef], S=None)->Any:
  """ Read the [ConfigAttrs](#pylightnix.types.ConfigAttr) of the storage node `r`.
  Note, that it is a kind of 'syntactic sugar' for `store_config`. Both
  functions do the same thing. """
  return config_cattrs(store_config(r,S))

def store_deps(drefs:Iterable[DRef],S=None)->Set[DRef]:
  """ Return a list of reference's immediate dependencies, not including `refs`
  themselves. """
  acc=set()
  for dref in drefs:
    acc.update(config_deps(store_config(dref,S))-{dref})
  return acc

def store_deepdeps(roots:Iterable[DRef], S=None)->Set[DRef]:
  """ Return the complete set of `roots`'s dependencies, not including `roots`
  themselves. """
  frontier=store_deps(roots,S)
  processed=set()
  while frontier:
    ref = frontier.pop()
    processed.add(ref)
    for dep in store_deps([ref],S):
      if dep not in processed:
        frontier.add(dep)
  return processed

def store_deepdepRrefs(roots:Iterable[RRef],S=None)->Set[RRef]:
  """ Return the complete set of root's dependencies, not including `roots`
  themselves.
  """
  acc:Set=set()
  for rref in roots:
    for rref_deps in store_context(rref,S).values():
      acc|=set(rref_deps)
  return acc

def store_drefs(S=None)->Iterable[DRef]:
  """ Iterates over all derivations of the storage located at `S`
  (PYLIGHTNIX_STORE env is used by default) """
  store_path_=storage(S)
  for dirname in listdir(store_path_):
    if dirname[-4:]!='.tmp' and isdir(join(store_path_,dirname)):
      yield mkdref(HashPart(dirname[:32]), Name(dirname[32+1:]))

def rrefs2groups(rrefs:List[RRef], S=None)->List[RRefGroup]:
  return [({store_tag(rref,S):rref for rref in rrefs if store_group(rref,S)==g})
    for g in sorted({store_group(rref,S) for rref in rrefs})]

def groups2rrefs(grs:List[RRefGroup])->List[RRef]:
  return list(chain.from_iterable([gr.values() for gr in grs]))

def store_rrefs_(dref:DRef,S=None)->List[RRefGroup]:
  """ Iterate over all realizations of a derivation `dref`. The sort order is
  unspecified. """
  (dhash,nm)=undref(dref)
  drefpath=store_dref2path(dref,S)
  rrefs:List[RRef]=[]
  for f in listdir(drefpath):
    if f[-4:]!='.tmp' and isdir(join(drefpath,f)):
      rrefs.append(mkrref(HashPart(f), dhash, nm))
  return rrefs2groups(rrefs,S)

def store_rrefs(dref:DRef, context:Context, S=None)->List[RRefGroup]:
  """ Iterate over realizations of a derivation `dref` which match a specified
  [context](#pylightnix.types.Context). Sorting order is unspecified. """
  rgs:List[RRefGroup]=[]
  for rg in store_rrefs_(dref):
    context2=store_context(list(rg.values())[0], S)
    if context_eq(context,context2):
      rgs.append(rg)
  return rgs

def store_deref_(context_holder:RRef, dref:DRef, S=None)->List[RRefGroup]:
  return context_deref(store_context(context_holder,S),dref,S)

def store_deref(context_holder:RRef, dref:DRef, S=None)->RRefGroup:
  """ For any realization `context_holder` and it's dependency `dref`, `store_deref`
  queries the realization reference of this dependency.

  See also [build_deref](#pylightnix.core.build_deref)"""
  rgs=store_deref_(context_holder, dref, S)
  assert len(rgs)==1
  return rgs[0]

def store_buildtime(rref:RRef, S=None)->Optional[str]:
  """ Return the buildtime of the current RRef in a format specified by the
  [PYLIGHTNIX_TIME](#pylightnix.utils.PYLIGHTNIX_TIME) constant.

  [parsetime](#pylightnix.utils.parsetime) may be used to parse stings into
  UNIX-Epoch seconds.

  Buildtime is the time when the realization process has started. Some
  realizations may not provide this information. """
  return tryread(Path(join(store_rref2path(rref,S),'__buildtime__.txt')))

def store_tag(rref:RRef,S=None)->Tag:
  """ Realizations may be marked with a tag. By default the tag is set to be
  'out'. """
  return mktag(tryreadjson_def(Path(join(store_rref2path(rref,S),'group.json')),{}).get('tag','out'))

def store_group(rref:RRef,S=None)->Group:
  """ Return group identifier of the realization """
  return mkgroup(tryreadjson_def(Path(join(store_rref2path(rref,S),'group.json')),{}).get('group',rref))

def store_gc(keep_drefs:List[DRef],
             keep_rrefs:List[RRef],
             S:Optional[SPath]=None)->Tuple[Set[DRef],Set[RRef]]:
  """ Take roots which are in use and should not be removed. Return roots which
  are not used and may be removed. Actual removing is to be done by the user.

  Default location of `S` may be changed.

  See also [rmref](#pylightnix.bashlike.rmref)"""
  assert_store_initialized()
  keep_rrefs_=set(keep_rrefs)
  keep_drefs_=set(keep_drefs)
  closure_rrefs=store_deepdepRrefs(keep_rrefs_,S) | keep_rrefs_
  closure_drefs=store_deepdeps(keep_drefs_,S) | keep_drefs_ | {rref2dref(rref) for rref in closure_rrefs}
  remove_drefs=set()
  remove_rrefs=set()
  for dref in store_drefs(S):
    if dref not in closure_drefs:
      remove_drefs.add(dref)
    for rg in store_rrefs_(dref,S):
      for rref in rg.values():
        if rref not in closure_rrefs:
          remove_rrefs.add(rref)
  return remove_drefs,remove_rrefs


def store_instantiate(c:Config,S=None)->DRef:
  """ Place new instantiation into the storage. We attempt to do it atomically
  by moving the directory right into it's place.

  FIXME: Assert or handle possible (but improbable) hash collision (*)
  """
  assert_store_initialized()
  # c=cp.config
  assert_valid_config(c)
  assert_rref_deps(c)

  refname=config_name(c)
  dhash=config_hash(c)

  dref=mkdref(trimhash(dhash),refname)

  o=Path(mkdtemp(prefix=refname, dir=PYLIGHTNIX_TMP))
  with open(join(o,'config.json'), 'w') as f:
    f.write(config_serialize(c))

  filero(Path(join(o,'config.json')))
  drefpath=store_dref2path(dref,S)
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

def store_realize_tag(dref:DRef, l:Context, o:Path,
                      leader:Optional[Tuple[Tag,RRef]]=None, S=None)->RRef:
  """
  FIXME: Assert or handle possible but improbable hash collision (*)
  """
  c=store_config(dref,S)
  assert_valid_config(c)
  (dhash,nm)=undref(dref)

  assert isdir(o), (
     f"While realizing {dref}: Outpath is expected to be a path to existing "
     f"directory, but got {o}")

  for fn in PYLIGHTNIX_RESERVED:
    assert not isfile(join(o,fn)), (
       f"While realizing {dref}: output folder '{o}' contains file '{fn}'. "
       f"This name is reserved, please use another name. List of reserved "
       f"names: {PYLIGHTNIX_RESERVED}")

  with open(join(o,'context.json'), 'w') as f:
    f.write(context_serialize(l))

  if leader is not None:
    tag,group_rref=leader
    with open(join(o,'group.json'), 'w') as f:
      json_dump({'tag':tag,'group':group_rref},f)

  rhash=dirhash(o)
  rref=mkrref(trimhash(rhash),dhash,nm)
  rrefpath=store_rref2path(rref,S)
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

def store_realize_group(dref:DRef, l:Context, og:Dict[Tag,Path], S=None)->RRefGroup:
  rrefg={}
  rrefg[Tag('out')]=store_realize_tag(dref,l,og[Tag('out')],S=S)
  for tag,o in og.items():
    if tag!=Tag('out'):
      rrefg[tag]=store_realize_tag(dref,l,o,(tag,rrefg[Tag('out')]),S=S)
  return rrefg

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

def context_deref(context:Context, dref:DRef, S=None)->List[RRefGroup]:
  assert dref in context, (
      f"Context {context} doesn't declare {dref} among it's dependencies so we "
      f"can't dereference it." )
  return rrefs2groups(context[dref],S)

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
  - `m:Manager`: A Manager to update with a new derivation
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
  dref=store_instantiate(config,m.storage)
  if dref in m.builders:
    if not m.in_redefine:
      warning((f"Overwriting either the matcher or the realizer of derivation "
               f"'{dref}'. It could be intended (e.g. a result of `redefine`), "
               f"but now we see a different situation. Could it be  "
               f"a recursive call to `instantiate`?\n"
               f"Derivation config:\n{store_config_(dref)}"))

  def _promise_aware(realizer)->Realizer:
    def _realizer(S:SPath,dref:DRef,ctx:Context,rarg:RealizeArg)->List[Dict[Tag,Path]]:
      outgroups=realizer(S,dref,ctx,rarg)
      for key,refpath in config_promises(store_config_(dref,S),dref):
        for g in outgroups:
          assert_promise_fulfilled(key,refpath,g[Tag('out')])
      return outgroups
    return _realizer

  m.builders[dref]=Derivation(dref=dref,
                              matcher=matcher,
                              realizer=_promise_aware(realizer) if check_promises else realizer)
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
                          Tuple[Optional[List[RRefGroup]],bool],
                          List[RRefGroup]]

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
  to system path](#pylightnix.core.store_rref2path) of the folder which
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
  print('Available realizations:', [store_rref2path(rref) for rref in rrefs])
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
  res:List[RRefGroup]
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
  return groups2rrefs(res)

def realizeSeq(closure:Closure, force_interrupt:List[DRef]=[],
                                assert_realized:List[DRef]=[],
                                realize_args:Dict[DRef,RealizeArg]={})->RealizeSeqGen:
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
  target_deps=store_deepdeps([target_dref],S)
  for drv in closure.derivations:
    dref=drv.dref
    rrefgs:Optional[List[RRefGroup]]
    if dref in target_deps or dref==target_dref:
      dref_deps=store_deepdeps([dref],S)
      dref_context={k:v for k,v in context_acc.items() if k in dref_deps}
      if dref in force_interrupt_:
        rrefgs,abort=yield (S,dref,dref_context,drv,realize_args.get(dref,{}))
        if abort:
          return []
      else:
        rrefgs=drv.matcher(S,dref,dref_context)
      if rrefgs is None:
        assert dref not in assert_realized, (
          f"Stage '{dref}' was assumed to be already realized. "
          f"Unfortunately, it is not the case. Config:\n"
          f"{store_config(dref)}"
          )
        gpaths:List[Dict[Tag,Path]]=drv.realizer(S,dref,dref_context,realize_args.get(dref,{}))
        rrefgs_built=[store_realize_group(dref,dref_context,g,S) for g in gpaths]
        rrefgs_matched=drv.matcher(S,dref,dref_context)
        assert rrefgs_matched is not None, (
          f"Matcher of {dref} repeatedly asked the core to realize. "
          f"Probably, it's realizer doesn't work well with it's matcher. "
          f"The follwoing just-built RRefs were marked as unmatched: "
          f"{rrefgs_built}" )
        if (set(groups2rrefs(rrefgs_built)) & set(groups2rrefs(rrefgs_matched))) == set() and \
           (set(groups2rrefs(rrefgs_built)) | set(groups2rrefs(rrefgs_matched))) != set():
          warning(f"None of the newly obtained realizations of "
                  f"{dref} were matched by the matcher. To capture those "
                  f"realizations explicitly, try `matcher([exact(..)])`")
        rrefgs=rrefgs_matched
      context_acc=context_add(context_acc,dref,groups2rrefs(rrefgs))
  assert rrefgs is not None
  return rrefgs


def linkrref(rref:RRef,
             destdir:Optional[Path]=None,
             name:Optional[str]=None,
             withtime:bool=False,
             S=None)->Path:
  """ Helper function that creates a symbolic link to a particular realization
  reference. The link is created under the current directory by default or under
  the `destdir` directory.

  Create a symlink pointing to realization `rref`. Other arguments define
  symlink name and location. Informally,
  `{tgtpath}/{timeprefix}{name} --> $PYLIGHTNIX_STORE/{dref}/{rref}`.
  Overwrite existing symlinks. Folder named `tgtpath` should exist.
  """
  destdir_='.' if destdir is None else destdir
  name_:str=name if name is not None else (
    '_result-'+config_name(store_config(rref,S)) if destdir is None else
    'result-'+config_name(store_config(rref,S)))
  ts:Optional[str]=store_buildtime(rref,S) if withtime else None
  timetag_=f'{ts}_' if ts is not None else ''
  symlink=Path(join(destdir_,f"{timetag_}{name_}"))
  forcelink(Path(relpath(store_rref2path(rref,S), destdir_)), symlink)
  return symlink


def linkdref(dref:DRef,
             destdir:Optional[Path]=None,
             name:Optional[str]=None,
             S=None)->Path:
  destdir_='.' if destdir is None else destdir
  name_:str=name if name is not None else (
    '_result-'+config_name(store_config(dref,S)) if destdir is None else
    'result-'+config_name(store_config(dref,S)))
  symlink=Path(join(destdir_,name_))
  forcelink(Path(relpath(store_dref2path(dref,S), destdir_)), symlink)
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

  Only realizations which have [tag](#pylightnix.types.Tag) 'out' (which is a
  default tag name) participate in matching. After the matching, Pylightnix
  adds all non-'out' realizations which share [group](#pylightnix.types.Group)
  with at least one matched realization.

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
  def _matcher(S:SPath, dref:DRef, context:Context)->Optional[List[RRefGroup]]:
    # Find 'out' RRefs in each group
    grefs={gr[Tag('out')]:gr for gr in store_rrefs(dref,context,S)}

    # Match only among realizations tagged as 'out'
    keymap={rref:[k(rref,S) for k in keys] for rref in grefs.keys()}

    # Apply filters and filter outputs
    res:List[RRef]=sorted(filter(lambda rref: None not in keymap[rref], grefs.keys()),
                          key=lambda rref:keymap[rref], reverse=True)
    # Filter by range
    if rmin is not None:
      if not rmin<=len(res):
        return None
    if rmax is not None:
      if not len(res)<=rmax:
        assert not exclusive
        res=res[:rmax]

    # Return matched groups
    return [grefs[rref] for rref in res]
  return _matcher


def latest()->Key:
  def _key(rref:RRef,S=None)->Optional[Union[int,float,str]]:
    try:
      with open(join(store_rref2path(rref,S),'__buildtime__.txt'),'r') as f:
        t=parsetime(f.read())
        return float(0 if t is None else t)
    except OSError:
      return float(0)
  return _key

def exact(expected:List[RRef])->Key:
  def _key(rref:RRef,S=None)->Optional[Union[int,float,str]]:
    return 1 if rref in expected else None
  return _key

def best(filename:str)->Key:
  def _key(rref:RRef,S=None)->Optional[Union[int,float,str]]:
    try:
      with open(join(store_rref2path(rref,S),filename),'r') as f:
        return float(f.readline())
    except OSError:
      return float('-inf')
    except ValueError:
      return float('-inf')
  return _key


def texthash()->Key:
  def _key(rref:RRef,S=None)->Optional[Union[int,float,str]]:
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
  need_drefs=store_deepdeps(drefs,m.storage) | set(drefs)
  missing=list(need_drefs-have_drefs)
  assert len(missing)==0, (
    f"The following derivations don't have realizers associated with them:\n"
    f"{missing}\n"
    f"Did you mix DRefs from several `Manager` sessions?")

