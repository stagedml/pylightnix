from pylightnix.imports import (
    sha256, deepcopy, isdir, makedirs, join, json_dump, json_load, json_dumps,
    json_loads, isfile, relpath, listdir, rmtree, mkdtemp, replace, environ,
    split, re_match, ENOTEMPTY, get_ident, contextmanager, OrderedDict )
from pylightnix.utils import (
    dirhash, assert_serializable, assert_valid_dict, dicthash, scanref_dict,
    scanref_list, forcelink, timestring, datahash, slugify,
    readjson, tryread, encode )
from pylightnix.types import (
    Dict, List, Any, Tuple, Union, Optional, Iterable, IO, Path, Hash, DRef,
    RRef, RefPath, HashPart, Callable, Context, Name, NamedTuple, Build,
    Config, ConfigAttrs, Derivation, Stage, Manager, Instantiator, Matcher,
    Realizer, Set, Closure )

#: *Do not change!*
#: Tracks the version of pylightnix storage
PYLIGHTNIX_STORE_VERSION = 1

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

def config_ro(c:Config)->Any:
  return ConfigAttrs(c.__dict__)

def config_serialize(c:Config)->str:
  return json_dumps(config_dict(c), indent=4)

def config_hash(c:Config)->Hash:
  return datahash([encode(config_serialize(c))])

def config_name(c:Config)->Name:
  """ Return short human-readable name of a config """
  return mkname(config_dict(c).get('name','unnamed'))

def config_deps(c:Config)->List[DRef]:
  return list(set(scanref_dict(config_dict(c))[0]))

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

def store_initialize(exist_ok:bool=True):
  print(f"Initializing {PYLIGHTNIX_STORE}")
  makedirs(PYLIGHTNIX_STORE, exist_ok=exist_ok)
  makedirs(PYLIGHTNIX_TMP, exist_ok=True)
  assert_store_initialized()


def store_dref2path(r:DRef)->Path:
  (dhash,nm)=undref(r)
  return Path(join(PYLIGHTNIX_STORE,dhash+'-'+nm))

def store_rref2path(r:RRef)->Path:
  (rhash,dhash,nm)=unrref(r)
  return Path(join(PYLIGHTNIX_STORE,dhash+'-'+nm,rhash))

def mkrefpath(r:DRef, items:List[str]=[])->RefPath:
  """ Constructs a RefPath out of a reference `ref` and a path within the node """
  assert_valid_dref(r)
  return RefPath([str(r)]+items)

def store_config(r:Union[DRef,RRef])->Config:
  if r[:4]=='rref':
    return Config(readjson(join(store_dref2path(rref2dref(RRef(r))),'config.json')))
  elif r[:4]=='dref':
    return Config(readjson(join(store_dref2path(DRef(r)),'config.json')))
  else:
    assert False, r"Invalid reference type {r}. Expected either RRef or DRef."

def store_context(r:RRef)->Context:
  assert_valid_rref(r)
  return readjson(join(store_rref2path(r),'context.json'))

def store_config_ro(r:Union[DRef,RRef])->Any:
  return config_ro(store_config(r))

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
    yield mkdref(HashPart(dirname[:32]), Name(dirname[32+1:]))

def store_rrefs_(dref:DRef)->Iterable[RRef]:
  (dhash,nm)=undref(dref)
  drefpath=store_dref2path(dref)
  for f in listdir(drefpath):
    if isdir(join(drefpath,f)):
      yield mkrref(HashPart(f), dhash, nm)

def store_rrefs(dref:DRef, context:Context)->Iterable[RRef]:
  """ `store_rrefs` iterates over those ralizations of a derivation `dref`,
  that fit into particular [context]($pylightnix.types.Context). """
  for rref in store_rrefs_(dref):
    context2=store_context(rref)
    if context_eq(context,context2):
      yield rref

def store_deref(rref:RRef, dref:DRef)->RRef:
  """ For any realization `rref` and it's dependency `dref`, `store_deref`
  queryies the realization reference of this dependency.

  See also [build_deref](#pylightnix.core.build_deref)"""
  c = store_context(rref)
  assert dref in c, (
      f"Realization {rref} doesn't declare {dref} among it's dependencies so we "
      f"can't dereference it." )
  return c[dref]

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


#  ____        _ _     _
# | __ ) _   _(_) | __| |
# |  _ \| | | | | |/ _` |
# | |_) | |_| | | | (_| |
# |____/ \__,_|_|_|\__,_|


def mkbuild(dref:DRef, context:Context)->Build:
  c=store_config(dref)
  assert_valid_config(c)
  timeprefix=timestring()
  outpath=Path(mkdtemp(prefix=f'{timeprefix}_{config_hash(c)[:8]}_', dir=PYLIGHTNIX_TMP))
  return Build(dref, context, timeprefix, outpath)

def build_config(b:Build)->Config:
  """ Return the [Config](#pylightnix.types.Config) object of the realization
  being built. """
  return store_config(b.dref)

def build_context(b:Build)->Context:
  """ Return the [Context](#pylightnix.types.Context) object of the realization
  being built. """
  return b.context

def build_config_ro(m:Build)->Any:
  return config_ro(build_config(m))

def build_outpath(m:Build)->Path:
  """ Return the output path of the realization being built. Output path is a
  path to valid temporary folder where user may put various build artifacts.
  Later this folder becomes a realization. """
  return m.outpath

def build_name(b:Build)->Name:
  """ Return the name of a derivation being built. """
  return Name(config_name(build_config(b)))

def build_deref(b:Build, dref:DRef)->RRef:
  """ For any [realization](#pylightnix.core.realize) process described with
  it's [b:Build](#pylightnix.types.Build) handler, `build_deref` queries a
  realization of a dependency `dref`.

  `build_deref` is designed to be called by
  [Realizers](#pylightnix.types.Realizer), where the final `rref` is not yet
  known.  In other cases, [store_deref](#pylightnix.core.store_deref) should be
  used.
  """
  rref=b.context.get(dref)
  assert rref is not None, (
      f"Unable to deref {dref} while realizing {b.dref}. Make sure that first link "
      f"is listed in the configurations of the second link or one of it's "
      f"dependencies" )
  return rref

def build_deref_path(b:Build, refpath:RefPath)->Path:
  assert_valid_refpath(refpath)
  return Path(join(store_rref2path(build_deref(b, refpath[0])), *refpath[1:]))

def build_instantiate(c:Config)->DRef:
  assert_store_initialized()

  refname=config_name(c)
  dhash=config_hash(c)

  dref=mkdref(trimhash(dhash),refname)

  o=Path(mkdtemp(prefix=refname, dir=PYLIGHTNIX_TMP))
  with open(join(o,'config.json'), 'w') as f:
    f.write(config_serialize(c))

  try:
    replace(o, store_dref2path(dref))
  except OSError as err:
    if err.errno == ENOTEMPTY:
      pass # Exactly matching derivation already exists
    else:
      raise
  return dref

def build_realize(dref:DRef, l:Context, o:Path)->RRef:
  c=store_config(dref)
  (dhash,nm)=undref(dref)

  assert not isfile(join(o,'context.json')), (
     f"While realizing {dref}: one of build artifacts has name 'context.json'. "
     f"This name is reserved, please rename the artifact.")
  with open(join(o,'context.json'), 'w') as f:
    f.write(context_serialize(l))

  rhash=dirhash(o)
  rref=mkrref(trimhash(rhash),dhash,nm)

  try:
    replace(o,store_rref2path(rref))
  except OSError as err:
    if err.errno == ENOTEMPTY:
      pass # Exactly matching realization already exists
    else:
      raise
  return rref


#   ____ _
#  / ___| | ___  ___ _   _ _ __ ___
# | |   | |/ _ \/ __| | | | '__/ _ \
# | |___| | (_) \__ \ |_| | | |  __/
#  \____|_|\___/|___/\__,_|_|  \___|


def mkcontext()->Context:
  return {}


def context_eq(a:Context,b:Context)->bool:
  return json_dumps(a)==json_dumps(b)

def context_add(context:Context, dref:DRef, rref:RRef)->Context:
  rref2=context.get(dref)
  if rref2:
    assert rref==rref2, (
        f"Attempting to re-introduce DRef {dref} to context with "
        f"different realization.\n"
        f" * Old realization: {rref2}\n"
        f" * New realization: {rref}\n" )
  else:
    context[dref]=rref
  return context

def context_serialize(c:Context)->str:
  assert_valid_context(c)
  return json_dumps(c, indent=4)

#  _____           _                _
# |_   _|__  _ __ | | _____   _____| |
#   | |/ _ \| '_ \| |/ _ \ \ / / _ \ |
#   | | (_) | |_) | |  __/\ V /  __/ |
#   |_|\___/| .__/|_|\___| \_/ \___|_|
#           |_|

def mkdrv(m:Manager, inst:Instantiator, matcher:Matcher, realizer:Realizer)->DRef:
  dref=build_instantiate(inst())
  if dref in m.builders:
    print(f"Overwriting realizer for {dref} with config:\n{config_dict(store_config(dref))}" )
  m.builders[dref]=Derivation(dref,matcher,realizer)
  return dref

#! `PYLIGHTNIX_RECURSION` encodes the state of recursion manager, do not modify!
PYLIGHTNIX_RECURSION:Dict[Any,List[str]]={}

@contextmanager
def recursion_manager(funcname:str):
  global PYLIGHTNIX_RECURSION
  if get_ident() not in PYLIGHTNIX_RECURSION:
    PYLIGHTNIX_RECURSION[get_ident()]=[]
  error_msg = (f"Recursion manager alerted while in {funcname}. "
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

def instantiate_(stage:Stage, m:Manager)->Closure:
  with recursion_manager('instantiate'):
    target_dref=stage(m)
    return Closure(target_dref,list(m.builders.values()))

def instantiate(stage:Stage)->Closure:
  """ `instantiate` takes the [Stage](#pylightnix.types.Stage) function and
  produces corresponding derivation object. Resulting list contains derivation
  of the current stage (in it's last element), preceeded by the derivations of
  all it's dependencies.

  Instantiation is the equivalent of type-checking in the typical compiler's
  pipeline.

  User-defined [Instantiators](pylightnix.types.Instantiator) calculate stage
  configs during the instantiation. This calculations fall under certain
  restrictions. In particular, it shouldn't start new instantiations or
  realizations recursively, and it shouldn't access realization objects in the
  storage.
  """
  return instantiate_(stage, Manager())

def realize(closure:Closure, force_rebuild:List[DRef]=[])->RRef:
  """ `realize` builds a realization of a derivation by executing
  [Realizer](#pylightnix.types.Realizer) that is a user-defined Python code for
  producing build artifacts.

  During this process, Realizer may access:
  - The configuration of derivation being built and configurations of all it's
    dependencies.
  - The realizations of all it's dependencies (and thus, their build
    artifacts).

  Return value of realization is a [reference to new
  realization](#pylightnix.types.RRef) which could be
  later [converted to system path](#pylightnix.core.store_rref2path)
  to access build artifacts. """
  assert_valid_closure(closure)
  with recursion_manager('realize'):
    context:Context={}
    rref:Optional[RRef]=None
    force_rebuild_:Set[DRef]=set(force_rebuild)
    target_dref=closure.dref
    target_deps=store_deepdeps([target_dref])
    for (dref,matcher,realizer) in closure.derivations:
      if dref in target_deps or dref==target_dref:
        c=store_config(dref)
        if dref in force_rebuild_:
          rref=None
        else:
          rref=matcher(dref,context)
        if not rref:
          rreftmp=build_realize(dref,context,realizer(dref,context))
          print(context)
          rref=matcher(dref,context)
          assert rref is not None
        context=context_add(context,dref,rref)
    assert rref is not None
    return rref

def only(dref:DRef, context:Context)->Optional[RRef]:
  matching=[]
  for rref in store_rrefs(dref, context):
    matching.append(rref)
  if len(matching)==0:
    return None
  elif len(matching)==1:
    return matching[0]
  else:
    assert False, (
        f"only() assumes that {dref} has 0 or 1 realizations under"
        f"context {context}, but in fact it has many:\n{matching}" )

def mksymlink(rref:RRef, tgtpath:Path, name:str, withtime=True)->Path:
  """ Create a symlink pointing to realization `rref`. Other arguments define
  symlink name and location. Informally,
  `{tgtpath}/{timeprefix}{name} --> $PYLIGHTNIX_STORE/{rref2dref(rref)}/{rref}` """
  assert_valid_rref(rref)
  assert isdir(tgtpath), f"store_link(): `tgt` dir '{tgtpath}' doesn't exist"
  ts:Optional[str]
  if withtime:
    ts=tryread(Path(join(store_rref2path(rref),'_timestamp_.txt')))
  else:
    ts=None
  timeprefix=f'{ts}_' if ts is not None else ''
  symlink=Path(join(tgtpath,f'{timeprefix}{name}'))
  forcelink(Path(relpath(store_rref2path(rref), tgtpath)), symlink)
  return symlink


def assert_valid_refpath(refpath:RefPath)->None:
  error_msg=(f'Value of type {type(refpath)} is not a valid refpath! Expected '
             f'list of strings starting from a d-reference, but actual value '
             f'is "{refpath}"')
  assert len(refpath)>0, error_msg
  assert_valid_dref(refpath[0])

def assert_valid_config(c:Config):
  assert c is not None, "Expected `Config` object, but None was passed"
  assert_valid_name(config_name(c))
  assert_valid_dict(c.__dict__, 'Config')

def assert_valid_name(s:Name)->None:
  assert re_match(f"^{PYLIGHTNIX_NAMEPAT}+$", s), \
      f"Name {s} contains characters besides {PYLIGHTNIX_NAMEPAT}"

def assert_valid_rref(ref:str)->None:
  error_msg=(f'Value of {ref} is not a valid instance reference! Expected '
             f'a string of form \'dref:HASH-HASH-name\'')
  assert ref[:5] == 'rref:', error_msg

def assert_valid_hashpart(hp:HashPart)->None:
  assert len(hp)==32, f"HashPart should have length of 32, but len({hp})=={len(hp)}"
  for s in ['-','_','/']:
    assert s not in hp, f"Invalid symbol '{s}' found in {hp}"

def assert_valid_dref(ref:str)->None:
  error_msg=(f'Value of {ref} is not a valid derivation reference! Expected '
             f'a string of form \'dref:HASH_HASH-name\'')
  assert ref[:5] == 'dref:', error_msg


def assert_valid_hash(h:Hash)->None:
  """ Asserts if it's `Hash` argument is ill-formed. """
  assert len(h)==64, f"HashPart should have length of 64, but len({h})=={len(h)}"
  for s in ['-','_','/']:
    assert s not in h, f"Invalid symbol '{s}' found in {h}"

def assert_valid_context(c:Context)->None:
  assert_serializable(c)
  for dref,rref in c.items():
    assert_valid_dref(dref)
    assert_valid_rref(rref)

def assert_valid_closure(closure:Closure)->None:
  assert len(closure.derivations)>0, \
      "Closure can not be empty"
  assert closure.dref in [d.dref for d in closure.derivations], \
      "Closure should contain target derivation"

