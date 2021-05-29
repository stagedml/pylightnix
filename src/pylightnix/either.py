from pylightnix.imports import (join, mkdtemp, format_exc, isfile)

from pylightnix.types import (Dict, List, Any, Tuple, Union, Optional, Config,
                              Realizer, DRef, Context, RealizeArg, RRef, Path,
                              SPath, TypeVar, Generic, Callable, EquivClasses,
                              Matcher, Manager, Output, Closure)

from pylightnix.core import (assert_valid_config, drefcfg_, config_cattrs,
                             config_hash, config_name, context_deref,
                             assert_valid_refpath, rref2path, drefdeps1, mkdrv,
                             realizeMany)

from pylightnix.utils import (readstr, writestr, readstr, tryread)

# FIXME: Get rid of this dependency. Maybe we need to define core exception
# `RealizeError`
from pylightnix.build import BuildError

_REF=TypeVar('_REF')
ExceptionText = str
class Either(Generic[_REF]):
  """ Either encodes a poor-man's `(EitherT Exception Ouput)` monad.  The
  structure contains either RIGHT realization results or (LEFT) error report
  together with half-done results which should nevertheless be kept.

  `Either` should be considered as an "upgrade" for regular Output, which allows
  user to record the fact of realization failure into the special kind of
  realization result rather than rasing an exception.

  TODO: Stress the attention on the fact that Either now encodes the list of
  items which may not have the same meaning. Some of items may now be 'failed'
  and we may need a mapping function to apply matchers to them.

  TODO: Think about whether we should mark the fact that a stage uses Either
  wrappert in the stage configuration or not. Probably we should, because
  either-realizers in general are not backward-compatible with regular
  realizers.
  """
  def __init__(self, right:Optional[Output[_REF]]=None, left=None):
    assert not ((right is None) and (left is None))
    self.right:Optional[Output[_REF]]=right
    self.left:Optional[Tuple[List[_REF],ExceptionText]]=left

def either_output(e:Either[Path])->Output:
  """ Return the Output based on Either value `e`, be it the successful or the
  failed one """
  if e.right is not None:
    return e.right
  else:
    assert e.left is not None
    assert len(e.left[0])>0
    return Output(e.left[0])

def either_paths(e:Either[_REF])->List[_REF]:
  if e.right is not None:
    return e.right.val
  else:
    assert e.left is not None
    return e.left[0]

def either_dump(e:Either[Path])->None:
  """ Write the build status to every output of the collection `e`. """
  for o in either_paths(e):
    assert not isfile(join(o,'either_status.txt')), (
      f"Realization '{o}' already contains a reserved file 'exception.txt'.")
    if e.left is not None:
      writestr(join(o,'either_status.txt'), e.left[1])

def either_isRight(e:Either[_REF])->bool:
  return e.right is not None

def either_isLeft(e:Either[_REF])->bool:
  return e.left is not None

def either_status(p:Path)->Optional[ExceptionText]:
  return tryread(Path(join(p,'either_status.txt')))

def either_loadP(paths:List[Path])->Either[Path]:
  val=Output(paths)
  ss=[either_status(p) for p in paths if either_status(p) is not None]
  return Either(val,ss[0] if len(ss)>0 else None)

def either_loadO(o:Output[RRef], S)->Either[RRef]:
  ss=[either_status(rref2path(p,S))
      for p in o.val if either_status(rref2path(p,S)) is not None]
  return Either(o,ss[0] if len(ss)>0 else None)


MatcherE = Callable[[SPath,Either[RRef]],Optional[Either[RRef]]]

RealizerE = Callable[[SPath,DRef,Context,RealizeArg],Either[Path]]

def either_realizer(f:Callable[[SPath,DRef,Context,RealizeArg],Either[Path]],
                   )->Callable[[SPath,DRef,Context,RealizeArg],Output[Path]]:
  """ Implements poor-man's `(EitherT Exception Ouput)` monad.
  Either, stages become either LEFT (if rasied an error) or
  RIGHT (after normal completion). If the stage turns LEFT, then so will be any
  of it's dependant stages.

  Stages which use `either_wrapper` typically don't use `claims` instead of
  `promises` to allow the existance of LEFT-versions of themselves.

  Either-stages should use appropriate matchers which supports LEFT-mode.
  """
  import pylightnix.core
  tmp=pylightnix.core.PYLIGHTNIX_TMP

  def _either(S:SPath, dref:DRef, ctx:Context, ra:RealizeArg)->Output:
    # Scan the statuses of immediate dependecnies, and propagate the 'LEFT'
    # condition if any of them has it.
    e2:Either[Path]
    for dref_dep in drefdeps1([dref],S):
      e=either_loadO(Output(context_deref(ctx,dref_dep)),S)
      if e.left is not None:
        outpath=Path(mkdtemp(prefix="either_tmp", dir=tmp))
        e2=Either(left=([outpath,e.left[1]]))
        either_dump(e2)
        return either_output(e2)

    # Execute the wrapped builder
    try:
      e2=f(S,dref,ctx,ra)
      assert e2.right is not None
      either_dump(e2)
      return e2.right
    except KeyboardInterrupt:
      raise
    # FIXME: repair build
    # except BuildError as be:
    #   outpaths=be.outgroups
    #   _mark_status(outpaths, 'LEFT', format_exc())
    except Exception:
      outpath=Path(mkdtemp(prefix="either_tmp", dir=tmp))
      e2=Either(left=([outpath],format_exc()))
      either_dump(e2)
      return either_output(e2)

  return _either


def either_matcher(m:Callable[[SPath,Either[RRef]],Optional[Either[RRef]]],
                   )->Matcher:
  """ Convert an Either-matcher into the regular Matcher """
  def _matcher(S:SPath,rrefs:Output[RRef])->Optional[Output[RRef]]:
    erefs=m(S,either_loadR(rrefs.promisers(), S, inject))
    return Output(erefs.promisers()) if erefs is not None else None
  return _matcher

def _injectP(ps:List[Path])->Output[Path]:
  return Output(ps)
def _injectR(rs:List[RRef])->Output[RRef]:
  return Output(rs)

def mkdrvE(m:Manager,
           config:Config,
           matcher:MatcherE,
           realizer:RealizerE
           )->DRef:
  return mkdrv(m, config,
               either_matcher(matcher,_injectR),
               either_realizer(realizer,_injectP))


# def match_right(m:Callable[[SPath,_A],Optional[_A]]
#                 )->Callable[[SPath, Either[RRef,_A]],Optional[Either[RRef,_A]]]:
#   def _matcher(S:SPath,col:Either[RRef,_A])->Optional[Either[RRef,_A]]:
#     if col.exc is not None:
#       return col
#     val=m(S,col.val)
#     return Either(val) if val is not None else None
#   return _matcher


def realizeE(closure:Closure,
             force_rebuild:Union[List[DRef],bool]=[],
             assert_realized:List[DRef]=[],
             realize_args:Dict[DRef,RealizeArg]={})->Either[RRef,Output]:
  rrefs=realizeMany(closure,force_rebuild,assert_realized,realize_args)
  return either_loadR(rrefs,closure.storage,_injectR)


