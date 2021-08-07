from pylightnix import (Manager, Build, Path, fsinit, DRef, Context,
                        Optional, mkbuildargs, build_outpath, allrrefs, RRef,
                        mkconfig, Name, mkdrv, rref2path, dirchmod, Config,
                        RealizeArg, drefrrefsC, tryreadstr_def, StorageSettings,
                        fsstorage, storagename, deepcopy, maybereadstr, selfref,
                        drefattrs, Output, Matcher, MatcherO, Realizer,
                        rrefdeps1, RealizerO, Output, output_realizer,
                        output_matcher, build_markstart, build_markstop,
                        StorageSettings)

from tests.imports import (rmtree, join, makedirs, listdir, Callable,
                           contextmanager, List, Dict,  Popen, PIPE,
                           gettempdir, mkdtemp, remove, settings, HealthCheck)


settings.register_profile("pylightnix", deadline=None, print_blob=True,
                          suppress_health_check=(HealthCheck.too_slow,))
settings.load_profile("pylightnix")

class ShouldHaveFailed(Exception):
  pass

# @contextmanager
# def setup_storage(tn:str):
#   # We reset STORE variables to prevent interaction with production store
#   import pylightnix.core
#   pylightnix.core.PYLIGHTNIX_STORE=None # type:ignore
#   pylightnix.core.PYLIGHTNIX_TMP=None # type:ignore
#   storepath=Path(join(gettempdir(),tn))
#   try:
#     dirchmod(storepath, 'rw')
#     rmtree(storepath)
#   except FileNotFoundError:
#     pass
#   fsinit(custom_store=storepath,
#                    custom_tmp=join(gettempdir(),'pylightnix_tmp'))
#   assert 0==len(listdir(storepath))
#   try:
#     yield storepath
#   finally:
#     # print('Setting PYLIGHTNIX_STORE to none')
#     pylightnix.core.PYLIGHTNIX_STORE=None # type:ignore
#     pylightnix.core.PYLIGHTNIX_TMP=None # type:ignore

@contextmanager
def setup_storage2(tn:str):
  assert len(tn)>0
  testroot=Path(join(gettempdir(), 'pylightnix', tn))
  storepath=Path(join(testroot, storagename()))
  tmppath=Path(join(testroot, 'tmp'))
  try:
    dirchmod(testroot, 'rw')
    rmtree(testroot)
  except FileNotFoundError:
    pass
  S=StorageSettings(testroot,tmppath)
  fsinit(S)
  assert 0==len(listdir(storepath))
  yield S

def setup_inplace_reset(S=None)->None:
  import pylightnix.inplace
  pylightnix.inplace.PYLIGHTNIX_MANAGER=Manager(S=S)


def setup_test_config(c:dict)->Config:
  c2=deepcopy(c)
  c2['artifact']=[selfref,'artifact']
  return mkconfig(c2)

def setup_test_match(nmatch:int)->MatcherO:
  def _match(S, o:Output[RRef])->Optional[Output[RRef]]:
    rrefs=o.val
    values=list(sorted([(maybereadstr(join(rref2path(rref, S),'artifact'),'0',int),rref)
                        for rref in rrefs], key=lambda x:x[0]))
    # print(nmatch, values)
    # Return `top-n` matched groups
    return Output([tup[1] for tup in values[-nmatch:]]) if len(values)>0 else None
  return _match

DELIBERATE_TEST_FAILURE='Deliberate test failure'

def setup_test_realize(nrrefs:int,
                       starttime:Optional[str],
                       nondet,
                       mustfail:bool)->RealizerO:
  def _realize(S, dref:DRef, context:Context, ra:RealizeArg)->Output[Path]:
    b=Build(mkbuildargs(S,dref,context,starttime,'AUTO',{},{}))
    paths=build_markstart(b,nrrefs)
    for i,o in enumerate(paths):
      with open(join(o,'artifact'),'w') as f:
        f.write(str(nondet(i)))
      with open(join(o,'id'),'w') as f:
        f.write(str(i))
      if mustfail:
        build_markstop(b)
        raise ValueError(DELIBERATE_TEST_FAILURE)
    assert b.outpaths is not None
    build_markstop(b)
    return b.outpaths
  return _realize

def mkstage(m:Manager,
            config:dict,
            nondet:Callable[[int],int]=lambda n:0,
            starttime:Optional[str]='AUTO',
            nrrefs:int=1,
            nmatch:int=1,
            mustfail:bool=False)->DRef:
  return mkdrv(m, setup_test_config(config),
                  output_matcher(setup_test_match(nmatch)),
                  output_realizer(setup_test_realize(
                    nrrefs, starttime, nondet, mustfail)))


def pipe_stdout(args:List[str], **kwargs)->str:
  return Popen(args, stdout=PIPE, **kwargs).stdout.read().decode() # type:ignore

def rrefdepth(rref:RRef,S=None)->int:
  rec=[rrefdepth(r,S) for r in rrefdeps1([rref],S=S)]
  return 1+(max(rec) if len(rec)>0 else 0)


def mkstageP(m:Manager,
            config:dict,
            nondet:Callable[[int],int]=lambda n:0,
            starttime:Optional[str]='AUTO',
            nrrefs:int=1,
            nmatch:int=1,
            mustfail:bool=False)->DRef:
  """ Makes a stage which could deliberately break the promise - i.e. fail to
  provide a promised artifact """
  def _r(S, dref:DRef, c:Context, ra:RealizeArg)->Output[Path]:
    r=setup_test_realize(nrrefs, starttime, nondet, False)(S,dref,c,ra)
    if mustfail:
      # for path in r.val:
      remove(join(r.val[-1],"artifact"))
    return r
  return mkdrv(m, setup_test_config(config),
               output_matcher(setup_test_match(nmatch)),
               output_realizer(_r))

