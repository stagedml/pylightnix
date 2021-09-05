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

from pylightnix.imports import (join,isfile)
from pylightnix.types import (Any, Dict, List, Build, DRef, RRef, Optional,
                              RefPath, Tuple, Union, Path, Context, NamedTuple,
                              Context, Closure, SPath, StorageSettings, Registry)
from pylightnix.utils import (isrefpath, isdref, isrref, tryreadjson )
from pylightnix.core import (rref2dref, rref2path, cfgdict,
                             dref2path, rrefctx, context_deref,
                             context_add, drefcfg)
from pylightnix.build import (build_outpaths, build_config, build_context)


LensContext = NamedTuple('LensContext',[('S',Optional[StorageSettings]),
                                        ('build_path',Optional[Path]),
                                        ('context',Optional[Context]),
                                        ('closure',Optional[Closure])])


def val2dict(v:Any, ctx:LensContext)->Optional[dict]:
  """ Return the `dict` representation of the Lens value, if possible. Getting
  the dictionary allows for creating new lenses """
  S=ctx.S
  if isdref(v):
    return cfgdict(drefcfg(DRef(v), S))
  elif isrref(v):
    return cfgdict(drefcfg(rref2dref(RRef(v)),S))
  elif isrefpath(v):
    j=tryreadjson(val2path(v, ctx))
    assert j is not None, f"RefPath {v} doesn't belong to a valid JSON file"
    assert isinstance(j, dict), f"A file with RefPath {v} doesn't contain valid JSON dict"
    return j
  elif isinstance(v,Build):
    return cfgdict(build_config(v))
  elif isinstance(v,dict):
    return v
  elif isinstance(v,Closure):
    assert len(v.targets)==1, \
      "Lens currently support only single-targeted closures"
    return val2dict(v.targets[0], ctx)
  else:
    return None


def val2rref(v:Any, ctx:LensContext)->RRef:
  S=ctx.S
  if isdref(v):
    dref=DRef(v)
    context=ctx.context
    if context is not None:
      if dref in context:
        rrefs=context_deref(context, dref)
        assert len(rrefs)==1, "Lens doesn't support multirealization dependencies"
        return rrefs[0]
      else:
        assert False, f"Can't convert {dref} into RRef because it is not in context"
    else:
      assert False, f"Lens couldn't resolve '{dref}' without a context"
  elif isinstance(v,Closure):
    assert len(v.targets)==1
    return val2rref(v.targets[0], ctx)
  else:
    assert isrref(v), f"Lens expected RRef, but got '{v}'"
    return RRef(v)

def val2path(v:Any, ctx:LensContext)->Path:
  """ Resolve the current value of Lens into system path. Assert if it is not
  possible or if the result is associated with multiple paths.

  FIXME: re-use val2rref here """
  S:Optional[StorageSettings]=ctx.S
  if isdref(v):
    dref=DRef(v)
    context=ctx.context
    if context is not None:
      if dref in context:
        rrefs=context_deref(context,dref)
        assert len(rrefs)==1, "Lens doesn't support multirealization dependencies"
        return Path(rref2path(rrefs[0],S=S))
    return dref2path(dref,S=S)
  elif isrref(v):
    return rref2path(RRef(v),S=S)
  elif isrefpath(v):
    refpath=list(v) # RefPath is list
    bpath=ctx.build_path
    context=ctx.context
    if context is not None:
      if refpath[0] in context:
        rrefs=context_deref(context,refpath[0])
        assert len(rrefs)==1, "Lens doesn't support multirealization dependencies"
        return Path(join(rref2path(rrefs[0],S), *refpath[1:]))
      else:
        if bpath is not None:
          # FIXME: should we assert on refpath[0]==build.dref ?
          return Path(join(bpath, *refpath[1:]))
        else:
          assert False, f"Can't dereference refpath {refpath}"
    else:
      assert False, f"Lens couldn't resolve '{refpath}' without a context"
  elif isinstance(v, Closure):
    assert len(v.targets)==1
    return val2path(v.targets[0], ctx)
  elif isinstance(v, Build):
    assert ctx.build_path is not None, f"Lens can't access build path of '{v}'"
    return ctx.build_path
  else:
    assert False, f"Lens doesn't know how to resolve '{v}'"

def traverse(l:"Lens", hint:str)->Any:
  val=l.start
  for s in l.steps:
    d=val2dict(val, l.ctx)
    if d is None:
      assert False, f"Lens `{hint}` can't be traversed"
    val=d[s]
  return val

def mutate(l:"Lens", v:Any, hint:str)->None:
  assert len(l.steps)>0, f"Fields to set are not specified"
  val=l.start
  for s in l.steps[:-1]:
    assert isinstance(val,dict), f"Lens {hint} can't be mutated"
    assert s in val, f"Lens `{hint}` can't be mutated"
    val=val[s]
  val[l.steps[-1]]=v

def lens_repr(l, accessor:str)->str:
  return f"mklens(x).{'.'.join(l.steps+[accessor])}"


class Lens:
  """ A Lens is a "syntactic sugar" helper object which could traverse through
  various Python and Pylightnix tree-like structures in a uniform way.

  The list of supported structures include:

  * Python dicts
  * Pylightnix [DRefs](#pylightnix.types.DRef)
  * Pylightnix [RRefs](#pylightnix.types.RRef)
  * Pylightnix [Build](#pylightnix.build.Build) objects
  * Pylightnix [Closures](#pylightnix.types.Closure) objects

  Lens lifecycle typically consists of three stages:
  1. Lens creation with [mklens](#pylightnix.lens.mklens) helper function.
  2. Navigation through the nested fileds using regular Python dot-notation.
     Accessing Lens's attributes results in the creation of new Lens.
  3. Access to the raw value which could no longer be converted into a Lens. In
     this case the raw value is returned. See `val`, `optval`, `rref`, `dref`,
     etc.

  Lenses are not inteded to be created directly, consider using
  [mklens](#pylightnix.lens.mklens) constructor.
  """
  def __init__(self, ctx:LensContext, start:Any, steps:List[str])->None:
    """
    Arguments:
    * `ctx` - is the context in which this Lens is created. The more information
      it contains the more functions are available
    * `start` - Source object which we explore
    * `steps` - List of attributes to query
    """
    self.ctx:LensContext=ctx
    self.start:Any=start
    self.steps:List[str]=steps

  def __getattr__(self, key)->"Lens":
    """ Sugar for `Lens.get` """
    return self.get(key)

  def get(self, key)->"Lens":
    """ Return a new Lens out of the `key` attribute of the current Lens """
    r=lens_repr(self,key)
    d=val2dict(traverse(self, r), self.ctx)
    assert d is not None, f"In `{r}`: can't convert '{key}' into a dict"
    assert key in d, f"In `{r}`: field '{key}' not found"
    return Lens(self.ctx, self.start, self.steps+[key])

  @property
  def optval(self)->Optional[Any]:
    """ Return the value of Lens as-is """
    v=traverse(self, lens_repr(self,'optval'))
    return v

  @property
  def val(self)->Any:
    """ Return the value of Lens as-is, assuming it is not None """
    v=traverse(self, lens_repr(self,'val'))
    assert v is not None
    return v

  @val.setter
  def val(self, v):
    mutate(self,v, lens_repr(self,'val'))

  @property
  def refpath(self)->RefPath:
    """ Check that the current value of Lens is a `RefPath` and return it """
    v=traverse(self, lens_repr(self,'refpath'))
    assert isrefpath(v), f"Lens expected RefPath, but got '{v}'"
    return v

  @property
  def dref(self)->DRef:
    """ Check that the current value of Lens is a `DRef` and return it """
    r=lens_repr(self,'dref')
    v=traverse(self, r)
    if isdref(v):
      return DRef(v)
    elif isrref(v):
      return rref2dref(v)
    else:
      assert False, f"Lens {r} expected a DRef-like object, got '{v}'"

  @property
  def syspath(self)->Path:
    """ Check that the current value of Lens is a `Path` and return it """
    v=traverse(self, lens_repr(self,'syspath'))
    return val2path(v, self.ctx)

  @property
  def contents(self)->str:
    """ Check that the current value of Lens is a `Path` and return it """
    p=self.syspath
    assert isfile(p), f"Can'r read the contents of {p}"
    return open(p,'r').read()

  @property
  def rref(self)->RRef:
    """ Check that the current value of Lens is an `RRef` and return it """
    v=traverse(self, lens_repr(self,'rref'))
    return val2rref(v, self.ctx)

  @property
  def closure(self)->Closure:
    """ Constructs a closure of the DRef which this lens points to.
    FIXME: Filter the closure derivations from unrelated entries.
    """
    r=lens_repr(self,'closure')
    v=traverse(self, r)
    assert isdref(v), f"Lens {r} expected a dref, but got '{v}'"
    assert self.ctx.closure is not None
    return Closure([v], [v], self.ctx.closure.derivations, self.ctx.S)


def mklens(x:Any, o:Optional[Path]=None,
                  b:Optional[Build]=None,
                  rref:Optional[RRef]=None,
                  ctx:Optional[Context]=None,
                  closure:Optional[Closure]=None,
                  build_output_idx:int=0,
                  S:Optional[StorageSettings]=None,
                  r:Optional[Registry]=None)->Lens:
  """ mklens creates [Lens](#pylightnix.lens.Lens) objects from various
  Pylightnix objects.

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

  Example:
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

  rref:RRef=realize1(instantiate(stage))

  mklens(rref).output.syspath  # Return output as a system path
  ```

  """
  if S is None and b is not None:
    S=b.S
  if S is None and isinstance(x,Build):
    S=x.S
  if S is None and r is not None:
    S=r.S
  if ctx is None and b is not None:
    ctx=build_context(b)
  if ctx is None and isinstance(x,Build):
    ctx=build_context(x)
  if ctx is None and rref is not None:
    ctx=rrefctx(rref,S)
  if ctx is None and isrref(x):
    ctx=context_add(rrefctx(RRef(x),S), rref2dref(RRef(x)), [RRef(x)])
  if o is None and b is not None:
    o=build_outpaths(b)[build_output_idx]
  if o is None and isinstance(x,Build):
    o=build_outpaths(x)[build_output_idx]
  if closure is None and isinstance(x,Closure):
    closure=x
  return Lens(LensContext(S,o,ctx,closure),x,[])

