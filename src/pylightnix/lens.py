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
    RefPath, Tuple, Union, Path, Context )
from pylightnix.utils import ( isrefpath, isdref, isrref )
from pylightnix.core import ( store_deref, store_config, rref2dref, rref2path,
    config_dict, build_outpath, build_config, build_context, store_dref2path,
    store_context, context_deref, context_add )


class Lens:
  """ Lens objects provide quick access to the parameters of stage
  configurations by navigating through different kinds of Pylightnix entities
  like DRefs, RRefs, Configs and RefPaths.

  Lens lifecycle consists of three stages:
  1. Creation on the basis of existing objects. Lens may be created out of
     any Python value, but the meaningful operations (besides getting this value
     back) are supported for the Pylightnix types which could be casted to
     Python dictionaries. See [mklens](#pylightnix.lens.mklens) for the list of
     supported source objects.
  2. Navigation through the nested configurations. Lenses access configuration
     attributes, automatically dereference Pylightnix references and produce other
     Lenses, which are 'focused' on new locations.
  3. Access to the raw value which could no longer be converted into a Lens. In
     this case the raw value is returned.

  To create Lenses, use `mklens` function rather than creating it directly
  because it encodes a number of supported ways of deducing `ctx` of Lens.
  """
  def __init__(self, ctx:Tuple[Optional[Path],Optional[Context]], v:Any)->None:
    self.ctx=ctx
    self.v=v

  def __getattr__(self, key)->"Lens":
    """ Sugar for `Lens.get` """
    return self.get(key)

  def get(self, key)->"Lens":
    """ Return a new Lens out of the `key` attribute of the current Lens """
    d=self.as_dict()
    return Lens(self.ctx, d[key] if key in d else None)

  @property
  def val(self)->Any:
    """ Return th current value of Lens as-is """
    return self.v

  @property
  def refpath(self)->RefPath:
    """ Check that the current value of Lens is a `RefPath` and return it """
    assert isrefpath(self.v), f"Lens expected RefPath, but got '{self.v}'"
    return self.v

  @property
  def syspath(self)->Path:
    """ Check that the current value of Lens is a `Path` and return it """
    res=self.resolve()
    assert isinstance(res,Path), f"Lens didn't resolve itself into a syspath. Got '{res}' instead."
    return res

  @property
  def dref(self)->DRef:
    """ Check that the current value of Lens is a `DRef` and return it """
    assert isdref(self.v), f"Lens expected DRef, but got '{self.v}'"
    return DRef(self.v)

  @property
  def rref(self)->RRef:
    """ Check that the current value of Lens is an `RRef` and return it """
    assert isrref(self.v), f"Lens expected RRef, but got '{self.v}'"
    return RRef(self.v)

  def resolve(self)->Path:
    """ Resolve the current value of Lens into system path. Assert if it is not
    possible or if the result is associated with multiple paths."""
    if isdref(self.v):
      return store_dref2path(DRef(self.v))
    elif isrref(self.v):
      return rref2path(RRef(self.v))
    elif isrefpath(self.v):
      refpath=list(self.v) # RefPath is list
      bpath=self.ctx[0]
      context=self.ctx[1]
      if context is not None:
        if refpath[0] in context:
          rrefs=context_deref(context, refpath[0])
          assert len(rrefs)==1, "Lens doesn't support multirealization dependencies"
          return Path(join(rref2path(rrefs[0]), *refpath[1:]))
        else:
          if bpath is not None:
            return Path(join(bpath, *refpath[1:]))
          else:
            assert False, f"Can't dereference refpath {refpath}"
      else:
        assert False, f"Lens couldn't resolve '{refpath}' without a context"
    else:
      assert False, f"Lens doesn't know how to resolve '{self.val}'"

  def as_dict(self)->dict:
    """ Return the `dict` representation of the Lens, asserting that it is possible. """
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


def mklens(x:Any, o:Optional[Path]=None,
                  b:Optional[Build]=None,
                  rref:Optional[RRef]=None,
                  ctx:Optional[Context]=None)->Lens:
  """ Mklens creates [Lenses](#pylightnix.lens.Lens) from various user objects.

  Arguments:
  - `x:Any` The object to create the Lens from. Supported source object types
    are:
    * `RRefs`
    * `DRefs`
    * `Build`
    * `RefPath`
    * `dict`
  - `b:Optional[Build]=None` Optional `Build` context of the Lens. Passing this
    object would allow Lens to resolve RRefs using the Context of the current
    realization. Also it would allow the Lens to use
    [build_path](#pylightnix.core.build_path) function to
    resolve Build paths.
  - `rref:Optional[RRef]=None` Optional `RRef` link. Passing this object will
    allow Lens to resolve other RRefs using the Context of the given RRef.
  - `ctx:Optional[Context]=None` Passing optional Context would allow Lens to
    resolve RRefs.

  """
  if ctx is None and b is not None:
    ctx=build_context(b)
  if ctx is None and isinstance(x,Build):
    ctx=build_context(x)
  if ctx is None and rref is not None:
    ctx=store_context(rref)
  if ctx is None and isrref(x):
    ctx=context_add(store_context(RRef(x)), rref2dref(RRef(x)), [RRef(x)])
  if o is None and b is not None:
    o=build_outpath(b)
  if o is None and isinstance(x,Build):
    o=build_outpath(x)
  return Lens((o,ctx),x)

