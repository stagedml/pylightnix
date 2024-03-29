from pylightnix.types import (Stage, Registry, Build, DRef, RRef, StageResult,
                              Callable, List, Optional, Any, Dict, Context,
                              Config, Union, Path, Matcher, Closure, Tuple,
                              PylightnixException)
from pylightnix.core import (mkdrv, mkconfig, match_latest, instantiate,
                             realize, realize1, context_deref,
                             context_derefpath, drefcfg, rref2dref,
                             rrefpath2path, unpack_closure_arg_)
from pylightnix.build import (build_wrapper)

from pylightnix.lens import (mklens)

from pylightnix.imports import (dataclass, getsourcelines, join, deepcopy, parse,
                                signature, InspectParameter)

from pylightnix.utils import (pyobjhash, isrefpath, isselfpath, isdref,
                              traverse_dict)

class Attrs:
  """ A class for proxy objects where realization config parameters are set as
  attributs. """
  pass


def unroll(ctx:Context,
           dref:DRef,
           b:Optional[Build],
           rindex:int,
           max_depth:Optional[int]=None,
           always_multiref:bool=False,
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
                      always_multiref=always_multiref,S=S)
          setattr(args,'_rref',r)
          acc.append(args)
        return acc[0] if len(acc)==1 and not always_multiref else acc
      else:
        return rrefs[0] if len(rrefs)==1 and not always_multiref else rrefs
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


def unrollR(sr:StageResult,
            ctx:Context,
            max_depth:Optional[int]=None,
            always_multiref:bool=False,
            S=None)->Any:
  def _visit(k:Any, v:Any)->Any:
    if isdref(v):
      rrefs=context_deref(ctx,DRef(v))
      acc=[]
      for i,r in enumerate(rrefs):
        args=unroll(ctx,DRef(v),None,0,
                    max_depth=max_depth,
                    always_multiref=always_multiref,
                    S=S)
        setattr(args,'_rref',r)
        acc.append(args)
      return acc[0] if len(acc)==1 and not always_multiref else acc
    else:
      return v
  d={0:deepcopy(sr)}
  traverse_dict(d,_visit)
  return d[0]

def realizeU(arg:Union[Closure,Tuple[StageResult,Closure]],
             *args,
             max_depth:Optional[int]=None,
             always_multiref:bool=False,
             **kwargs):
  result,closure=unpack_closure_arg_(arg)
  r,_,ctx=realize((result,closure),*args,**kwargs)
  return unrollR(r,ctx,max_depth=max_depth,always_multiref=always_multiref,
                 S=closure.S)


def autodrv_(*,
             nouts:int=1,
             matcher:Optional[Matcher]=None,
             always_multiref:bool=False,
             sourcedeps:List[Any]=[],
             r:Optional[Registry]=None,
             **kwargs):
  matcher_=match_latest(nouts) if matcher is None else matcher
  def _deco(f:Callable[[Build,List[Any]],None]):
    cfg={}
    for k,v in kwargs.items():
      if k!="r":
        if callable(v):
          cfg.update({k:v(r=r)})
        else:
          cfg.update({k:v})
    cfg["__source__"]=pyobjhash([f]+sourcedeps)
    def _make(b:Build):
      assert b.outpaths is not None
      arglist=[]
      for i,_ in enumerate(b.outpaths.val):
        args=unroll(b.context,b.dref,b,i,None,
                    always_multiref=always_multiref,S=b.S)
        delattr(args,'__source__')
        if nouts>1 or always_multiref:
          setattr(args,'rindex',i)
        arglist.append(args)
      f(b,arglist)
    return mkdrv(mkconfig(cfg),matcher_,
                 build_wrapper(_make,nouts=nouts),r=r)
  return _deco


def wrapsig(f, extargs):
  sig=signature(f)
  args={k:v.default for k,v in sig.parameters.items()
        if v.default is not InspectParameter.empty}
  cm=set.intersection(set(args.keys()), set(extargs.keys()))
  if len(cm)>0:
    raise PylightnixException(f"Conflicting arguments: {cm}")
  args.update(extargs)
  accepts_build='build' in sig.parameters
  accepts_rindex='rindex' in sig.parameters
  def _call(build,args):
    args2={}
    for k in args.keys():
      if k in sig.parameters:
        args2[k]=args[k]
    if accepts_build:
      args2.update({'build':build})
    if accepts_rindex:
      assert 'rindex' in args, args
      args2.update({'rindex':args['rindex']})
    return f(**args2)
  return args,_call


def autodrv(*args,sourcedeps:List[Any]=[],**kwargs):
  def _deco(f:Callable[...,None])->Callable[...,DRef]:
    @autodrv_(*args,sourcedeps=[f]+sourcedeps,**kwargs) # type:ignore
    def _fn(build,arglist):
      for args in arglist:
        f(build=build,**args.__dict__)
    return _fn
  return _deco

def autostage_(f=None,
               *,
               nouts:int=1,
               matcher:Optional[Matcher]=None,
               always_multiref:bool=False,
               sourcedeps:List[Any]=[],
               r:Optional[Registry]=None,
               **decokw):
  r2=r
  def _deco(f:Callable[[Build,List[Any]],None])->Callable[...,DRef]:
    def _stage(r:Optional[Registry]=None,**stagekw)->DRef:
      kwargs:Dict[str,Any]={}
      kwargs.update(decokw)
      kwargs.update(stagekw)
      @autodrv_(sourcedeps=[f]+sourcedeps,nouts=nouts,matcher=matcher,
               always_multiref=always_multiref,r=(r or r2),**kwargs)
      def drv(build,arglist):
        f(build,arglist)
      return drv
    return _stage
  return _deco if f is None else _deco(f)


def autostage(fn=None,*,sourcedeps=[],r=None,**kwargs):
  """ Builds a Pylightnix [Stage](#pylightnix.types.Stage) out of a Python
  function. The decorator's arguments form the
  [Configuration](#pylightnix.types.Config) of a stage. After that, they go
  through the certain transformations and finally appear as the inner function's
  arguments. The transformation rules are explained in the table below.

  |Argument name in decorator|Argument type in decorator|Argument name in function| Argument type in function| Comment      |
  |:-----------:|:-----------:|:------------:|:-------------:|:---|
  | `r=None` | Optional[[Registry](#pylightnix.types.Registry)]  | - | - | Registry to register this stage in |
  | `sourcedeps=[]` | `List[Any]` | - | - | List of arbitrary Python objects to track by source in addition to the source of the wrapped function |
  | `matcher=match_latest` | [Matcher](#pylightnix.types.Matcher) | - | - | Matcher to set for this stage. |
  | `always_multiref=False` | `bool` | - | - | Set to `True` to represent dependencies as lists even if they include only one matched realization. |
  | x | [[selfref](#pylightnix.utils.selfref),str,...]  | x | `str` | A promise to produce a file or folder |
  | x | [DRef](#pylightnix.types.DRef) | x | [Attrs](#pylightnix.deco.Attrs) or `List[Attrs]` or [RRef](#pylightnix.types.RRef) or `List[RRef]` | Attrs with attributs of parent realization(s) or raw [Realization references](#pylightnix.types.RRef) |
  | x | t | x | t | JSON-compatible arguments (`bool`,`int`,`float`,`str`,lists and dicts of thereof) are passed without changes |
  | nouts=1 | int | rindex | int | Number of realizations to produce for this stage in one run (defaults to 1) |
  | - | - | `build` | [Build](#pylightnix.types.Build) | Build context for the current stage


  Example:
  ``` python
  with current_registry(Registry(S)) as r:
    @autostage
    def stage1(a=42):
      assert a==42
    @autostage(ref_stage1=stage1())
    def stage2(build,b=33,ref_stage1=stage1()):
      assert b==33
      assert ref_stage1.a==42
    r1=realize1(instantiate(stage2))
    assert mklens(r1,S=S).b.val==33
  ```
  """
  def _deco(f:Callable[...,None])->Callable[...,DRef]:
    kwargs2,f2=wrapsig(f,kwargs)
    @autostage_(sourcedeps=[f]+sourcedeps,r=r,**kwargs2) # type:ignore
    def _fn(build,arglist):
      for args in arglist:
        f2(build,args.__dict__)
    return _fn
  return _deco if fn is None else _deco(fn)


