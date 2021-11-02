from pylightnix.types import (Stage, Registry, Build, DRef, RRef, StageResult,
                              Callable, List, Optional, Any, Dict)
from pylightnix.core import (mkdrv, mkconfig, match_latest, instantiate,
                             realize, realize1, context_deref)
from pylightnix.build import (build_wrapper)

from pylightnix.lens import (mklens)

from pylightnix.imports import dataclass, getsourcelines

from pylightnix.utils import (pyobjhash, isrefpath, isselfpath, isdref,
                              traverse_dict)


def autodrv(kwargs:dict,
            sourcedeps:List[Any]=[],
            matcher=match_latest()):
  def _deco(f:Callable[...,None]):
    r:Optional[Registry]=kwargs['r']
    assert r is not None, "One of arguments should have type Registry"
    cfg={k:v for k,v in kwargs.items()}
    cfg["__source__"]=pyobjhash([f]+sourcedeps)
    def _make(b:Build):
      args:dict={k:v for k,v in kwargs.items() if not isinstance(v,Registry)}
      def _visit(k:Any, v:Any)->Any:
        if isdref(v) and isinstance(v,DRef):
          rrefs=context_deref(b.context,v)
          assert len(rrefs)==1
          return rrefs[0]
        elif isrefpath(v) or isselfpath(v):
          # FIXME: resolve refpath by value
          return mklens(b).get(k).syspath
        else:
          return v
      traverse_dict(args,_visit)
      f(build=b,**args)
    return mkdrv(mkconfig(cfg),matcher,build_wrapper(_make),r=r)
  return _deco


def autostage(matcher=match_latest(),**decokw):
  def _deco(f:Callable[...,None])->Callable[...,DRef]:
    def _stage(r:Registry,**stagekw)->DRef:
      args:Dict[str,Any]={'r':r}
      args.update(decokw)
      args.update(stagekw)
      @autodrv(args, sourcedeps=[f], matcher=matcher)
      def drv(build:Build,**drvkw):
        f(build=build,**drvkw)
      return drv
    return _stage
  return _deco


