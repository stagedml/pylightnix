from pylightnix.imports import (
    sha256, deepcopy, isdir, makedirs, join, json_dump, json_load, isfile,
    relpath, listdir, rmtree, mkdtemp, replace, environ )
from pylightnix.utils import (
    dhash, assert_serializable, assert_valid_dict, dicthash, scanref_dict,
    scanref_list, forcelink, timestring )
from pylightnix.types import (
    List, Any, Tuple, Union, Optional, Iterable, IO, Path, Hash, Ref, RefPath,
    Protocol )

PYLIGHTNIX_STORE_VERSION = 1
PYLIGHTNIX_ROOT:str = environ.get('PYLIGHTNIX_ROOT', join(environ.get('HOME','/var/run'),'_pylightnix'))
PYLIGHTNIX_LOGDIR:str = environ.get('PYLIGHTNIX_LOGDIR', join(PYLIGHTNIX_ROOT,'log'))
PYLIGHTNIX_TMP:str = environ.get('PYLIGHTNIX_TMP', join(PYLIGHTNIX_ROOT,'tmp'))
PYLIGHTNIX_STORE:str = join(PYLIGHTNIX_ROOT, f'store-v{PYLIGHTNIX_STORE_VERSION}')

# ____
# |  _ \ _ __ ___   __ _ _ __ __ _ _ __ ___
# | |_) | '__/ _ \ / _` | '__/ _` | '_ ` _ \
# |  __/| | | (_) | (_| | | | (_| | | | | | |
# |_|   |_|  \___/ \__, |_|  \__,_|_| |_| |_|
#                  |___/

class Program:
  """ Program is a collection of non-determenistic operations applied to a
  `Config`.

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

def program_hash(p:Program)->Hash:
  """ Calculate the hashe of a program """
  string=";".join([f'{nm}({str(args)})' for nm,args in p.ops if nm[0]!='_'])
  return Hash(sha256(string.encode('utf-8')).hexdigest())


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

def config_hash(c:Config)->Hash:
  """ Calculate the hash of config. Top-level fields starting from '_' are ignored """
  return dicthash(config_dict(c))


#  ____  _        _
# / ___|| |_ __ _| |_ ___
# \___ \| __/ _` | __/ _ \
#  ___) | || (_| | ||  __/
# |____/ \__\__,_|\__\___|


""" State is a combination of config and program """
State = Tuple[Config,Program]

def state(c:Config)->State:
  """ State constructor """
  return (c,Program())

def state_add(s:State, op:str, arg:Any=[])->State:
  return (s[0],program_add(s[1],op,arg))

def state_deps(s:State)->List[Ref]:
  (c,p)=s
  refs=scanref_dict(config_dict(c))+scanref_list(p.ops)
  return list(set(refs))


#  ____  _
# / ___|| |_ ___  _ __ ___
# \___ \| __/ _ \| '__/ _ \
#  ___) | || (_) | | |  __/
# |____/ \__\___/|_|  \___|

def assert_valid_ref(ref:Ref)->None:
  error_msg=(f'Value of type {type(ref)} is not a valid reference! Expected '
             f'string of form \'ref:HASH\', but actual value is "{ref}"')
  assert len(ref)>4, error_msg
  assert ref[:4] == 'ref:', error_msg

def assert_valid_refpath(refpath):
  error_msg=(f'Value of type {type(refpath)} is not a valid refpath! Expected '
             f'list of strings starting from a reference, but actual value '
             f'is "{refpath}"')
  assert len(refpath)>0, error_msg
  assert_valid_ref(refpath[0]), error_msg


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
  makedirs(PYLIGHTNIX_TMP, exist_ok=exist_ok)
  assert_store_initialized()

def store_systempath(refpath:RefPath)->Path:
  """ Constructs a Refpath into system-specific path
  TODO: use joins here
  """
  assert_valid_refpath(refpath)
  return Path(join(PYLIGHTNIX_STORE,join(refpath[0][4:],join(*refpath[1:]))))

def store_refpath(ref:Ref, items:List[str]=[])->RefPath:
  """ Constructs a Refpath out of a reference `ref` and a path within the node """
  assert_valid_ref(ref)
  return RefPath([str(ref)]+items)

def store_readjson(refpath:RefPath)->Any:
  with open(store_systempath(refpath), "r") as f:
    return json_load(f)

def config_deref(ref:Ref)->Config:
  assert_valid_ref(ref)
  return Config(store_readjson(store_refpath(ref, ['config.json'])))

def config_deref_ro(ref:Ref)->Any:
  return config_ro(Config(store_readjson(store_refpath(ref, ['config.json']))))

store_config_ro = config_deref_ro

def program_deref(ref:Ref)->Program:
  return Program(store_readjson(store_refpath(ref, ['program.json'])))

def store_deps(ref:Ref)->List[Ref]:
  """ Return a list of reference's dependencies, that is all the other references
  found in current ref's config and program """
  c=config_deref(ref)
  p=program_deref(ref)
  return state_deps((c,p))


def store_deepdeps(roots:List[Ref])->List[Ref]:
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


def store_link(ref:Ref, tgtpath:Path, name:str, withtime=True)->None:
  """ Puts a link pointing to storage node into user-specified directory
  `tgtpath` """
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
  forcelink(Path(relpath(store_systempath(store_refpath(ref,[])), tgtpath)),
            Path(join(tgtpath,f'{timeprefix}{name}')))

def store_gc(refs_in_use:List[Ref])->List[Ref]:
  """ Take roots which are in use and should not be removed. Return roots which
  are not used and may be removed. Actual removing is to be done by user-defined
  application. """
  assert_store_initialized()

  roots_with_deps=store_deepdeps(refs_in_use)

  to_delete=[]
  for dirname in sorted(listdir(PYLIGHTNIX_STORE)):
    ref='ref:'+dirname
    if not ref in roots_with_deps:
      to_delete.append(Ref(ref))
  return to_delete


#  __  __           _      _
# |  \/  | ___   __| | ___| |
# | |\/| |/ _ \ / _` |/ _ \ |
# | |  | | (_) | (_| |  __/ |
# |_|  |_|\___/ \__,_|\___|_|


class Model:
  """ Model tracks the process of building storage nodes.

  Lifecycle of a model starts from its creation from JSON-serializable
  `Config`.

  After the model is created, users typically perform non-determenistic
  operations on it. To make the model abstraction aware of them, users have to
  update the _state_ of the model, which is a combination of `config`, `program`
  and `protocol` field.  The separation of state into `config` and `program` is
  not strictly important, but we hope it will help us to build a more
  user-friendly search system. We encourage users to keep config immutable after
  it was passed to model, and use `program` to track changes.  During
  operations, users are welcome to save various processing artifacts into
  temporary folder as returned by `model_outpath(m)` function.

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
    self.outprefix:str=f'{self.timeprefix}_{config_hash(config)[:8]}_'
    self.outpath:Optional[Path]=None
    self.storedir:Optional[Path]=None

  def get_whash(self)->Hash:
    assert self.storedir is None, \
      "This model is already saved so we don't want to get the hash of its temporary state"
    return dhash(model_outpath(self))

def model_program(m:Model)->Program:
  return m.program

def model_outpath(m:Model)->Path:
  if m.outpath is None:
    m.outpath=Path(mkdtemp(prefix=m.outprefix, dir=PYLIGHTNIX_TMP))
  return m.outpath

def model_storepath(m:Model)->str:
  assert m.storedir is not None, \
      "Looks like this model is not saved yet and thus it's `storepath` is undefined"
  return PYLIGHTNIX_STORE+'/'+m.storedir

def model_config(m:Model)->Config:
  return m.config

def model_config_ro(m:Model)->Any:
  return config_ro(model_config(m))

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

def model_storelink(m:Model, expdir:Path, linksuffix:str, withtime:bool=True)->None:
  """ Puts a link to model's storage into user-specified directory `expdir` """
  assert m.storedir is not None, \
      "Looks like this model is not saved yet and thus it's `storelink` is undefined"
  timeprefix=f'{m.timeprefix}_' if withtime else ''
  forcelink(Path(relpath(model_storepath(m), expdir)), Path(join(expdir,f'{timeprefix}{linksuffix}')))

# def metricslink(m:Model, expdir:str, tmpname:Optional[str]='tmplink')->None:
#   """ FIXME: move this out of generic libraty to ML-specific place """
#   prefix=tmpname if tmpname is not None else f'{m.timeprefix}'
#   forcelink(relpath(model_metricspath(m), expdir), expdir+f'/{prefix}')

def model_save(m:Model)->Ref:
  """ Create new node in the storage. Return reference to newly created storage node.
  Node artifacts should be already prepared in the `model_output` directory.
  This function saves additional metadata and seals the node with hash. Sealed
  state is marked by assigning non-empty `storedir`.

  TODO: make atomic """
  assert_store_initialized()

  c = model_config(m)
  p = model_program(m)
  o = model_outpath(m)

  oops_message = ("Oops: Attempting to overwrite file %(F)s with builtin"
                  "version. Please don't save files with this name in model's"
                  "`model_outpath` folder for now.")

  assert not isfile(o+'/config.json'), oops_message % {'F':'config.json'}
  assert not isfile(o+'/program.json'), oops_message % {'F':'program.json'}
  assert not isfile(o+'/protocol.json'), oops_message % {'F':'protocol.json'}

  with open(o+'/config.json', 'w') as f:
    json_dump(config_dict(c), f, indent=4)
  with open(o+'/program.json', 'w') as f:
    json_dump(m.program.ops, f, indent=4)
  with open(o+'/protocol.json', 'w') as f:
    json_dump(m.protocol, f, indent=4)
  with open(o+'/_timestamp_.txt', 'w') as f:
    f.write(str(m.timeprefix))

  ho=dhash(o)
  storedir=config_dict(c).get('name','unnamed')+'-'+ho
  nodepath=Path(join(PYLIGHTNIX_STORE,storedir))
  if isdir(nodepath):
    hs=dhash(nodepath)
    assert ho==hs, f"Oops: {storedir} exists, but have incorrect hash {hs}."
    rmtree(o)
  else:
    replace(o, nodepath)

  m.storedir=storedir
  print(m.storedir)
  ref='ref:'+storedir
  assert_valid_ref(ref)
  return ref


#  ____                      _
# / ___|  ___  __ _ _ __ ___| |__
# \___ \ / _ \/ _` | '__/ __| '_ \
#  ___) |  __/ (_| | | | (__| | | |
# |____/ \___|\__,_|_|  \___|_| |_|


def search_(chash:Hash, phash:Hash)->List[Ref]:
  """ Return references matching the hashes of config and program """
  matched=[]
  for dirname in sorted(listdir(PYLIGHTNIX_STORE)):
    ref=Ref('ref:'+dirname)
    c=config_deref(ref)
    p=program_deref(ref)
    if config_hash(c)==chash and program_hash(p)==phash:
      matched.append(ref)
  return matched

def search(cp:State)->List[Ref]:
  """ Return list of references to Store nodes that matches given `State` i.e.
  `Config` and `Program` (in terms of corresponding `*_hash` functions)."""
  return search_(config_hash(cp[0]), program_hash(cp[1]))

def single(refs:List[Ref])->List[Ref]:
  """ Return a resulting list only if it a singleton list """
  for r in refs:
    assert_valid_ref(r)
  if len(refs)==1:
    return refs
  else:
    return []

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

