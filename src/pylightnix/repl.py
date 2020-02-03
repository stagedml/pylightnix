from pylightnix.types import ( Closure, Context, Derivation, RRef, DRef, List,
    Tuple, Optional, Generator  )

from pylightnix.core import ( realize_seq, store_realize )

class ReplHelper:
  def __init__(self, gen:Generator[Tuple[DRef,Context,Derivation],RRef,RRef],
                     force_interrupt:List[DRef])->None:
    self.force_interrupt=set(force_interrupt)
    self.gen=gen
    self.dref:Optional[DRef]=None
    self.context:Optional[Context]=None
    self.drv:Optional[Derivation]=None

def repl_start_(rh:ReplHelper)->Optional[RRef]:
  try:
    rh.dref,rh.context,rh.drv=next(rh.gen)
    return None
  except StopIteration as e:
    return e.value

def repl_continue(rh:ReplHelper, rref:Optional[RRef])->Optional[RRef]:
  try:
    while True:
      assert rh.dref is not None
      assert rh.context is not None
      assert rh.drv is not None
      if not rref:
        path=rh.drv.realizer(rh.dref,rh.context)
        rref=store_realize(rh.dref,rh.context,path)
        rreftmp=rh.drv.matcher(rh.dref,rh.context)
      rh.dref,rh.context,rh.drv=rh.gen.send(rref)
      if rh.dref in rh.force_interrupt:
        return None
      else:
        rref=rh.drv.matcher(rh.dref,rh.context)
  except StopIteration as e:
    return e.value

def repl_realize(closure:Closure, force_interrupt:List[DRef]=[])->Optional[RRef]:
  return repl_start_(ReplHelper(realize_seq(closure), force_interrupt))

