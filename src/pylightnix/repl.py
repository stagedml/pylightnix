from pylightnix.types import ( Closure, Context, Derivation, RRef, DRef, List,
    Tuple, Optional, Generator, Path, Build  )

from pylightnix.core import ( realizeSeq, store_realize, RealizeSeqGen,
    mkbuild, build_outpaths )

class ReplHelper:
  def __init__(self, gen:RealizeSeqGen)->None:
    self.gen:Optional[RealizeSeqGen]=gen
    self.dref:Optional[DRef]=None
    self.context:Optional[Context]=None
    self.drv:Optional[Derivation]=None
    self.build:Optional[Build]=None
    self.rrefs:Optional[List[RRef]]=None

def repl_continueMany(rh:ReplHelper, out_paths:Optional[List[Path]]=None)->Optional[List[RRef]]:
  try:
    assert rh.gen is not None
    assert rh.dref is not None
    assert rh.context is not None
    assert rh.drv is not None
    if out_paths is None:
      if rh.build is not None:
        out_paths=build_outpaths(rh.build)
        rh.build=None
    if out_paths is not None:
      rrefs=[store_realize(rh.dref,rh.context,out_path) for out_path in out_paths]
    else:
      rrefs=[]
    rh.dref,rh.context,rh.drv=rh.gen.send(rrefs)
  except StopIteration as e:
    rh.gen=None
    rh.build=None
    rh.rrefs=e.value
  return rh.rrefs

def repl_continue(rh:ReplHelper, out_paths:Optional[List[Path]]=None)->Optional[RRef]:
  rrefs=repl_continueMany(rh, out_paths)
  if rrefs is None:
    return None
  assert len(rrefs)==1
  return rrefs[0]

def repl_realize(closure:Closure, force_interrupt:List[DRef]=[])->ReplHelper:
  rh=ReplHelper(realizeSeq(closure,force_interrupt))
  assert rh.gen is not None
  try:
    rh.dref,rh.context,rh.drv=next(rh.gen)
  except StopIteration as e:
    rh.gen=None
    rh.build=None
    rh.rrefs=e.value
  return rh

def repl_rrefs(rh:ReplHelper)->Optional[List[RRef]]:
  return rh.rrefs

def repl_rref(rh:ReplHelper)->Optional[RRef]:
  rrefs=repl_rrefs(rh)
  if rrefs is None:
    return None
  assert len(rrefs)==1
  return rrefs[0]

def repl_build(rh:ReplHelper, buildtime:bool=True, nouts:int=1)->Build:
  assert rh.gen is not None
  assert rh.dref is not None
  assert rh.context is not None
  rh.build=mkbuild(rh.dref, rh.context, buildtime=buildtime, nouts=nouts)
  return rh.build

def repl_cancel(rh:ReplHelper)->None:
  try:
    assert rh.gen is not None
    rh.gen.send(None)
  except StopIteration as e:
    rh.gen=None
    rh.build=None

