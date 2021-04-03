from pylightnix.imports import (chain, join, isfile, isdir, islink, defaultdict)

from pylightnix.types import (Any, DRef, RRef, Dict, List, Union, RealizeArg,
                              Realizer, Closure, Iterable, Optional, Matcher,
                              SPath, Context, Tuple, Callable, Config, Path,
                              RConfig, Manager, Set, Hash, NewType, RefPath,
                              OutputBase)

from pylightnix.core import (realizeSeq, drefrrefsC, rref2path, unrref,
                             reserved, drefcfg, mkrealization, rref2dref,
                             mkdrv, context_deref, config_dict, isselfpath)

from pylightnix.utils import (parsetime, tryreadjson_def, traverse_dict, isrref,
                              isdref, dirhash, writejson, readjson, concat)

from typing import TypeVar, Generic


_A = TypeVar('_A', bound=OutputBase)
class Promising(Generic[_A], OutputBase):
  val:_A
  promising:List[Path]
  def __init__(self, val:_A, ps:List[Path]):
    self.val=val
    self.promising=ps
  def get(self)->List[Path]:
    return self.val.get()


def cfgpromises(c:Config, r:DRef)->List[Tuple[str,RefPath]]:
  promises=[]
  def _mut(key:Any, val:Any):
    nonlocal promises
    if isselfpath(val):
      promises.append((str(key),val))
    return val
  traverse_dict(config_dict(c),_mut)
  return promises


def assert_promise_fulfilled(k:str, p:RefPath, o:Path)->None:
  ppath=join(o,*p[1:])
  assert isfile(ppath) or isdir(ppath) or islink(ppath), (
      f"Promise '{k}' of {p[0]} is not fulfilled. "
      f"{ppath} is expected to be a file or a directory.")


_B = TypeVar('_B', bound=OutputBase)
def checkpromise(r:Callable[[SPath,DRef,Context,RealizeArg],Promising[_B]]
                 )->Callable[[SPath,DRef,Context,RealizeArg],_B]:
  def _realizer(S:SPath, dref:DRef, ctx:Context, ra:RealizeArg)->_B:
    p=r(S,dref,ctx,ra)
    for ppath in p.promising:
      for key,val in cfgpromises(drefcfg(dref,S),dref):
        assert_promise_fulfilled(key,val,ppath)
    return p.val
  return _realizer

