from pylightnix import ( Manager, Path, store_initialize, DRef, Context,
    Optional, mkbuild, build_outpath, store_rrefs, RRef, mkconfig, Config,
    Name, mkdrv, store_rref2path )
from tests.imports import ( rmtree, join, makedirs, listdir, Callable)

PYLIGHTNIX_TEST:str='/tmp/pylightnix_tests'

def setup_storage(tn:str)->str:
  import pylightnix.core
  storepath=f'/tmp/{tn}'
  rmtree(storepath, onerror=lambda a,b,c:())
  pylightnix.core.PYLIGHTNIX_STORE=storepath
  pylightnix.core.PYLIGHTNIX_TMP='/tmp'
  store_initialize(exist_ok=False)
  assert 0==len(listdir(storepath))
  return storepath

def setup_testpath(name:str)->Path:
  testpath=join(PYLIGHTNIX_TEST, name)
  rmtree(testpath, onerror=lambda a,b,c:())
  makedirs(testpath, exist_ok=False)
  return Path(testpath)

def setup_inplace_reset()->None:
  import pylightnix.inplace
  pylightnix.inplace.PYLIGHTNIX_MANAGER=Manager()

def mktestnode_nondetermenistic(m:Manager, sources:dict, nondet:Callable[[],int])->DRef:
  """ Emulate non-determenistic builds. `nondet` is expected to return
  different values from build to build """
  def _instantiate()->Config:
    return mkconfig(sources)
  def _realize(dref:DRef, context:Context)->Path:
    b=mkbuild(dref, context)
    with open(join(build_outpath(b),'nondet'),'w') as f:
      f.write(str(nondet()))
    return build_outpath(b)
  def _match(dref:DRef, context:Context)->Optional[RRef]:
    max_i=-1
    max_rref=None
    for rref in store_rrefs(dref, context):
      with open(join(store_rref2path(rref),'nondet'),'r') as f:
        i=int(f.read())
        if i>max_i:
          max_i=i
          max_rref=rref
    return max_rref
  return mkdrv(m, _instantiate, _match, _realize)


def mktestnode(m:Manager, sources:dict)->DRef:
  """ Build a test node with a given config and fixed build artifact """
  return mktestnode_nondetermenistic(m, sources, lambda : 0)


