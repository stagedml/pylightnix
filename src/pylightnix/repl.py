from pylightnix.types import ( Closure, Context, Derivation, RRef, DRef, List,
    Tuple, Optional, Generator, Path, Build  )

from pylightnix.core import ( realize_seq, store_realize, RealizeSeqGen,
    RealizeSeqCancelled, mkbuild, build_outpaths )

class ReplHelper:
  def __init__(self, gen:RealizeSeqGen,
                     force_interrupt:List[DRef])->None:
    self.force_interrupt=set(force_interrupt)
    self.gen:Optional[RealizeSeqGen]=gen
    self.dref:Optional[DRef]=None
    self.context:Optional[Context]=None
    self.drv:Optional[Derivation]=None
    self.build:Optional[Build]=None
    self.rrefs:List[RRef]=[]


def repl_start_(rh:ReplHelper)->List[RRef]:
  assert rh.gen is not None
  rh.dref,rh.context,rh.drv=next(rh.gen)
  if rh.dref in rh.force_interrupt:
    return []
  return repl_continue_(rh,[])


def repl_continue_(rh:ReplHelper, out_paths:List[Path]=[])->List[RRef]:
  try:
    rref:Optional[RRef]=None
    while True:
      assert rh.gen is not None
      assert rh.dref is not None
      assert rh.context is not None
      assert rh.drv is not None
      if rh.build is not None:
        out_paths=build_outpaths(rh.build)
        rh.build=None
      if len(out_paths)>0:
        rrefs=[store_realize(rh.dref,rh.context,out_path) for out_path in out_paths]
        rreftmp=rh.drv.matcher(rh.dref,rh.context)
        out_paths=[]
      else:
        rrefs=rh.drv.matcher(rh.dref,rh.context)
      if len(rrefs)==0:
        paths=rh.drv.realizer(rh.dref,rh.context)
        rrefs=[store_realize(rh.dref,rh.context,path) for path in paths]
        rreftmp=rh.drv.matcher(rh.dref,rh.context)
      assert len(rrefs)>0
      rh.dref,rh.context,rh.drv=rh.gen.send(rrefs)
      if rh.dref in rh.force_interrupt:
        return []
  except StopIteration as e:
    rh.gen=None
    rh.rrefs=e.value
    return rh.rrefs

def repl_continue(rh:ReplHelper, out_paths:List[Path]=[])->Optional[RRef]:
  rrefs=repl_continue_(rh, out_paths)
  assert len(rrefs)<=1
  return rrefs[0] if len(rrefs)==1 else None

def repl_realize(closure:Closure, force_interrupt:List[DRef]=[])->ReplHelper:
  rh=ReplHelper(realize_seq(closure), force_interrupt)
  repl_start_(rh)
  return rh

def repl_rrefs(rh:ReplHelper)->List[RRef]:
  return rh.rrefs

def repl_rref(rh:ReplHelper)->Optional[RRef]:
  rrefs=repl_rrefs(rh)
  assert len(rrefs)<=1
  return rrefs[0] if len(rrefs)==1 else None

def repl_build(rh:ReplHelper, buildtime:bool=True, nouts:int=1)->Build:
  assert rh.gen is not None
  assert rh.dref is not None
  assert rh.context is not None
  rh.build=mkbuild(rh.dref, rh.context, buildtime=buildtime, nouts=nouts)
  return rh.build

def repl_cancel(rh:ReplHelper)->None:
  try:
    assert rh.gen is not None
    rh.gen.send([])
  except RealizeSeqCancelled:
    rh.gen=None
    rh.build=None
  assert rh.gen is None

