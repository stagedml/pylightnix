from pylightnix.imports import (
    sha256, deepcopy, isdir, makedirs, join, json_dump, json_load, json_dumps,
    json_loads, isfile, relpath, listdir, rmtree, mkdtemp, replace, environ,
    split )
from pylightnix.utils import (
    dhash, assert_serializable, assert_valid_dict, dicthash, scanref_dict,
    scanref_list, forcelink, timestring, datahash, slugify, splitpath, readjson
    )
from pylightnix.types import (
    List, Any, Tuple, Union, Optional, Iterable, IO, Path, Hash, DRef, RRef, Ref, RefPath,
    Protocol, HashPart )

PYLIGHTNIX_STORE_VERSION = 1
PYLIGHTNIX_ROOT:str = environ.get('PYLIGHTNIX_ROOT', join(environ.get('HOME','/var/run'),'_pylightnix'))
PYLIGHTNIX_LOGDIR:str = environ.get('PYLIGHTNIX_LOGDIR', join(PYLIGHTNIX_ROOT,'log'))
PYLIGHTNIX_TMP:str = environ.get('PYLIGHTNIX_TMP', join(PYLIGHTNIX_ROOT,'tmp'))
PYLIGHTNIX_STORE:str = join(PYLIGHTNIX_ROOT, f'store-v{PYLIGHTNIX_STORE_VERSION}')



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
             f'a string of form \'dref:name-HASH_HASH\'')
  assert ref[:5] == 'dref:', error_msg

def mkdref(refname:str, dhash:HashPart)->DRef:
  assert_valid_hashpart(dhash)
  return DRef('dref:'+dhash+'-'+refname)

def undref(r:DRef)->Tuple[str,HashPart]:
  assert_valid_rref(r)
  return (r[5+32+1:], HashPart(r[5:5+32]))



def assert_valid_rref(ref:str)->None:
  error_msg=(f'Value of {ref} is not a valid instance reference! Expected '
             f'a string of form \'dref:name-HASH_HASH\'')
  assert ref[:5] == 'rref:', error_msg

def mkrref(refname:str, dhash:HashPart, rhash:HashPart)->RRef:
  assert_valid_hashpart(dhash)
  assert_valid_hashpart(rhash)
  return RRef('rref:'+dhash+'-'+ihash+'-'+refname)

def unrref(r:RRef)->Tuple[str, HashPart, HashPart]:
  assert_valid_rref(r)
  return (r[5+32+1+32+1:], r[5:5+32], r[5+32+1:5+32+1+32])




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
    uf=[x for x in d if len(x)>0 and x[0]=='_']
    assert len(uf)==0, \
        (f"Config shouldn't initially contain fields starting with "
         f"underscopes '_'. Such filed should be added explicitly, "
         f"if needed. Got {uf}.")
    self.__dict__=deepcopy(d)

def assert_valid_config(c:Config):
  assert c is not None, 'Expected `Config` object, but None was passed'
  assert_valid_dict(c.__dict__, 'Config')

def config_dict(c:Config)->dict:
  return deepcopy(c.__dict__)

def config_ro(c:Config)->Any:
  return ConfigAttrs(c.__dict__)

def config_serialize(c:Config)->str:
  return json_dumps(config_dict(c), indent=4)

def config_hash(c:Config)->Hash:
  return datahash([config_serialize(c)])

def config_shortname(c:Config)->str:
  """ Return short human-readable name of a config """
  return slugify(config_dict(c).get('name','unnamed'))

#  ____  _        _
# / ___|| |_ __ _| |_ ___
# \___ \| __/ _` | __/ _ \
#  ___) | || (_| | ||  __/
# |____/ \__\__,_|\__\___|


""" State is a combination of a Config and a Program """
State = Tuple[Config,Program]

def state(c:Config)->State:
  """ State constructor """
  return (c,Program())

def state_add(s:State, op:str, arg:Any=[])->State:
  return (s[0],program_add(s[1],op,arg))

def state_deps(s:State)->List[DRef]:
  return list(set(scanref_dict(config_dict(s[0]))+scanref_list(s[1].ops)))

def state_hash(s:State)->Hash:
  return datahash([config_serialize(s[0]), program_serialize(s[1])])

#  ____  _
# / ___|| |_ ___  _ __ ___
# \___ \| __/ _ \| '__/ _ \
#  ___) | || (_) | | |  __/
# |____/ \__\___/|_|  \___|

def assert_valid_refpath(refpath:RefPath)->None:
  error_msg=(f'Value of type {type(refpath)} is not a valid refpath! Expected '
             f'list of strings starting from a reference, but actual value '
             f'is "{refpath}"')
  assert len(refpath)>0, error_msg
  assert_valid_rref(refpath[0])

def assert_store_initialized()->None:
  assert isdir(PYLIGHTNIX_STORE), \
    (f"Looks like the Modelcap store ('{PYLIGHTNIX_STORE}') is not initialized. Did "
     f"you call `store_initialize`?")
  assert isdir(PYLIGHTNIX_TMP), \
    (f"Looks like the Modelcap tmp ('{PYLIGHTNIX_TMP}') is not initialized. Did "
     f"you call `store_initialize`?")

def store_initialize(exist_ok:bool=True):
  print(f"Initializing {PYLIGHTNIX_STORE}")
  makedirs(PYLIGHTNIX_STORE, exist_ok=exist_ok)
  makedirs(PYLIGHTNIX_TMP, exist_ok=True)
  assert_store_initialized()


def store_dref2path(r:DRef)->Path:
  (nm,dhash)=undref(r)
  return Path(join(PYLIGHTNIX_STORE,dhash+'-'+nm))

def store_rref2path(r:RRef)->Path:
  (nm,dhash,rhash)=unrref(r)
  return Path(join(PYLIGHTNIX_STORE,dhash+'-'+nm,rhash))

def store_refpath2path(r:RefPath)->Path:
  assert_valid_refpath(r)
  return Path(join(store_rref2path(r[0]),*r[1:]))

def mkrefpath(r:RRef, items:List[str]=[])->RefPath:
  """ Constructs a RefPath out of a reference `ref` and a path within the node """
  assert_valid_rref(r)
  return RefPath([str(r)]+items)

def store_config(r:DRef)->Config:
  assert_valid_dref(ref)
  return Config(readjson(join(store_dref2path(r),'config.json')))

def store_config_ro(r:DRef)->Any:
  return config_ro(store_config(r))


def store_deps(r:DRef)->List[DRef]:
  """ Return a list of reference's dependencies, that is all the other references
  found in current ref's config and program """
  c=store_config(r)
  p=store_program(r)
  return state_deps((c,p))


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
  assert_valid_ref(ref)
  assert isdir(tgtpath), f"store_link(): `tgt` dir '{tgtpath}' doesn't exist"
  ts:Optional[str]
  if withtime:
    tspath=store_systempath(store_refpath(ref,['_timestamp_.txt']))
    if isfile(tspath):
      ts=open(tspath,'r').read()
    else:
      print(f"Warning: no timestamp for {ref}, probably because of old version of Modelcap")
      ts=None
  else:
    ts=None
  timeprefix=f'{ts}_' if ts is not None else ''
  forcelink(Path(relpath(store_dref2path(ref), tgtpath)),
            Path(join(tgtpath,f'{timeprefix}{name}')))

def store_drefs()->Iterable[DRef]:
  for dirname in listdir(PYLIGHTNIX_STORE):
    yield mkdref(str(dirname[32+1:]), HashPart(dirname[:32]))


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

def store_deref(m:Model, refpath:RefPath, search:Callable[[DRef],RRef])->Path:
  pass

#  __  __           _      _
# |  \/  | ___   __| | ___| |
# | |\/| |/ _ \ / _` |/ _ \ |
# | |  | | (_) | (_| |  __/ |
# |_|  |_|\___/ \__,_|\___|_|


class Model:
  """ Model tracks the process of building storage nodes.

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
  as returned by `model_outpath(m)` function.

  Note, that the rational behind `protocol` is unclear, maybe it should be
  moved into userland code completely.

  Finally, users typically call `model_save` which finishes the node creation,
  'seals' the node with a hash and sets the `storedir` field.  The storage item
  is believed to be immutable (but nothing special is done to enforce this
  restriction). `model_storelink` may be used to drop a symlink to this node
  into user-specified folder """

  def __init__(self, config:Config, timeprefix:Optional[str]=None):
    assert_valid_config(config)
    self.timeprefix:str = timestring() if timeprefix is None else timeprefix
    self.config:Config = config
    self.program:Program = Program([])
    self.protocol:Protocol = []
    self.outprefix:str = f'{self.timeprefix}_{config_hash(config)[:8]}_'
    self.outpath:Path = Path(mkdtemp(prefix=m.outprefix, dir=PYLIGHTNIX_TMP))
    self.deps:List[RRef]=[]

  def get_whash(self)->Hash:
    assert self.outref is None, \
      "This model is already saved so we don't want to get the hash of its temporary state"
    return dhash(model_outpath(self))

def model_config(m:Model)->Config:
  return m.config

def model_program(m:Model)->Program:
  return m.program

def model_config_ro(m:Model)->Any:
  return config_ro(model_config(m))

def model_outpath(m:Model)->Path:
  return m.outpath

def model_lasthash(m:Model)->Optional[Hash]:
  assert m.protocol is not None
  if len(m.protocol) == 0:
    return None
  else:
    return m.protocol[-1][1]

def protocol_add(m:Model, name:str, arg:Any=[], result:Any=[], expect_wchange:bool=True)->None:
  assert_serializable(name,'name')
  assert_serializable(arg,'arg')
  assert_serializable(result,'result')
  new_whash=m.get_whash()
  old_whash=model_lasthash(m)
  if expect_wchange:
    assert new_whash != old_whash, \
        (f"Modelcap sanity check: Operation was marked as parameter-changing,"
         f"but Model parameters didn't change their hashes as expected."
         f"Both hashes are {new_whash}.")
  else:
    assert new_whash == old_whash or (old_whash is None), \
        (f"Modelcap sanity check: Operation was marked as"
         f"non-paramerer-changing, but Model parameters were in fact changed by"
         f"something. Expected {old_whash}, got {new_whash}.")
  c=model_config(m)
  m.program.ops.append((name, arg))
  m.protocol.append((name, new_whash, result))

# def model_storelink(m:Model, expdir:Path, linksuffix:str, withtime:bool=True)->None:
#   """ Puts a link to model's storage into user-specified directory `expdir` """
#   assert m.outref is not None, \
#       "Looks like this model is not saved yet and thus it's `outref` is None"
#   timeprefix=f'{m.timeprefix}_' if withtime else ''
#   forcelink(Path(relpath(model_storepath(m), expdir)), Path(join(expdir,f'{timeprefix}{linksuffix}')))

# def metricslink(m:Model, expdir:str, tmpname:Optional[str]='tmplink')->None:
#   """ FIXME: move this out of generic libraty to ML-specific place """
#   prefix=tmpname if tmpname is not None else f'{m.timeprefix}'
#   forcelink(relpath(model_metricspath(m), expdir), expdir+f'/{prefix}')

# def model_save(m:Model)->Ref:
#   """ Create new node in the storage. Return reference to newly created storage node.
#   Node artifacts should be already prepared in the `model_output` directory.
#   This function saves additional metadata and seals the node with hash. Sealed
#   state is marked by assigning non-empty `storedir`.

#   TODO: make atomic """
#   assert_store_initialized()

#   c = model_config(m)
#   p = model_program(m)
#   o = model_outpath(m)

#   oops_message = ("Oops: Attempting to overwrite file %(F)s with builtin"
#                   "version. Please don't save files with this name in model's"
#                   "`model_outpath` folder for now.")

#   assert not isfile(join(o,'config.json')), oops_message % {'F':'config.json'}
#   assert not isfile(join(o,'program.json')), oops_message % {'F':'program.json'}
#   assert not isfile(join(o,'protocol.json')), oops_message % {'F':'protocol.json'}

#   with open(join(o,'config.json'), 'w') as f:
#     json_dump(config_dict(c), f, indent=4)
#   with open(join(o,'program.json'), 'w') as f:
#     json_dump(m.program.ops, f, indent=4)
#   with open(join(o,'protocol.json'), 'w') as f:
#     json_dump(m.protocol, f, indent=4)
#   with open(join(o,'_timestamp_.txt'), 'w') as f:
#     f.write(str(m.timeprefix))

#   refname=config_shortname(c)
#   statehash=fileshash([Path(join(o,'config.json')), Path(join(o,'program.json'))])
#   nodehash=dhash(o)
#   ref=store_mkref(refname, statehash, nodehash)
#   nodepath=store_systempath(store_refpath(ref))
#   cfgpath,dirname=split(nodepath)
#   makedirs(cfgpath, exist_ok=True)
#   replace(o, nodepath)

#   m.outref=ref
#   print(m.outref)
#   return ref

############################
## Actions
############################


def instantiate(s:State)->DRef:
  assert_store_initialized()
  (c,p)=s

  refname=config_shortname(c)
  dhash=state_hash(s)

  dref=mkdref(refname,trimhash(dhash))
  dpath=store_dref2path

  o=Path(mkdtemp(prefix=refname, dir=PYLIGHTNIX_TMP))
  with open(join(o,'config.json'), 'w') as f:
    f.write(config_serialize(c))
  with open(join(o,'program.json'), 'w') as f:
    f.write(program_serialize(p))

  replace(o, store_dref2path(dref))
  return dref


def realize(dref:DRef, builder:Callable[[Model],None])->RRef:
  c=store_config(dref)
  m=Model(c)
  builder(b)
  o=model_outpath(m)
  p=model_program(m)

  with open(join(o,'links.json'), 'w') as f:
    f.write(json_dumps(m.deps))

  name=config_shortname(c)
  dhash=state_hash((c,p))
  rhash=dhash(o)
  rref=mkrref(name,trimhash(dhash),trimhash(rhash))
  replace(o,store_rref2path(rref))
  return rref


#  ____                      _
# / ___|  ___  __ _ _ __ ___| |__
# \___ \ / _ \/ _` | '__/ __| '_ \
#  ___) |  __/ (_| | | | (__| | | |
# |____/ \___|\__,_|_|  \___|_| |_|


# def search_(chash:Hash, phash:Hash)->List[Ref]:
#   """ Return references matching the hashes of config and program """
#   matched=[]
#   store=PYLIGHTNIX_STORE
#   for name_statehash in listdir(store):
#     for nodehash in listdir(join(store,name_statehash)):

#       ref=store_mkref(statehash,nodehash)
#       c=config_deref(ref)
#       p=program_deref(ref)
#       if config_hash(c)==chash and program_hash(p)==phash:
#         matched.append(ref)
#   return matched

# def search(cp:State)->List[Ref]:
#   """ Return list of references to Store nodes that matches given `State` i.e.
#   `Config` and `Program` (in terms of corresponding `*_hash` functions)."""
#   return search_(config_hash(cp[0]), program_hash(cp[1]))

# def single(refs:List[Ref])->List[Ref]:
#   """ Return a resulting list only if it a singleton list """
#   for r in refs:
#     assert_valid_ref(r)
#   if len(refs)==1:
#     return refs
#   else:
#     return []

# def only(refs:List[Ref])->List[Ref]:
#   """ Take a list and extract it's single item, or complain loudly """
#   for r in refs:
#     assert_valid_ref(r)
#   if len(refs)==0:
#     assert False, \
#         (f"Empty list was passed to only(). This may mean that preceeding "
#          f"search founds no results in storage. You may have to either update "
#          f"the storage from elsewhere or re-run the associated computations to "
#          f"produce that nodes locally")
#   else:
#     assert len(refs)==1, \
#         (f"only() expected exactly one matched ref, but there are {len(refs)} "
#          f"of them:\n{refs}\n. Probably you need a more clever filter to make "
#          f"a right choice")
#   return refs[0]

