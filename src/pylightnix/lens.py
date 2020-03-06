# Copyright 2020, Sergey Mironov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Lens module defines the `Lens` helper class, which offers quick navigation
through the dependent configurations """

from pylightnix.imports import ( join )
from pylightnix.types import ( Any, Dict, List, Build, DRef, RRef, Optional,
    RefPath, Tuple, Union, Path )
from pylightnix.utils import ( isrefpath, isdref, isrref )
from pylightnix.core import ( build_path, store_deref, store_config, rref2dref,
    rref2path, config_dict, build_config, store_dref2path )


class Lens:
  """ Lens objects provide quick access to the parameters of stage
  configurations by navigating through different kinds of Pylightnix entities
  like DRefs, RRefs, Configs and RefPaths.

  Lens lifecycle consists of three stages:
  1. Creation on the basis of existing objects. Lens may be created out of
     any Python value, but the meaningful operations (besides getting this value
     back) are supported for the Pylightnix types which could be casted to
     Python dictionaries. Those types are:
     - `Build` helper class
     - `DRef` references
     - `RRef` references
     - `RConfig` configuration wrappers
     - Regular Python dictionaries
  2. Navigation through the nested configurations. Lenses access configuration
     attributes, automatically dereference Pylightnix references and produce other
     Lenses, which are 'focused' on new locations.
  3. Access to the raw value which could no longer be converted into a Lens. In
     this case the raw value is returned.

  """
  def __init__(self, ctx:Tuple[Optional[Build],Optional[RRef]], v:Any)->None:
    self.ctx=ctx
    self.v=v

  def __getattr__(self, key)->Any:
    return self.get(key)

  def get(self, key)->Any:
    d=self.as_dict()
    return Lens(self.ctx, d[key] if key in d else None)

  @property
  def val(self)->Any:
    return self.v

  @property
  def refpath(self)->RefPath:
    assert isrefpath(self.v), f"Lens expected RefPath, but got '{self.v}'"
    return self.v

  @property
  def syspath(self)->Path:
    res=self.resolve()
    assert isinstance(res,Path), f"Lens didn't resolve itself into a syspath. Got '{res}' instead."
    return res

  @property
  def dref(self)->DRef:
    assert isdref(self.v), f"Lens expected DRef, but got '{self.v}'"
    return DRef(self.v)

  @property
  def rref(self)->RRef:
    assert isrref(self.v), f"Lens expected RRef, but got '{self.v}'"
    return RRef(self.v)

  def resolve(self)->Any:
    if isdref(self.v):
      return store_dref2path(DRef(self.v))
    elif isrref(self.v):
      return rref2path(RRef(self.v))
    elif isrefpath(self.v):
      refpath=list(self.v) # RefPath is list
      if self.ctx[0] is not None:
        return build_path(self.ctx[0], refpath)
      elif self.ctx[1] is not None:
        return Path(join(rref2path(store_deref(self.ctx[1], refpath[0])), *refpath[1:]))
      else:
        assert False, f"Lens couldn't resolve '{refpath}' without a context"
    else:
      assert False, f"Lens doesn't know how to resolve '{self.val}'"

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
  if isinstance(x,Build) and b is None:
    b=x
  elif isrref(x):
    rref=RRef(x)
  return Lens((b,rref),x)

