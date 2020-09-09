from pylightnix.imports import (join, mkdtemp, format_exc)
from pylightnix.types import (Dict, List, Any, Tuple, Union, Optional, Config,
                              Realizer, DRef, Context, RealizeArg, RRef, Tag,
                              Path)

from pylightnix.core import (assert_valid_config, store_config, config_cattrs,
                             config_hash, config_name, context_deref,
                             assert_valid_refpath, rref2path, tag_out,
                             store_deps)

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

  def _either(dref:DRef, ctx:Context, ra:RealizeArg)->List[Dict[Tag,Path]]:
    # Write the specified build status to every output
    def _mark_status(outpaths:List[Dict[Tag,Path]],
                     status:str,
                     exception:Optional[str]=None)->None:
      for rg in outpaths:
        o=rg[tag_out()]
        writestr(join(o,'status_either.txt'), status)
        if exception is not None:
          writestr(join(o,'exception.txt'), exception)

    # Scan all immediate dependecnies of this build, propagate 'LEFT' status
    for dref_dep in store_deps([dref]):
      for rg in context_deref(ctx, dref_dep):
        rref = rg[tag_out()]
        status=tryreadstr_def(join(rref2path(rref),'status_either.txt'), 'RIGHT')
        if status=='RIGHT':
          continue
        elif status=='LEFT':
          outpaths=[{tag_out(): Path(mkdtemp(prefix="either_tmp", dir=tmp))}]
          _mark_status(outpaths, 'LEFT')
          return outpaths
        else:
          assert False, f"Invalid either status {status}"

    # Execute the original build
    try:
      outpaths=f(dref,ctx,ra)
      _mark_status(outpaths, 'RIGHT')
    except KeyboardInterrupt:
      raise
    except BuildError as be:
      outpaths=be.outgroups
      _mark_status(outpaths, 'LEFT', format_exc())
    except Exception:
      outpaths=[{tag_out(): Path(mkdtemp(prefix="either_tmp", dir=tmp))}]
      _mark_status(outpaths, 'LEFT', format_exc())

    # Return either valid artifacts or a LEFT-substitute
    return outpaths

  return _either

def either_status(rref:RRef)->str:
  return readstr(join(rref2path(rref),'status_either.txt'))

def either_isRight(rref:RRef)->bool:
  return either_status(rref)=='RIGHT'

def either_isLeft(rref:RRef)->bool:
  return either_status(rref)=='LEFT'

