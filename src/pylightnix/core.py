from pylightnix.imports import (
    sha256, deepcopy, isdir, makedirs, join, json_dump, json_load, json_dumps,
    json_loads, isfile, relpath, listdir, rmtree, mkdtemp, replace, environ,
    split, re_match )
from pylightnix.utils import (
    dirhash, assert_serializable, assert_valid_dict, dicthash, scanref_dict,
    scanref_list, forcelink, timestring, datahash, slugify, splitpath,
    readjson, tryread )
from pylightnix.types import (
    Dict, List, Any, Tuple, Union, Optional, Iterable, IO, Path, Hash, DRef,
    RRef, Ref, RefPath, HashPart, Callable, Closure, Name )

PYLIGHTNIX_STORE_VERSION = 1
PYLIGHTNIX_ROOT:str = environ.get('PYLIGHTNIX_ROOT', join(environ.get('HOME','/var/run'),'_pylightnix'))
PYLIGHTNIX_LOGDIR:str = environ.get('PYLIGHTNIX_LOGDIR', join(PYLIGHTNIX_ROOT,'log'))
PYLIGHTNIX_TMP:str = environ.get('PYLIGHTNIX_TMP', join(PYLIGHTNIX_ROOT,'tmp'))
PYLIGHTNIX_STORE:str = join(PYLIGHTNIX_ROOT, f'store-v{PYLIGHTNIX_STORE_VERSION}')
PYLIGHTNIX_NAMEPAT:str = "[a-zA-Z0-9_-]"


#  ____       __
# |  _ \ ___ / _|___
# | |_) / _ \ |_/ __|
# |  _ <  __/  _\__ \
# |_| \_\___|_| |___/

def assert_valid_hash(h:Hash)->None:
  assert len(h)==64, f"HashPart should have length of 64, but len({h})=={len(h)}"
  for s in ['-','_','/']:
    assert s not in h, f"Invalid symbol '{s}' found in {h}"

def trimhash(h:Hash)->HashPart:
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

def mkdrefR(rref:RRef)->DRef:
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


# ____
# |  _ \ _ __ ___   __ _ _ __ __ _ _ __ ___
# | |_) | '__/ _ \ / _` | '__/ _` | '_ ` _ \
# |  __/| | | (_) | (_| | | | (_| | | | | | |
# |_|   |_|  \___/ \__, |_|  \__,_|_| |_| |_|
#                  |___/

class Program:
  """ Program contains an information of non-determenistic operations applied
  to a `Config`.

  Currently it is represented with a list of operation names, with possible
  arguments. Operation names and arguments should be JSON-serializable
  """
  def __init__(self, ops:list=[]):
    self.ops:List[Tuple[str,Any]]=ops

def program_add(p:Program, op:str, arg:Any=[])->Program:
  """ Add new operation to a program. Builds new program object """
  assert_serializable({'op':op,'arg':arg}, "op/arg")
  p2=deepcopy(p)
  p2.ops.append((op,arg))
  return p2

def program_serialize(p:Program)->str:
  assert_serializable(p.ops, "p.ops")
  return json_dumps(p.ops, indent=4)

def program_hash(p:Program)->Hash:
  """ Calculate the hashe of a program """
  return datahash([program_serialize(p)])

  # string=";".join([f'{nm}({str(args)})' for nm,args in p.ops if nm[0]!='_'])
  # return Hash(sha256(string.encode('utf-8')).hexdigest())


#   ____             __ _
#  / ___|___  _ __  / _(_) __ _
# | |   / _ \| '_ \| |_| |/ _` |
# | |__| (_) | | | |  _| | (_| |
#  \____\___/|_| |_|_| |_|\__, |
#                         |___/

class ConfigAttrs(dict):
  """ Helper object allowing to access dict fields as attributes """
  __getattr__ = dict.__getitem__ # type:ignore


class Config:
  """ Config is a JSON-serializable configuration object. It should match the
  requirements of `assert_valid_config`. Tupically, it's __dict__ should
  contain only either simple Python types (strings, bool, ints, floats), lists
  or dicts. No tuples, no `np.float32`, no functions. Fields with names
  starting from '_' are may be added after construction, but they are not
  preserved during the serialization."""
  def __init__(self, d:dict):
    assert_valid_dict(d,'dict')
    # uf=[x for x in d if len(x)>0 and x[0]=='_']
    # assert len(uf)==0, \
    #     (f"Config shouldn't initially contain fields starting with "
    #      f"underscopes '_'. Such filed should be added explicitly, "
    #      f"if needed. Got {uf}.")
    self.__dict__=deepcopy(d)

def mkconfig(d:dict)->Config:
  return Config(d)

def assert_valid_config(c:Config):
  assert c is not None, 'Expected `Config` object, but None was passed'
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

def store_program(r:DRef)->Program:
  assert_valid_dref(r)
  return Program(readjson(join(store_dref2path(r),'program.json')))

def store_closure(r:RRef)->Closure:
  assert_valid_rref(r)
  return readjson(join(store_rref2path(r),'closure.json'))

def store_config_ro(r:DRef)->Any:
  return config_ro(store_config(r))


def store_deps(r:DRef)->List[DRef]:
  """ Return a list of reference's dependencies, that is all the other references
  found in current ref's config and program """
  return config_deps(store_config(r))


def store_deepdeps(roots:List[DRef])->List[DRef]:
  """ Return an exhaustive list of dependencies of the `roots`. `roots`
  themselves are also included. """
  frontier=set(roots)
  processed=set()
  while frontier:
    ref = frontier.pop()
    processed.add(ref)
    for dep in store_deps(ref):
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


def store_gc(refs_in_use:List[DRef])->List[DRef]:
  """ Take roots which are in use and should not be removed. Return roots which
  are not used and may be removed. Actual removing is to be done by user-defined
  application. """
  assert_store_initialized()
  to_delete=[]
  roots_with_deps=store_deepdeps(refs_in_use)
  for dref in store_drefs():
    if not dref in roots_with_deps:
      to_delete.append(dref)
  return to_delete

#
#  ____        _ _     _
# | __ ) _   _(_) | __| |
# |  _ \| | | | | |/ _` |
# | |_) | |_| | | | (_| |
# |____/ \__,_|_|_|\__,_|


class Build:
  """ Build tracks the process of building storage nodes.

  Lifecycle of a model starts from its creation from JSON-serializable
  `Config`.

  After the model is created, users typically want to perform non-determenistic
  operations on it. To make the model abstraction aware of it, users have to
  update the _state_ of the model, which is a combination of `config`,
  `program` and `protocol` field.  The separation of state into `config` and
  `program` is not strictly important, but we hope it will help us to build a
  more user-friendly search system. We encourage users to keep config immutable
  after it was passed to model, and use `program` to track changes.  During
  those operations, users are to save various artifacts into temporary folder
  as returned by `build_outpath(m)` function.

  Note, that the rational behind `protocol` is unclear, maybe it should be
  moved into userland code completely.

  Finally, users typically call `build_save` which finishes the node creation,
  'seals' the node with a hash and sets the `storedir` field.  The storage item
  is believed to be immutable (but nothing special is done to enforce this
  restriction). `build_storelink` may be used to drop a symlink to this node
  into user-specified folder """

  def __init__(self, config:Config, closure:Closure, timeprefix:Optional[str]=None):
    assert_valid_config(config)
    self.timeprefix:str = timestring() if timeprefix is None else timeprefix
    self.config:Config = config
    self.program:Program = Program([])
    # self.protocol:Protocol = []
    self.outprefix:str = f'{self.timeprefix}_{config_hash(config)[:8]}_'
    self.outpath:Path = Path(mkdtemp(prefix=self.outprefix, dir=PYLIGHTNIX_TMP))
    self.closure:Closure=closure

  def get_whash(self)->Hash:
    return dirhash(build_outpath(self))

def mkbuild(dref:DRef, closure:Closure)->Build:
  return Build(store_config(dref), closure)

def build_config(b:Build)->Config:
  return b.config

def build_closure(b:Build)->Closure:
  return b.closure

def build_config_ro(m:Build)->Any:
  return config_ro(build_config(m))

def build_outpath(m:Build)->Path:
  return m.outpath

# def build_lasthash(m:Build)->Optional[Hash]:
#   assert m.protocol is not None
#   if len(m.protocol) == 0:
#     return None
#   else:
#     return m.protocol[-1][1]

def build_name(b:Build)->Name:
  return Name(config_name(build_config(b)))

# def protocol_add(m:Build, name:str, arg:Any=[], result:Any=[], expect_wchange:bool=True)->None:
#   assert_serializable(name,'name')
#   assert_serializable(arg,'arg')
#   assert_serializable(result,'result')
#   new_whash=m.get_whash()
#   old_whash=build_lasthash(m)
#   if expect_wchange:
#     assert new_whash != old_whash, \
#         (f"Pylightnix sanity check: Operation was marked as parameter-changing,"
#          f"but Build parameters didn't change their hashes as expected."
#          f"Both hashes are {new_whash}.")
#   else:
#     assert new_whash == old_whash or (old_whash is None), \
#         (f"Pylightnix sanity check: Operation was marked as"
#          f"non-paramerer-changing, but Build parameters were in fact changed by"
#          f"something. Expected {old_whash}, got {new_whash}.")
#   c=build_config(m)
#   m.program.ops.append((name, arg))
#   m.protocol.append((name, new_whash, result))


def build_rref(b:Build, dref:DRef)->RRef:
  rref=b.closure.get(dref)
  assert rref is not None, f"Unable to deref {dref} while building {build_name(b)}"
  return rref

def build_deref(b:Build, refpath:RefPath)->Path:
  assert_valid_refpath(refpath)
  return Path(join(store_rref2path(build_rref(b, refpath[0])), *refpath[1:]))


#  ___                       _   _
# / _ \ _ __   ___ _ __ __ _| |_(_) ___  _ __  ___
#| | | | '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \/ __|
#| |_| | |_) |  __/ | | (_| | |_| | (_) | | | \__ \
# \___/| .__/ \___|_|  \__,_|\__|_|\___/|_| |_|___/
#      |_|


def build_instantiate(c:Config)->DRef:
  assert_store_initialized()

  refname=config_name(c)
  dhash=config_hash(c)

  dref=mkdref(trimhash(dhash),refname)

  o=Path(mkdtemp(prefix=refname, dir=PYLIGHTNIX_TMP))
  with open(join(o,'config.json'), 'w') as f:
    f.write(config_serialize(c))

  replace(o, store_dref2path(dref))
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

##################
## Closure
##################


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

##################
## Manager
##################


class Manager:
  def __init__(self):
    self.builders:List[Tuple[DRef, Callable[[DRef,Closure],Build], Callable[[DRef, Closure],Optional[RRef]]]]=[]


def manage(m:Manager, finstantiate, frealize, fselect)->DRef:
  dref=build_instantiate(finstantiate())
  m.builders.append((dref,frealize,fselect))
  return dref

# def typecheck(stage:Callable[[Manager],DRef])
#   print('Going to build')
#   for (dref,builder,search) in m.builders:
#     c=store_config(dref)
#     n=config_name(c)
#     print(n)


def emerge(stage:Callable[[Manager],DRef])->RRef:
  m=Manager()
  stage(m)

  closure:Closure={}
  rref:Optional[RRef]=None
  for (dref,frealize,fsearch) in m.builders:
    c=store_config(dref)
    n=config_name(c)
    print(n)
    rref=fsearch(dref,closure)
    if not rref:
      b=frealize(dref,closure)
      rreftmp=build_realize(dref,b)
      rref=fsearch(dref,closure)
      assert rref is not None
    closure=closure_add(closure,dref,rref)
  assert rref is not None
  return rref


##################
## Searches
##################

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
    assert False, "Multiple matches"



