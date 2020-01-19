from pylightnix.imports import (
    sha256, deepcopy, isdir, makedirs, join, json_dump, json_load, json_dumps,
    json_loads, isfile, relpath, listdir, rmtree, mkdtemp, replace, environ,
    split, re_match, ENOTEMPTY )
from pylightnix.utils import (
    dirhash, assert_serializable, assert_valid_dict, dicthash, scanref_dict,
    scanref_list, forcelink, timestring, datahash, slugify, splitpath,
    readjson, tryread )
from pylightnix.types import (
    Dict, List, Any, Tuple, Union, Optional, Iterable, IO, Path, Hash, DRef,
    RRef, RefPath, HashPart, Callable, Closure, Name, NamedTuple, Build,
    Config, ConfigAttrs, Derivation, Stage, Manager, Instantiator, Matcher,
    Realizer, Set )

#: *Do not change!*
#: Tracks the version of pylightnix storage
PYLIGHTNIX_STORE_VERSION = 1

#: `PYLIGHTNIX_ROOT` configures the root folder of pylightnix shared data folder.
#:
#: Default is `~/_pylightnix` / `/var/run/_pylightnix`.
#: Set `PYLIGHTNIX_ROOT` shell variable to overwrite.
PYLIGHTNIX_ROOT = environ.get('PYLIGHTNIX_ROOT', join(environ.get('HOME','/var/run'),'_pylightnix'))

# PYLIGHTNIX_LOGDIR = environ.get('PYLIGHTNIX_LOGDIR', join(PYLIGHTNIX_ROOT,'log'))

#: `PYLIGHTNIX_TMP` sets the location for temporary files and folders
#: Set `PYLIGHTNIX_TMP` shell variable to overwrite the default location.
PYLIGHTNIX_TMP = environ.get('PYLIGHTNIX_TMP', join(PYLIGHTNIX_ROOT,'tmp'))

#: `PYLIGHTNIX_STORE` sets the location of the main storage.
#:
#: By default, the store will be located in `$PYLIGHTNIX_ROOT/store-vXX` folder.
#: Set `PYLIGHTNIX_STORE` shell variable to overwrite the default location.
PYLIGHTNIX_STORE = join(PYLIGHTNIX_ROOT, f'store-v{PYLIGHTNIX_STORE_VERSION}')

#: Set the regular expression pattern for valid name characters.
PYLIGHTNIX_NAMEPAT = "[a-zA-Z0-9_-]"


#  ____       __
# |  _ \ ___ / _|___
# | |_) / _ \ |_/ __|
# |  _ <  __/  _\__ \
# |_| \_\___|_| |___/

def assert_valid_hash(h:Hash)->None:
  """ Asserts if it's `Hash` argument is ill-formed. """
  assert len(h)==64, f"HashPart should have length of 64, but len({h})=={len(h)}"
  for s in ['-','_','/']:
    assert s not in h, f"Invalid symbol '{s}' found in {h}"

def trimhash(h:Hash)->HashPart:
  """ Trim a hash to get `HashPart` objects which are used in referencing """
  return HashPart(h[:32])

def assert_valid_hashpart(hp:HashPart)->None:
  assert len(hp)==32, f"HashPart should have length of 32, but len({hp})=={len(hp)}"
  for s in ['-','_','/']:
    assert s not in hp, f"Invalid symbol '{s}' found in {hp}"

def assert_valid_dref(ref:str)->None:
  error_msg=(f'Value of {ref} is not a valid derivation reference! Expected '
             f'a string of form \'dref:HASH_HASH-name\'')
  assert ref[:5] == 'dref:', error_msg

def mkdref(dhash:HashPart, refname:Name)->DRef:
  assert_valid_hashpart(dhash)
  assert_valid_name(refname)
  return DRef('dref:'+dhash+'-'+refname)

def rref2dref(rref:RRef)->DRef:
  return mkdref(*unrref(rref)[1:])

def undref(r:DRef)->Tuple[HashPart, Name]:
  assert_valid_dref(r)
  return (HashPart(r[5:5+32]), Name(r[5+32+1:]))



def assert_valid_rref(ref:str)->None:
  error_msg=(f'Value of {ref} is not a valid instance reference! Expected '
             f'a string of form \'dref:HASH-HASH-name\'')
  assert ref[:5] == 'rref:', error_msg

def mkrref(rhash:HashPart, dhash:HashPart, refname:Name)->RRef:
  assert_valid_name(refname)
  assert_valid_hashpart(rhash)
  assert_valid_hashpart(dhash)
  return RRef('rref:'+rhash+'-'+dhash+'-'+refname)

def unrref(r:RRef)->Tuple[HashPart, HashPart, Name]:
  assert_valid_rref(r)
  return (HashPart(r[5:5+32]), HashPart(r[5+32+1:5+32+1+32]), Name(r[5+32+1+32+1:]))


def assert_valid_name(s:Name)->None:
  assert re_match(f"^{PYLIGHTNIX_NAMEPAT}+$", s), \
      f"Name {s} contains characters besides {PYLIGHTNIX_NAMEPAT}"


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

def assert_valid_config(c:Config):
  assert c is not None, "Expected `Config` object, but None was passed"
  assert_valid_name(config_name(c))
  assert_valid_dict(c.__dict__, 'Config')

def config_dict(c:Config)->dict:
  return deepcopy(c.__dict__)

def config_ro(c:Config)->Any:
  return ConfigAttrs(c.__dict__)

def config_serialize(c:Config)->str:
  return json_dumps(config_dict(c), indent=4)

def config_hash(c:Config)->Hash:
  return datahash([config_serialize(c)])

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

def assert_valid_refpath(refpath:RefPath)->None:
  error_msg=(f'Value of type {type(refpath)} is not a valid refpath! Expected '
             f'list of strings starting from a d-reference, but actual value '
             f'is "{refpath}"')
  assert len(refpath)>0, error_msg
  assert_valid_dref(refpath[0])

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

# def store_refpath2path(r:RefPath)->Path:
#   assert_valid_refpath(r)
#   return Path(join(store_dref2path(r[0]),*r[1:]))

def mkrefpath(r:DRef, items:List[str]=[])->RefPath:
  """ Constructs a RefPath out of a reference `ref` and a path within the node """
  assert_valid_dref(r)
  return RefPath([str(r)]+items)

def store_config(r:DRef)->Config:
  assert_valid_dref(r)
  return Config(readjson(join(store_dref2path(r),'config.json')))

# def store_program(r:DRef)->Program:
#   assert_valid_dref(r)
#   return Program(readjson(join(store_dref2path(r),'program.json')))

def store_closure(r:RRef)->Closure:
  assert_valid_rref(r)
  return readjson(join(store_rref2path(r),'closure.json'))

def store_config_ro(r:DRef)->Any:
  return config_ro(store_config(r))


def store_deps(refs:List[DRef])->List[DRef]:
  """ Return a list of reference's dependencies, that is all the references
  found in current ref's `Config` """
  acc=set()
  for r in refs:
    acc.update(config_deps(store_config(r)))
  return list(acc)


def store_deepdeps(roots:List[DRef])->List[DRef]:
  """ Return an exhaustive list of dependencies of the `roots`. `roots`
  themselves are also included. """
  frontier=set(store_deps(roots))
  processed=set()
  while frontier:
    ref = frontier.pop()
    processed.add(ref)
    for dep in store_deps([ref]):
      if not dep in processed:
        frontier.add(dep)
  return list(processed)


def store_link(ref:DRef, tgtpath:Path, name:str, withtime=True)->None:
  """ Creates a link pointing to node `ref` into directory `tgtpath` """
  assert_valid_dref(ref)
  assert isdir(tgtpath), f"store_link(): `tgt` dir '{tgtpath}' doesn't exist"
  ts:Optional[str]
  if withtime:
    ts=tryread(Path(join(store_dref2path(ref),'_timestamp_.txt')))
    if ts is None:
      print(f"Warning: no timestamp for {ref}, probably because of old version of Pylightnix")
  else:
    ts=None
  timeprefix=f'{ts}_' if ts is not None else ''
  forcelink(Path(relpath(store_dref2path(ref), tgtpath)),
            Path(join(tgtpath,f'{timeprefix}{name}')))

def store_drefs()->Iterable[DRef]:
  for dirname in listdir(PYLIGHTNIX_STORE):
    yield mkdref(HashPart(dirname[:32]), Name(dirname[32+1:]))


def store_rrefs(dref:DRef)->Iterable[RRef]:
  (dhash,nm)=undref(dref)
  drefpath=store_dref2path(dref)
  for f in listdir(drefpath):
    if isdir(join(drefpath,f)):
      yield mkrref(HashPart(f), dhash, nm)

def store_deref(rref:RRef, dref:DRef)->RRef:
  return store_closure(rref)[dref]

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


def mkbuild(dref:DRef, closure:Closure)->Build:
  c=store_config(dref)
  assert_valid_config(c)
  timeprefix=timestring()
  outpath=Path(mkdtemp(prefix=f'{timeprefix}_{config_hash(c)[:8]}_', dir=PYLIGHTNIX_TMP))
  return Build(c, closure, timeprefix, outpath)

def build_config(b:Build)->Config:
  return b.config

def build_closure(b:Build)->Closure:
  return b.closure

def build_config_ro(m:Build)->Any:
  return config_ro(build_config(m))

def build_outpath(m:Build)->Path:
  return m.outpath

def build_name(b:Build)->Name:
  return Name(config_name(build_config(b)))

def build_rref(b:Build, dref:DRef)->RRef:
  rref=b.closure.get(dref)
  assert rref is not None, f"Unable to deref {dref} while building {build_name(b)}"
  return rref

def build_deref(b:Build, refpath:RefPath)->Path:
  assert_valid_refpath(refpath)
  return Path(join(store_rref2path(build_rref(b, refpath[0])), *refpath[1:]))

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
      pass # Derivation already exists
  return dref

def build_realize(dref:DRef, b:Build)->RRef:
  o=build_outpath(b)
  c=build_config(b)
  l=build_closure(b)
  (dhash,nm)=undref(dref)

  with open(join(o,'closure.json'), 'w') as f:
    f.write(closure_serialize(l))

  rhash=dirhash(o)
  rref=mkrref(trimhash(rhash),dhash,nm)
  replace(o,store_rref2path(rref))
  return rref


#   ____ _
#  / ___| | ___  ___ _   _ _ __ ___
# | |   | |/ _ \/ __| | | | '__/ _ \
# | |___| | (_) \__ \ |_| | | |  __/
#  \____|_|\___/|___/\__,_|_|  \___|


def mkclosure()->Closure:
  return {}

def assert_valid_closure(c:Closure)->None:
  assert_serializable(c)
  for dref,rref in c.items():
    assert_valid_dref(dref)
    assert_valid_rref(rref)


def closure_eq(a:Closure,b:Closure)->bool:
  return json_dumps(a)==json_dumps(b)

def closure_add(closure:Closure, dref:DRef, rref:RRef)->Closure:
  rref2=closure.get(dref)
  if rref2:
    assert rref==rref2, \
      ( f"Attempting to re-introduce DRef {dref} to closure with "
        f"different realization.\n"
        f" * Old realization: {rref2}\n"
        f" * New realization: {rref}\n" )
  else:
    closure[dref]=rref
  return closure

def closure_serialize(c:Closure)->str:
  assert_valid_closure(c)
  return json_dumps(c, indent=4)

#  _____           _                _
# |_   _|__  _ __ | | _____   _____| |
#   | |/ _ \| '_ \| |/ _ \ \ / / _ \ |
#   | | (_) | |_) | |  __/\ V /  __/ |
#   |_|\___/| .__/|_|\___| \_/ \___|_|
#           |_|


def manage(m:Manager, inst:Instantiator, matcher:Matcher, realizer:Realizer)->DRef:
  dref=build_instantiate(inst())
  m.builders.append(Derivation(dref,matcher,realizer))
  return dref


def instantiate(stage:Stage)->List[Derivation]:
  m=Manager()
  stage(m)
  visited:Set[DRef]=set()
  for (dref,_,_) in m.builders:
    assert dref not in visited, \
      f"Multiple realizers for DRef {dref}"
    visited.add(dref)
  return m.builders


def realize(stage:Stage, force_rebuild:List[DRef]=[])->RRef:
  closure:Closure={}
  rref:Optional[RRef]=None
  force_rebuild_:Set[DRef]=set(force_rebuild)
  for (dref,matcher,realizer) in instantiate(stage):
    c=store_config(dref)
    n=config_name(c)
    if dref in force_rebuild_:
      rref = None
    else:
      rref=matcher(dref,closure)
    if not rref:
      rreftmp=build_realize(dref,realizer(dref,closure))
      rref=matcher(dref,closure)
      assert rref is not None
    closure=closure_add(closure,dref,rref)
  assert rref is not None
  return rref

def only(dref:DRef, closure:Closure)->Optional[RRef]:
  matching=[]
  for rref in store_rrefs(dref):
    closure2=store_closure(rref)
    if closure_eq(closure,closure2):
      matching.append(rref)
  if len(matching)==0:
    return None
  elif len(matching)==1:
    return matching[0]
  else:
    assert False, (
        f"only() assumes that {dref} has a single realization under"
        f"closure {closure}, but is has many:\n{matching}" )



