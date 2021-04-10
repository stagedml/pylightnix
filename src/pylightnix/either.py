from pylightnix.imports import (join, mkdtemp, format_exc)

from pylightnix.types import (Dict, List, Any, Tuple, Union, Optional, Config,
                              Realizer, DRef, Context, RealizeArg, RRef, Path,
                              SPath, TypeVar, Generic, Callable, OutputBase,
                              Matcher, Manager, Output)

from pylightnix.core import (assert_valid_config, drefcfg_, config_cattrs,
                             config_hash, config_name, context_deref,
                             assert_valid_refpath, rref2path, drefdeps1, mkdrv)

from pylightnix.utils import (readstr, writestr, readstr, tryreadstr_def)

# FIXME: Get rid of this dependency. Maybe we need to define core exception
# `RealizeError`
from pylightnix.build import BuildError

_A = TypeVar('_A', bound=OutputBase)
class Either(Generic[_A],OutputBase):
  val:Union[Exception,_A]
  def __init__(self, val:_A):
    self.val=val
  def get(self)->List[Path]:
    if isinstance(self.val,Exception):
      return []
    elif isinstance(self.val,OutputBase):
      return self.val.get()
    else:
      assert False


def either_status(rref:RRef,S=None)->str:
  return tryreadstr_def(join(rref2path(rref,S),'status_either.txt'),'RIGHT')

def either_isRight(rref:RRef,S=None)->bool:
  return either_status(rref,S)=='RIGHT'

def either_isLeft(rref:RRef,S=None)->bool:
  return either_status(rref,S)=='LEFT'


_B = TypeVar('_B', bound=OutputBase)
def either_realizer(f:Callable[[SPath,DRef,Context,RealizeArg],Either[_B]],
                   inject:Callable[[Path],_B]
                   )->Callable[[SPath,DRef,Context,RealizeArg],_B]:
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

  def _either(S:SPath, dref:DRef, ctx:Context, ra:RealizeArg)->_B:
    # Write the specified build status to every output
    def _mark_status(outpaths:List[Path],
                     status:str,
                     exception:Optional[str]=None)->None:
      for o in outpaths:
        writestr(join(o,'status_either.txt'), status)
        if exception is not None:
          writestr(join(o,'exception.txt'), exception)

    # Scan all immediate dependecnies of this build, propagate the 'LEFT' status
    # if any of them has it.
    for dref_dep in drefdeps1([dref],S):
      for rref in context_deref(ctx,dref_dep):
        if either_isLeft(rref):
          outpath=Path(mkdtemp(prefix="either_tmp", dir=tmp))
          _mark_status([outpath], 'LEFT')
          return inject(outpath)

    # Execute the original build
    try:
      outpaths=f(S,dref,ctx,ra)
      assert not isinstance(outpaths.val,Exception)
      _mark_status(outpaths.get(), 'RIGHT')
      return outpaths.val
    except KeyboardInterrupt:
      raise
    # FIXME: repair build
    # except BuildError as be:
    #   outpaths=be.outgroups
    #   _mark_status(outpaths, 'LEFT', format_exc())
    except Exception:
      outpath=Path(mkdtemp(prefix="either_tmp", dir=tmp))
      _mark_status([outpath], 'LEFT', format_exc())
      return inject(outpath)

    # Return either valid artifacts or a LEFT-substitute
    return outpath

  return _either

def either_matcher(m:Matcher)->Matcher:
  return m

# def mkdrvE(m:Manager, config:Config,
#            matcher:Matcher,
#            realizer:Callable[[SPath,DRef,Context,RealizeArg],Either[Output]]
#            )->DRef:
#   def _inject(p:Path)->Output:
#     return Output([p])
#   return mkdrv(m, config, either_matcher(matcher), either_realizer(realizer,_inject))


