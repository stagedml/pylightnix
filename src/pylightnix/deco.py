from pylightnix.types import (Stage, Registry, Build, DRef, RRef, StageResult,
                              Callable, List, Optional, Any, Dict, Context,
                              Config, Union, Path, Matcher)
from pylightnix.core import (mkdrv, mkconfig, match_latest, instantiate,
                             realize, realize1, context_deref,
                             context_derefpath, drefcfg, rref2dref,
                             rrefpath2path)
from pylightnix.build import (build_wrapper)

from pylightnix.lens import (mklens)

from pylightnix.imports import dataclass, getsourcelines, join

from pylightnix.utils import (pyobjhash, isrefpath, isselfpath, isdref,
                              traverse_dict)

class Attrs:
  pass

def unroll(ctx:Context, dref:DRef, b:Optional[Build], rindex:int,
           max_depth:Optional[int]=None,
           always_multyref:bool=False,
           S=None)->Attrs:
  def _visit(k:Any, v:Any)->Any:
    if isdref(v):
      v=DRef(v)
      rrefs=context_deref(ctx,v)
      if max_depth is None or max_depth>0:
        max_depth2=max_depth-1 if max_depth is not None else None
        acc=[]
        for i,r in enumerate(rrefs):
          args=unroll(ctx,v,None,i,max_depth2,
                      always_multyref=always_multyref,S=S)
          setattr(args,'_rref',r)
          acc.append(args)
        return acc[0] if len(acc)==1 and not always_multyref else acc
      else:
        return rrefs[0] if len(rrefs)==1 and not always_multyref else rrefs
    elif isrefpath(v):
      if dref==v[0]:
        if dref in ctx:
          return context_derefpath(ctx,v,S=S)[rindex]
        else:
          assert b is not None and b.outpaths is not None
          return Path(join(b.outpaths.val[rindex],*v[1:]))
      else:
        return list(context_derefpath(ctx,v,S=S))
    elif isselfpath(v):
      assert False
    else:
      return v
  cfg=drefcfg(dref,S)
  traverse_dict(cfg.val,_visit)
  attrs=Attrs()
  for k,v in cfg.val.items():
    setattr(attrs,k,v)
  return attrs

def autodrv(kwargs:dict,
            sourcedeps:List[Any]=[],
            nouts:int=1,
            matcher:Optional[Matcher]=None,
            always_multyref:bool=False):
  matcher_=match_latest(nouts) if matcher is None else matcher
  def _deco(f:Callable[...,None]):
    r:Optional[Registry]=kwargs['r']
    assert r is not None, "One of arguments should have type Registry"
    cfg={k:v for k,v in kwargs.items()}
    cfg["__source__"]=pyobjhash([f]+sourcedeps)
    def _make(b:Build):
      assert b.outpaths is not None
      for i,_ in enumerate(b.outpaths.val):
        args=unroll(b.context,b.dref,b,i,None,
                    always_multyref=always_multyref,S=b.S)
        delattr(args,'__source__')
        if nouts>1 or always_multyref:
          setattr(args,'rindex',i)
        f(build=b,**args.__dict__)
    return mkdrv(mkconfig(cfg),matcher_,
                 build_wrapper(_make,nouts=nouts),r=r)
  return _deco

def autostage(nouts:int=1,
              sourcedeps:List[Any]=[],
              matcher:Optional[Matcher]=None,
              always_multyref:bool=False,
              **decokw):
  def _deco(f:Callable[...,None])->Callable[...,DRef]:
    def _stage(r:Registry,**stagekw)->DRef:
      args:Dict[str,Any]={'r':r}
      args.update(decokw)
      args.update(stagekw)
      @autodrv(args,sourcedeps=[f]+sourcedeps,nouts=nouts,matcher=matcher,
               always_multyref=always_multyref)
      def drv(build:Build,**drvkw):
        f(build=build,**drvkw)
      return drv
    return _stage
  return _deco


