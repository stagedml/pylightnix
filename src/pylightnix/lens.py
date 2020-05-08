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
    RefPath, Tuple, Union, Path, Context, Tag )
from pylightnix.utils import ( isrefpath, isdref, isrref )
from pylightnix.core import ( store_deref, store_config, rref2dref, rref2path,
    config_dict, store_dref2path, store_context, context_deref, context_add )
from pylightnix.build import ( build_outpaths, build_config, build_context )


def val2dict(v:Any)->Optional[dict]:
  """ Return the `dict` representation of the Lens, asserting that it is possible. """
  if isdref(v):
    return config_dict(store_config(DRef(v)))
  elif isrref(v):
    return config_dict(store_config(rref2dref(RRef(v))))
  elif isinstance(v,Build):
    return config_dict(build_config(v))
  elif isinstance(v,dict):
    return v
  else:
    return None


def val2path(v:Any, ctx:Tuple[Any,Any])->Path:
  """ Resolve the current value of Lens into system path. Assert if it is not
  possible or if the result is associated with multiple paths."""
  if isdref(v):
    return store_dref2path(DRef(v))
  elif isrref(v):
    return rref2path(RRef(v))
  elif isrefpath(v):
    refpath=list(v) # RefPath is list
    bpath=ctx[0]
    context=ctx[1]
    if context is not None:
      if refpath[0] in context:
        rgs=context_deref(context, refpath[0])
        assert len(rgs)==1, "Lens doesn't support multirealization dependencies"
        return Path(join(rref2path(rgs[0][Tag('out')]), *refpath[1:]))
      else:
        if bpath is not None:
          # FIXME: should we assert on refpath[0]==build.dref ?
          return Path(join(bpath, *refpath[1:]))
        else:
          assert False, f"Can't dereference refpath {refpath}"
    else:
      assert False, f"Lens couldn't resolve '{refpath}' without a context"
  else:
    assert False, f"Lens doesn't know how to resolve '{v}'"

def val2rref(v:Any, ctx)->RRef:
  if isdref(v):
    dref=DRef(v)
    context=ctx[1]
    if context is not None:
      if dref in context:
        rgs=context_deref(context, dref)
        assert len(rgs)==1, "Lens doesn't support multirealization dependencies"
        return rgs[0][Tag('out')]
      else:
        assert False, f"Can't convert {dref} into RRef because it is not in context"
    else:
      assert False, f"Lens couldn't resolve '{dref}' without a context"
  assert isrref(v), f"Lens expected RRef, but got '{v}'"
  return RRef(v)

def traverse(l:"Lens")->Any:
  val=l.start
  for s in l.steps:
    d=val2dict(val)
    if d is None:
      assert False, f"Lens {'.'.join(l.steps)} can't be traversed"
    val=d[s]
  return val

def mutate(l:"Lens", v:Any)->None:
  assert len(l.steps)>0, f"Fields to set are not specified"
  val=l.start
  for s in l.steps[:-1]:
    assert isinstance(val,dict), f"Lens {'.'.join(l.steps)} can't be mutated"
    assert s in val, f"Lens {'.'.join(l.steps)} can't be mutated"
    val=val[s]
  val[l.steps[-1]]=v

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
  def __init__(self, ctx:Tuple[Optional[Path],Optional[Context]],
                     start:Any,
                     steps:List[str])->None:
    self.ctx=ctx
    self.start=start
    self.steps=steps

  def __getattr__(self, key)->"Lens":
    """ Sugar for `Lens.get` """
    return self.get(key)

  def get(self, key)->"Lens":
    """ Return a new Lens out of the `key` attribute of the current Lens """
    d=val2dict(traverse(self))
    assert d is not None
    assert key in d
    return Lens(self.ctx, self.start, self.steps+[key])

  @property
  def optval(self)->Optional[Any]:
    """ Return the value of Lens as-is """
    v=traverse(self)
    return v

  @property
  def val(self)->Any:
    """ Return the value of Lens as-is, assuming it is not None """
    v=traverse(self)
    assert v is not None
    return v

  @val.setter
  def val(self, v):
    mutate(self,v)

  @property
  def refpath(self)->RefPath:
    """ Check that the current value of Lens is a `RefPath` and return it """
    v=traverse(self)
    assert isrefpath(v), f"Lens expected RefPath, but got '{v}'"
    return v

  @property
  def dref(self)->DRef:
    """ Check that the current value of Lens is a `DRef` and return it """
    v=traverse(self)
    assert isdref(v), f"Lens expected DRef, but got '{v}'"
    return DRef(v)

  @property
  def syspath(self)->Path:
    """ Check that the current value of Lens is a `Path` and return it """
    v=traverse(self)
    return val2path(v, self.ctx)

  @property
  def rref(self)->RRef:
    """ Check that the current value of Lens is an `RRef` and return it """
    v=traverse(self)
    return val2rref(v, self.ctx)


def mklens(x:Any, o:Optional[Path]=None,
                  b:Optional[Build]=None,
                  rref:Optional[RRef]=None,
                  ctx:Optional[Context]=None,
                  build_output_idx:int=0)->Lens:
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
  - `build_output_idx:int=0` For `Builds`, specify the index of output path,
    defaulted to zero

  Examples:
  ```Python
  stage=partial(fetchurl, url='http://example.com',
                          sha256='...',
                          output=[promise,'file.txt'],
                          foo={'bar':42}, # Additional configuration item
               )

  dref:DRef=instantiate(stage).dref

  mklens(dref).url.val  # Access raw value of 'url'
  mklens(dref).foo             # Return another lens pointing at 'foo'
  mklens(dref).foo.val         # Return raw value of 'foo' (a dict)
  mklens(dref).foo.bar.val     # Return raw value of 'bar'
  mklens(dref).foo.refpath     # Error! dict is not a path

  mklens(dref).output.val      # Return raw output value
  mklens(dref).output.refpath  # Return output as a RefPath (a list)
  mklens(dref).output.syspath  # Error! not a realization

  rref:RRef=realize(instantiate(stage))

  mklens(rref).output.syspath  # Return output as a system path
  ```

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
    o=build_outpaths(b)[build_output_idx]
  if o is None and isinstance(x,Build):
    o=build_outpaths(x)[build_output_idx]
  return Lens((o,ctx),x,[])

