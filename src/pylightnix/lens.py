
from pylightnix.imports import ( join )
from pylightnix.types import ( Any, Dict, List, Build, DRef, RRef, Optional,
    RefPath, Tuple, Union, Path )
from pylightnix.utils import ( isrefpath, isdref, isrref )
from pylightnix.core import ( build_path, store_deref, store_config, rref2dref,
    rref2path, config_dict, build_config, store_dref2path )


class Lens:
  def __init__(self, ctx:Tuple[Optional[Build],Optional[RRef]], v:Any)->None:
    self.ctx=ctx
    self.v=v

  def __getattr__(self, key)->Any:
    return self.get(key)

  def get(self, key)->Any:
    return Lens(self.ctx, self.as_dict()[key])

  @property
  def val(self)->Any:
    return self.v

  @property
  def refpath(self)->RefPath:
    assert isrefpath(self.v), f"Lens expected RefPath, but got {self.v}"
    return self.v

  @property
  def syspath(self)->Path:
    res=self.resolve()
    assert isinstance(res,Path), f"Lens didn't resolve itself into a syspath. Got {res} instead."
    return res

  @property
  def dref(self)->DRef:
    assert isdref(self.v), f"Lens expected DRef, but got {self.v}"
    return DRef(self.v)

  @property
  def rref(self)->RRef:
    assert isrref(self.v), f"Lens expected RRef, but got {self.v}"
    return RRef(self.v)

  def resolve(self)->Any:
    if isdref(self.v):
      return store_dref2path(DRef(self.v))
    elif isrref(self.v):
      return rref2path(RRef(self.v))
    elif isrefpath(self.v):
      refpath=RefPath(self.v)
      if self.ctx[0] is not None:
        return build_path(self.ctx[0], refpath)
      elif self.ctx[1] is not None:
        return Path(join(rref2path(store_deref(self.ctx[1], refpath[0])), *refpath[1:]))
    else:
      assert False, f"Lens doesn't know how to resolve {self.val}"

  def as_dict(self)->dict:
    if isdref(self.v):
      return config_dict(store_config(DRef(self.v)))
    elif isrref(self.v):
      return config_dict(store_config(rref2dref(RRef(self.v))))
    elif isinstance(self.v,Build):
      return config_dict(build_config(self.v))
    elif isinstance(self.v,dict):
      return self.v
    else:
      assert False, f"Can't get dict representation of {self.val}"


def mklens(x:Any, b:Optional[Build]=None, rref:Optional[RRef]=None)->Lens:
  return Lens((b,rref),x)

