from pylightnix.imports import (join, mkdtemp, format_exc)

from pylightnix.types import (Dict, List, Any, Tuple, Union, Optional, Config,
                              Realizer, DRef, Context, RealizeArg, RRef, Path,
                              SPath)

from pylightnix.core import (assert_valid_config, drefcfg_, config_cattrs,
                             config_hash, config_name, context_deref,
                             assert_valid_refpath, store_rref2path, store_deps)

from pylightnix.utils import (readstr, writestr, readstr, tryreadstr_def)

# FIXME: Get rid of this dependency. Maybe we need to define core exception
# `RealizeError`
from pylightnix.build import BuildError


def either_wrapper(f:Realizer)->Realizer:
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

  def _either(S:SPath, dref:DRef, ctx:Context, ra:RealizeArg)->List[Path]:
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
    for dref_dep in store_deps([dref],S):
      for rref in context_deref(ctx,dref_dep):
        status=tryreadstr_def(join(store_rref2path(rref,S),'status_either.txt'), 'RIGHT')
        if status=='RIGHT':
          continue
        elif status=='LEFT':
          outpaths=[Path(mkdtemp(prefix="either_tmp", dir=tmp))]
          _mark_status(outpaths, 'LEFT')
          return outpaths
        else:
          assert False, f"Invalid either status {status}"

    # Execute the original build
    try:
      outpaths=f(S,dref,ctx,ra)
      _mark_status(outpaths, 'RIGHT')
    except KeyboardInterrupt:
      raise
    # FIXME: repair build
    # except BuildError as be:
    #   outpaths=be.outgroups
    #   _mark_status(outpaths, 'LEFT', format_exc())
    except Exception:
      outpaths=[Path(mkdtemp(prefix="either_tmp", dir=tmp))]
      _mark_status(outpaths, 'LEFT', format_exc())

    # Return either valid artifacts or a LEFT-substitute
    return outpaths

  return _either

def either_status(rref:RRef,S=None)->str:
  return readstr(join(store_rref2path(rref,S),'status_either.txt'))

def either_isRight(rref:RRef,S=None)->bool:
  return either_status(rref,S)=='RIGHT'

def either_isLeft(rref:RRef,S=None)->bool:
  return either_status(rref,S)=='LEFT'

