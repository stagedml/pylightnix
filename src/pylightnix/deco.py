from pylightnix.types import (Stage, Registry, Build, DRef, RRef, StageResult,
                              Callable, List, Optional, Any, Dict)
from pylightnix.core import (mkdrv, mkconfig, match_latest, instantiate,
                             realize, realize1)
from pylightnix.build import (build_wrapper)

from pylightnix.lens import (mklens)

from pylightnix.imports import dataclass, getsourcelines

from pylightnix.utils import (pyobjhash, isrefpath, isselfpath, isdref)


def autodrv(kwargs:dict, sourcedeps:List[Any]=[]):
  def _deco(f:Callable[...,None]):
    r:Optional[Registry]=None
    cfg:dict={}
    for k,v in kwargs.items():
      if isinstance(v,Registry):
        r=v
      else:
        cfg[k]=v
    assert r is not None, "One of arguments should have type Registry"
    cfg["__source__"]=pyobjhash([f]+sourcedeps)
    def _make(b:Build):
      args:dict={}
      for k,v in kwargs.items():
        if isinstance(v,Registry):
          pass
        elif isinstance(v,DRef) and isdref(v):
          args[k]=mklens(b).get(k).rref
        elif isrefpath(v) or isselfpath(v):
          args[k]=mklens(b).get(k).syspath
        else:
          args[k]=v
      f(build=b,**args)
    return mkdrv(mkconfig(cfg),match_latest(),build_wrapper(_make),r=r)
  return _deco


@dataclass
class Placeholder:
  pass

def autostage(**decokw):
  def _deco(f:Callable[...,None])->Callable[...,DRef]:
    def _stage(r:Registry,**stagekw)->DRef:
      args:Dict[str,Any]={'r':r}
      for k,v in decokw.items():
        if isinstance(v,Placeholder):
          assert isinstance(stagekw[k],DRef)
        else:
          args[k]=v
      for k,v in stagekw.items():
        if isinstance(v,DRef):
          assert isinstance(decokw[k],Placeholder)
          args[k]=v
        else:
          assert k in decokw
          args[k]=v
      @autodrv(args, sourcedeps=[f])
      def drv(build:Build,**drvkw):
        f(build=build,**drvkw)
      return drv
    return _stage
  return _deco


