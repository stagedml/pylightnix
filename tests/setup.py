from pylightnix import ( Manager, Path, store_initialize, DRef, Context,
    Optional, mkbuild, build_outpath, store_rrefs, RRef, mkconfig,
    Name, mkdrv, rref2path, dirchmod, promise, Config, RealizeArg )
from tests.imports import ( rmtree, join, makedirs, listdir, Callable,
    contextmanager, List)

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

def setup_testpath(name:str)->Path:
  testpath=join(PYLIGHTNIX_TEST, name)
  rmtree(testpath, onerror=lambda a,b,c:())
  makedirs(testpath, exist_ok=False)
  return Path(testpath)

def setup_inplace_reset()->None:
  import pylightnix.inplace
  pylightnix.inplace.PYLIGHTNIX_MANAGER=Manager()

def mktestnode_nondetermenistic(m:Manager, sources:dict,
                                nondet:Callable[[],int],
                                buildtime:bool=True)->DRef:
  """ Emulate non-determenistic builds. `nondet` is expected to return
  different values from build to build """
  def _instantiate()->Config:
    c=mkconfig(sources)
    c.val['promise_artifact']=[promise,'artifact']
    return c
  def _realize(dref:DRef, context:Context, ra:RealizeArg)->List[Path]:
    b=mkbuild(dref, context, buildtime=buildtime)
    with open(join(build_outpath(b),'artifact'),'w') as f:
      f.write(str(nondet()))
    return [build_outpath(b)]
  def _match(dref:DRef, context:Context)->Optional[List[RRef]]:
    max_i=-1
    max_rref:Optional[List[RRef]]=None
    for gr in store_rrefs(dref, context):
      for rref in gr.values():
        with open(join(rref2path(rref),'artifact'),'r') as f:
          i=int(f.read())
          if i>max_i:
            max_i=i
            max_rref=[rref]
    return max_rref
  return mkdrv(m, _instantiate(), _match, _realize)


def mktestnode(m:Manager, sources:dict, buildtime=True)->DRef:
  """ Build a test node with a given config and fixed build artifact """
  return mktestnode_nondetermenistic(m, sources, lambda:0, buildtime)


