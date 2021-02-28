from pylightnix import ( Manager, Path, store_initialize, DRef, Context,
    Optional, mkbuild, build_outpath, store_rrefs, RRef, mkconfig,
    Name, mkdrv, store_rref2path, dirchmod, promise, Config, RealizeArg, Tag,
    RRefGroup, tryreadstr_def, SPath, storage, storagename, deepcopy)

from tests.imports import ( rmtree, join, makedirs, listdir, Callable,
    contextmanager, List, Dict,  Popen, PIPE, gettempdir )

PYLIGHTNIX_TEST:str='/tmp/pylightnix_tests'

class ShouldHaveFailed(Exception):
  pass

@contextmanager
def setup_storage(tn:str):
  # We reset STORE variables to prevent interaction with production store
  import pylightnix.core
  pylightnix.core.PYLIGHTNIX_STORE=None # type:ignore
  pylightnix.core.PYLIGHTNIX_TMP=None # type:ignore
  storepath=Path(f'/tmp/{tn}')
  try:
    dirchmod(storepath, 'rw')
    rmtree(storepath)
  except FileNotFoundError:
    pass
  store_initialize(custom_store=storepath, custom_tmp='/tmp')
  assert 0==len(listdir(storepath))
  try:
    yield storepath
  finally:
    # print('Setting PYLIGHTNIX_STORE to none')
    pylightnix.core.PYLIGHTNIX_STORE=None # type:ignore
    pylightnix.core.PYLIGHTNIX_TMP=None # type:ignore

@contextmanager
def setup_storage2(tn:str):
  # We reset STORE variables to prevent interaction with production store
  import pylightnix.core
  pylightnix.core.PYLIGHTNIX_TMP=None # type:ignore
  pylightnix.core.PYLIGHTNIX_STORE=None # type:ignore
  assert len(tn)>0
  testroot=Path(join(gettempdir(), 'pylightnix', tn))
  storepath=Path(join(testroot, storagename()))
  tmppath=Path(join(testroot, 'tmp'))
  try:
    dirchmod(testroot, 'rw')
    rmtree(testroot)
  except FileNotFoundError:
    pass
  # store_initialize(custom_store=storepath, custom_tmp=gettempdir())
  makedirs(storepath, exist_ok=False)
  makedirs(tmppath, exist_ok=False)
  pylightnix.core.PYLIGHTNIX_TMP=tmppath # type:ignore
  assert 0==len(listdir(storepath))
  try:
    yield tmppath,storepath
  finally:
    pylightnix.core.PYLIGHTNIX_STORE=None # type:ignore
    pylightnix.core.PYLIGHTNIX_TMP=None # type:ignore

def setup_testpath(name:str)->Path:
  testpath=join(PYLIGHTNIX_TEST, name)
  rmtree(testpath, onerror=lambda a,b,c:())
  makedirs(testpath, exist_ok=False)
  return Path(testpath)

def setup_inplace_reset()->None:
  import pylightnix.inplace
  pylightnix.inplace.PYLIGHTNIX_MANAGER=Manager(storage(None))

def mkstage(m:Manager,
            config:dict,
            nondet:Callable[[],int]=lambda:0,
            buildtime:bool=True,
            realize_wrapper=None,
            promise_strength=promise)->DRef:
  """ Emulate non-determenistic builds. `nondet` is expected to return
  different values from build to build """
  def _config()->Config:
    c=deepcopy(config)
    c['artifact']=[promise_strength,'artifact']
    return mkconfig(c)
  def _realize(S:SPath, dref:DRef, context:Context, ra:RealizeArg)->List[Dict[Tag,Path]]:
    b=mkbuild(S, dref, context, buildtime=buildtime)
    with open(join(build_outpath(b),'artifact'),'w') as f:
      f.write(str(nondet()))
    return b.outgroups
  def _match(S:SPath, dref:DRef, context:Context)->Optional[List[RRefGroup]]:
    max_i=-1
    max_gr:Optional[List[RRefGroup]]=None
    for gr in store_rrefs(dref, context, S):
      rref=gr[Tag('out')]
      i=int(tryreadstr_def(join(store_rref2path(rref, S),'artifact'), "0"))
      if i>max_i:
        max_i=i
        max_gr=[gr]
    return max_gr

  rw=(lambda x:x) if realize_wrapper is None else realize_wrapper
  return mkdrv(m, _config(), _match, rw(_realize))


def pipe_stdout(args:List[str], **kwargs)->str:
  return Popen(args, stdout=PIPE, **kwargs).stdout.read().decode() # type:ignore

