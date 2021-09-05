from pylightnix.imports import (join, mkdtemp, format_exc, isfile)

from pylightnix.types import (Dict, List, Any, Tuple, Union, Optional, Config,
                              Realizer, RealizerO, DRef, Context, RealizeArg,
                              RRef, Path, SPath, TypeVar, Generic, Callable,
                              Matcher, MatcherO, Registry, Output, Closure,
                              NamedTuple, StorageSettings)

from pylightnix.core import (assert_valid_config, drefcfg_, cfgcattrs,
                             cfghash, cfgname, context_deref,
                             assert_valid_refpath, rref2path, drefdeps1, mkdrv,
                             realize, output_validate, fstmpdir, realize1)

from pylightnix.utils import (readstr, writestr, readstr, tryread)

# FIXME: Get rid of this dependency. Maybe we need to define core exception
# `RealizeError`
from pylightnix.build import BuildError

#: _REF is either `Path` or `RRef`
_REF=TypeVar('_REF')

#: Alias for exception text
ExceptionText = str

class Either(Generic[_REF]):
  """ Either is a poor-man's `(EitherT Exception Ouput)` monad. It contains
  either (RIGHT) result of a realization or (LEFT) error report together with
  half-done results to show to the user.

  `Either` should be considered as an "upgrade" for regular Output, which allows
  user to record the fact of realization failure into the special kind of
  realization result rather than rasing an exception.

  TODO: Stress the attention on the fact that Either now encodes the list of
  items which may not have the same meaning. Some items may now be 'failed'
  and we may need a mapping function to apply matchers to them.

  TODO: Think about whether we should mark the fact that a stage uses Either
  wrappert in the stage configuration or not. Probably we should, because
  either-realizers in general are not backward-compatible with regular
  realizers.
  """
  def __init__(self, right:Optional[Output[_REF]]=None,
                     left:Optional[Tuple[List[_REF],ExceptionText]]=None):
    assert not ((right is None) and (left is None))
    self.right=right
    self.left=left

def mkright(o:Output[_REF])->Either[_REF]:
  """ Create a RIGHT Either """
  return Either(o,None)

def mkleft(paths:List[Path], exc:ExceptionText)->Either[Path]:
  """ Create a LEFT Either """
  for o in paths:
    assert not isfile(join(o,'either_status.txt')), (
      f"Realization '{o}' already contains a reserved file 'exception.txt'.")
    writestr(join(o,'either_status.txt'), exc)
  return Either(None,(paths,exc))

def either_paths(e:Either[_REF])->List[_REF]:
  if e.right is not None:
    return e.right.val
  else:
    assert e.left is not None
    assert len(e.left[0])>0
    return e.left[0]

def either_isRight(e:Either[_REF])->bool:
  return e.right is not None

def either_isLeft(e:Either[_REF])->bool:
  return e.left is not None

def either_status(e:Either[_REF])->Optional[ExceptionText]:
  return e.left[1] if e.left is not None else None

def either_loadR(rrefs:List[RRef], S)->Either[RRef]:
  ss=[]
  for rref in rrefs:
    err=tryread(Path(join(rref2path(rref,S),'either_status.txt')))
    if err is not None:
      ss.append(err)
  return Either(None,(rrefs,'\n'.join(ss))) if len(ss)>0 else \
         Either(Output(rrefs),None)





def either_validate(dref:DRef, e:Either[Path], S=None)->List[Path]:
  if e.right is not None:
    return output_validate(dref, e.right, S)
  else:
    assert e.left is not None
    assert len(e.left[0])>0
    return e.left[0]


def either_realizer(f:Callable[[Optional[StorageSettings],DRef,
                                Context,RealizeArg],Output[Path]],
                   )->Callable[[Optional[StorageSettings],DRef,
                                Context,RealizeArg],List[Path]]:
  """ Implements poor-man's `(EitherT Exception Ouput)` monad.
  Either, stages become either LEFT (if rasied an error) or
  RIGHT (after normal completion). If the stage turns LEFT, then so will be any
  of it's dependant stages.

  Stages which use `either_wrapper` typically don't use `claims` instead of
  `promises` to allow the existance of LEFT-versions of themselves.

  Either-stages should use appropriate matchers which supports LEFT-mode.
  """
  # import pylightnix.core

  def _either(S, dref:DRef, ctx:Context, ra:RealizeArg)->Either[Path]:
    # Scan the statuses of immediate dependecnies, and propagate the 'LEFT'
    # condition if any of them has it.
    tmp=fstmpdir(S)
    e2:Either[Path]
    for dref_dep in drefdeps1([dref],S):
      e=either_loadR(context_deref(ctx,dref_dep),S)
      if e.left is not None:
        return mkleft([Path(mkdtemp(prefix="either_tmp", dir=tmp))],e.left[1])

    # Execute the wrapped builder
    try:
      return mkright(f(S,dref,ctx,ra))
    except KeyboardInterrupt:
      raise
    # FIXME: Introduce the type of exception which would posess information
    # about incompleted paths, then rewrite the following:
    # except BuildError as be:
    #   outpaths=be.outgroups
    #   _mark_status(outpaths, 'LEFT', format_exc())
    except Exception:
      return mkleft([Path(mkdtemp(prefix="either_tmp", dir=tmp))], format_exc())

  def _r(S:Optional[StorageSettings],dref:DRef,
         ctx:Context,ra:RealizeArg)->List[Path]:
    """ Obtain the structured result and validate it """
    e=_either(S,dref,ctx,ra)
    return either_validate(dref,e,S)

  return _r

def either_matcher(m:MatcherO)->Matcher:
  """ Convert an Either-matcher into the regular Matcher """
  def _matcher(S:Optional[StorageSettings],
               rrefs:List[RRef])->Optional[List[RRef]]:
    erefs=either_loadR(rrefs, S)
    if erefs.right is not None:
      o2=m(S,erefs.right)
      return o2.val if o2 is not None else None
    else:
      assert erefs.left is not None
    return erefs.left[0]
  return _matcher

def mkdrvE(config:Config,
           matcher:MatcherO,
           realizer:RealizerO,
           m:Optional[Registry]=None
           )->DRef:
  return mkdrv(config, either_matcher(matcher), either_realizer(realizer), m)

def realizeE(closure:Closure,
             force_rebuild:Union[List[DRef],bool]=[],
             assert_realized:List[DRef]=[],
             realize_args:Dict[DRef,RealizeArg]={})->Either[RRef]:
  rref=realize1(closure,force_rebuild,assert_realized,realize_args)
  return either_loadR([rref],closure.S)

def realizeManyE(closure:Union[Closure,Tuple[Any,Closure]],
             force_rebuild:Union[List[DRef],bool]=[],
             assert_realized:List[DRef]=[],
             realize_args:Dict[DRef,RealizeArg]={})->Either[RRef]:
  _,clo,ctx=realize(closure,force_rebuild,assert_realized,realize_args)
  assert len(ctx.keys())==1
  return either_loadR(list(ctx.values())[0],clo.S)


