from pylightnix.imports import (join, mkdtemp, format_exc, isfile)

from pylightnix.types import (Dict, List, Any, Tuple, Union, Optional, Config,
                              Realizer, DRef, Context, RealizeArg, RRef, Path,
                              SPath, TypeVar, Generic, Callable, EquivClasses,
                              Matcher, Manager, Output)

from pylightnix.core import (assert_valid_config, drefcfg_, config_cattrs,
                             config_hash, config_name, context_deref,
                             assert_valid_refpath, rref2path, drefdeps1, mkdrv)

from pylightnix.utils import (readstr, writestr, readstr, tryread)

# FIXME: Get rid of this dependency. Maybe we need to define core exception
# `RealizeError`
from pylightnix.build import BuildError

ExceptionText = str

_REF=TypeVar('_REF')
_A = TypeVar('_A', bound=EquivClasses)
class Either(Generic[_REF,_A],EquivClasses[_REF]):
  val:_A
  exc:Optional[ExceptionText]
  def __init__(self, val:_A, exc:Optional[ExceptionText]=None):
    self.val=val
    self.exc=exc
  def n(self)->int:
    return 1 if self.exc else self.val.n()
  def all(self)->List[_REF]:
    return self.val.all()


def either_status(p:Path)->Optional[ExceptionText]:
  return tryread(Path(join(p,'either_status.txt')))

def either_isRight(p:Path)->bool:
  return either_status(p) is None

def either_isLeft(p:Path)->bool:
  return either_status(p) is not None

def either_set(outpaths:List[Path],
               exception:Optional[str]=None)->None:
  """ Write the specified build status to every output """
  for o in outpaths:
    assert not isfile(join(o,'either_status.txt')), (
      f"Realization '{o}' already contains a reserved file 'exception.txt'.")
    if exception is not None:
      writestr(join(o,'either_status.txt'), exception)

def either_loadP(paths:List[Path], inject:Callable[[List[Path]],_A])->Either[Path,_A]:
  val=inject(paths)
  ss=[either_status(p) for p in paths if either_status(p) is not None]
  return Either(val,ss[0] if len(ss)>0 else None)

def either_loadR(rrefs:List[RRef], S, inject:Callable[[List[RRef]],_A])->Either[RRef,_A]:
  val=inject(rrefs)
  ss=[either_status(rref2path(p,S)) for p in rrefs if either_status(rref2path(p,S)) is not None]
  return Either(val,ss[0] if len(ss)>0 else None)


MatcherE = Callable[[SPath,Either[RRef,_A]],Optional[Either[RRef,_A]]]

RealizerE = Callable[[SPath,DRef,Context,RealizeArg],Either[Path, _A]]

def either_realizer(f:Callable[[SPath,DRef,Context,RealizeArg],Either[Path,_A]],
                   inject:Callable[[List[Path]],_A]
                   )->Callable[[SPath,DRef,Context,RealizeArg],_A]:
  """ This wrapper implements poor-man's `(EitherT Error)` monad on stages.
  With this wrapper, stages could become either LEFT (if rasied an error) or
  RIGHT (after normal completion). If the stage turns LEFT, then so will be any
  of it's dependant stages.

  Stages which use `either_wrapper` typically don't use `claims` instead of
  `promises` to allow the existance of LEFT-versions of themselves.

  Either-stages should use appropriate matchers which supports LEFT-mode.
  """
  import pylightnix.core
  tmp=pylightnix.core.PYLIGHTNIX_TMP

  def _either(S:SPath, dref:DRef, ctx:Context, ra:RealizeArg)->_A:
    # Scan the statuses of immediate dependecnies, and propagate the 'LEFT'
    # status if any of them has it.
    for dref_dep in drefdeps1([dref],S):
      for rref in context_deref(ctx,dref_dep):
        status=either_status(rref2path(rref,S))
        if status is not None:
          outpath=Path(mkdtemp(prefix="either_tmp", dir=tmp))
          either_set([outpath], status)
          return inject([outpath])

    # Execute the original build
    try:
      outpaths=f(S,dref,ctx,ra)
      either_set(outpaths.all(), outpaths.exc)
      return outpaths.val
    except KeyboardInterrupt:
      raise
    # FIXME: repair build
    # except BuildError as be:
    #   outpaths=be.outgroups
    #   _mark_status(outpaths, 'LEFT', format_exc())
    except Exception:
      outpath=Path(mkdtemp(prefix="either_tmp", dir=tmp))
      either_set([outpath], format_exc())
      return inject([outpath])

    # Return either valid artifacts or a LEFT-substitute
    return outpath
  return _either


def either_matcher(m:Callable[[SPath,Either[RRef,_A]],Optional[Either[RRef,_A]]],
                   inject:Callable[[List[RRef]],_A])->Matcher:
  """ Convert an Either-matcher into the regular Matcher """
  def _matcher(S:SPath,rrefs:Output[RRef])->Optional[Output[RRef]]:
    erefs=m(S,either_loadR(rrefs.all(), S, inject))
    return Output(erefs.all()) if erefs is not None else None
  return _matcher



def mkdrvE(m:Manager,
           config:Config,
           matcher:MatcherE,
           realizer:RealizerE
           )->DRef:
  def _injectP(ps:List[Path])->Output[Path]:
    return Output(ps)
  def _injectR(rs:List[RRef])->Output[RRef]:
    return Output(rs)
  return mkdrv(m, config,
               either_matcher(matcher,_injectR),
               either_realizer(realizer,_injectP))


def match_right(m:Callable[[SPath,_A],Optional[_A]]
                )->Callable[[SPath, Either[RRef,_A]],Optional[Either[RRef,_A]]]:
  def _matcher(S:SPath,col:Either[RRef,_A])->Optional[Either[RRef,_A]]:
    if col.exc is not None:
      return col
    val=m(S,col.val)
    return Either(val) if val is not None else None
  return _matcher


