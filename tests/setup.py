from pylightnix import (Manager, Path, initialize, DRef, Context, Optional,
                        mkbuild, build_outpath, allrrefs, RRef, mkconfig, Name,
                        mkdrv, rref2path, dirchmod, Config, RealizeArg,
                        drefrrefsC, tryreadstr_def, SPath, storage,
                        storagename, deepcopy, build_setoutpaths, maybereadstr,
                        selfref, drefattrs, Output, Matcher, Realizer, rrefdeps1)

from tests.imports import (rmtree, join, makedirs, listdir, Callable,
                           contextmanager, List, Dict,  Popen, PIPE,
                           gettempdir, mkdtemp)

class ShouldHaveFailed(Exception):
  pass

@contextmanager
def setup_storage(tn:str):
  # We reset STORE variables to prevent interaction with production store
  import pylightnix.core
  pylightnix.core.PYLIGHTNIX_STORE=None # type:ignore
  pylightnix.core.PYLIGHTNIX_TMP=None # type:ignore
  storepath=Path(join(gettempdir(),tn))
  try:
    dirchmod(storepath, 'rw')
    rmtree(storepath)
  except FileNotFoundError:
    pass
  initialize(custom_store=storepath,
                   custom_tmp=join(gettempdir(),'pylightnix_tmp'))
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
  # initialize(custom_store=storepath, custom_tmp=gettempdir())
  makedirs(storepath, exist_ok=False)
  makedirs(tmppath, exist_ok=False)
  pylightnix.core.PYLIGHTNIX_TMP=tmppath # type:ignore
  assert 0==len(listdir(storepath))
  try:
    yield tmppath,storepath
  finally:
    pylightnix.core.PYLIGHTNIX_STORE=None # type:ignore
    pylightnix.core.PYLIGHTNIX_TMP=None # type:ignore

def setup_inplace_reset()->None:
  import pylightnix.inplace
  pylightnix.inplace.PYLIGHTNIX_MANAGER=Manager(storage(None))


def setup_test_config(c:dict)->Config:
  c2=deepcopy(c)
  c2['artifact']=[selfref,'artifact']
  return mkconfig(c2)

def setup_test_match(nmatch)->Matcher:
  def _match(S:SPath, rrefs:Output[RRef])->Optional[Output[RRef]]:
    values=list(sorted([(maybereadstr(join(rref2path(rref, S),'artifact'),'0',int),rref)
                        for rref in rrefs.val], key=lambda x:x[0]))
    print(nmatch, values)
    # Return `top-n` matched groups
    return Output([tup[1] for tup in values[-nmatch:]]) if len(values)>0 else None
  return _match

def setup_test_realize(nrrefs, buildtime, nondet, mustfail)->Realizer:
  def _realize(S:SPath, dref:DRef, context:Context, ra:RealizeArg)->Output:
    b=mkbuild(S, dref, context, buildtime=buildtime)
    paths=build_setoutpaths(b,nrrefs)
    for i,o in enumerate(paths):
      with open(join(o,'artifact'),'w') as f:
        f.write(str(nondet(i)))
      with open(join(o,'id'),'w') as f:
        f.write(str(i))
      if mustfail:
        raise ValueError('Failure by request')
    return Output(b.outpaths)
  return _realize

def mkstage(m:Manager,
            config:dict,
            nondet:Callable[[int],int]=lambda n:0,
            buildtime:bool=True,
            mkdrv_=mkdrv,
            nrrefs:int=1,
            nmatch:int=1,
            mustfail:bool=False)->DRef:
  return mkdrv_(m,
               setup_test_config(config),
               setup_test_match(nmatch),
               setup_test_realize(nrrefs, buildtime, nondet, mustfail))


def pipe_stdout(args:List[str], **kwargs)->str:
  return Popen(args, stdout=PIPE, **kwargs).stdout.read().decode() # type:ignore

def rrefdepth(rref:RRef,S=None)->int:
  rec=[rrefdepth(r,S) for r in rrefdeps1([rref],S=S)]
  return 1+(max(rec) if len(rec)>0 else 0)


