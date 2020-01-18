from pylightnix.core import ( Manager, manage, mkconfig, mkbuild, Build, Config,
    Closure, only )
from pylightnix.types import DRef, RRef


def mknode(m:Manager, d:dict)->DRef:
  """ Create a storage node which doesn't store any artifacts. It's meaning is
  entirely deternined by it's configuration dict `d`.  """
  def _instantiate()->Config:
    return mkconfig(d)
  def _realize(dref:DRef, closure:Closure)->Build:
    return mkbuild(dref, closure)
  return manage(m, _instantiate, _realize, only)
