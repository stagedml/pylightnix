from pylightnix.types import ( Closure, Context, Derivation, RRef, DRef, List,
    Tuple, Optional, Generator, Path, Build  )

from pylightnix.core import ( realize_seq, store_realize, RealizeSeqGen,
    RealizeSeqCancelled, mkbuild, build_outpath )

class ReplHelper:
  def __init__(self, gen:RealizeSeqGen,
                     force_interrupt:List[DRef])->None:
    self.force_interrupt=set(force_interrupt)
    self.gen:Optional[RealizeSeqGen]=gen
    self.dref:Optional[DRef]=None
    self.context:Optional[Context]=None
    self.drv:Optional[Derivation]=None
    self.rref:Optional[RRef]=None
    self.build:Optional[Build]=None


def repl_start_(rh:ReplHelper)->Optional[RRef]:
  assert rh.gen is not None
  rh.dref,rh.context,rh.drv=next(rh.gen)
  if rh.dref in rh.force_interrupt:
    return None
  return repl_continue(rh,None)


def repl_continue(rh:ReplHelper, out_path:Optional[Path]=None)->Optional[RRef]:
  try:
    rref:Optional[RRef]=None
    while True:
      assert rh.gen is not None
      assert rh.dref is not None
      assert rh.context is not None
      assert rh.drv is not None
      if rh.build is not None:
        out_path=build_outpath(rh.build)
        rh.build=None
      if out_path is not None:
        rref=store_realize(rh.dref,rh.context,out_path)
        rreftmp=rh.drv.matcher(rh.dref,rh.context)
        out_path=None
      else:
        rref=rh.drv.matcher(rh.dref,rh.context)
      if rref is None:
        path=rh.drv.realizer(rh.dref,rh.context)
        rref=store_realize(rh.dref,rh.context,path)
        rreftmp=rh.drv.matcher(rh.dref,rh.context)
      assert rref is not None
      rh.dref,rh.context,rh.drv=rh.gen.send(rref)
      if rh.dref in rh.force_interrupt:
        return None
  except StopIteration as e:
    rh.gen=None
    rh.rref=e.value
    return rh.rref

def repl_realize(closure:Closure, force_interrupt:List[DRef]=[])->ReplHelper:
  rh=ReplHelper(realize_seq(closure), force_interrupt)
  repl_start_(rh)
  return rh

def repl_rref(rh:ReplHelper)->Optional[RRef]:
  return rh.rref

def repl_build(rh:ReplHelper, buildtime:bool=True)->Build:
  assert rh.gen is not None
  assert rh.dref is not None
  assert rh.context is not None
  rh.build=mkbuild(rh.dref, rh.context, buildtime=buildtime)
  return rh.build

def repl_cancel(rh:ReplHelper)->None:
  try:
    assert rh.gen is not None
    rh.gen.send(None)
  except RealizeSeqCancelled:
    rh.gen=None
    rh.build=None
  assert rh.gen is None

