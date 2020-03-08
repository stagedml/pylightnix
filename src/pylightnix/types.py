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

""" All main types which we use in Pylightnix are defined here. """


from pylightnix.imports import ( deepcopy, OrderedDict )
from typing import ( List, Any, Tuple, Union, Optional, Iterable, IO, Callable,
    Dict, NamedTuple, Set, Generator, TypeVar )

class Path(str):
  """ `Path` is an alias for string. It is used in pylightnix to
  tell the typechecker that a given string contains a filesystem path. """
  pass

class Hash(str):
  """ `Hash` is an alias for string. It is used in pylightnix to
  tell the typechecker that a given string contains sha256 hash digest. """
  pass

class HashPart(str):
  """ `HashPart` is an alias for string. It is used in pylightnix to
  tell the typechecker that a given string contains first 32 characters of
  sha256 hash digest. """
  pass

class DRef(str):
  """ `DRef` is an alias for string. It is used in pylightnix to tell the
  typechecker that a given string refers to some derivation.

  The format of *derivation reference* is `<HashPart>-<Name>`, where:
  - `<HashPart>` contains first 32 characters of derivation `RConfig`'s sha256
    hash digest.
  - `<Name>` object contains the name of derivation.

  Derivation reference 'points to' derivation object in pylightnix filesystem
  storage. For a valid DRef, `$PYLIGHTNIX_STORE/<HashPart>-<Name>/` does
  exist and is a directory which contains `config.json` file.

  Derivation references are results of
  [instantiation](#pylightnix.core.instantiate).

  Derivation reference may be converted into a [realization
  reference](#pylightnix.types.RRef) by either dereferencing (that is by
  querying for existing realizations) or by
  [realizing](#pylightnix.core.realize) it from scratch.

  - For derefencing dependencies at the build time, see
    [build_deref](#pylightnix.core.build_deref).
  - For querying the storage, see [store_deref](#pylightnix.core.store_deref).
  """
  pass

class RRef(str):
  """ `RRef` is an alias for string. It is used in pylightnix to tell the
  typechecker that a given string refers to a particular realization of a
  derivation.

  The format of *realization reference* is `<HashPart0>-<HashPart1>-<Name>`,
  where:
  - `<HashPart0>` is calculated over realization's
    [Context](#pylightnix.types.Context) and build artifacts.
  - `<HashPart1>-<Name>` forms valid [DRef](#pylightnix.types.DRef) which
    this realizaion was [realized](#pylightnix.core.realize) from.

  Realization reference describes realization object in pylightnix filesystem
  storage.  For valid references, `$PYLIGHTNIX_STORE/<HashPart1>-<Name>/<HashPart0>`
  folder does exist and contains `context.json` file together with
  stage-specific *build artifacts*

  Realization reference is obtained from the process called
  [realization](#pylightnix.core.realize).

  Valid realization references may be dereferenced down to system paths of
  *build artifacts* by calling
  [rref2path](#pylightnix.core.rref2path). """
  pass

class Name(str):
  """ `Name` is an alias for string. It is used in pylightnix to tell the
  typechecker that a given string contains name of a pylightnix storage object.

  Names are restircted to contain charaters matching `PYLIGHTNIX_NAMEPAT`.

  See also `mkname` """
  pass

#: RefPath is an alias for Python list (of strings). The first item of
#: `RefPath` is a [derivation reference](#pylightnix.types.DRef). Other
#: elements are to represent parts of file path.
#: RefPath is designed to be used in a stage config where they typically refer
#: to artifacts of already existing dependencies. To refer to future artifacts of
#: the derivation being configured, use
#: [PromisePaths](#pylightnix.types.PromisePath).
#:
#: To convert `RefPath` into a [system path](#pylightnix.types.Path), one
#: generally have to perform the following basic actions:
#:
#: 1. Dereference it's first item to obtain the realization. See
#:    [store_deref](#pylightnix.core.store_deref) or
#:    [build_deref](#pylightnix.core.build_deref).
#: 2. Convert the realization reference into system path with
#:    [rref2path](#pylightnix.core.rref2path)
#: 3.  Join the system path with `[1:]` part of RefPath to get the real filename.
#:
#: The algorithm described above is implemented as
#: [build_path](#pylightnix.core.build_path) helper function.
RefPath = List[Any]

#: *Do not change!*
#: A tag to mark the start of [PromisePaths](#pylightnix.types.PromisePath).
PYLIGHTNIX_PROMISE_TAG = "__promise__"

#: *Do not change!*
#: A tag to mark the start of [PromisePaths](#pylightnix.types.PromisePath). In
#: contrast to promises, Pylightnix doesn't check the claims
PYLIGHTNIX_CLAIM_TAG = "__claim__"

#: PromisePath is an alias for Python list of strings. The first item is a
#: special tag (the [promise](#pylightnix.core.promise) or the
#: [claim](#pylightnix.core.claim)) and the subsequent
#: items should represent a file or directory path parts. PromisePaths are
#: typically fields of [Configs](#pylightnix.types.Config). They represent
#: paths to the artifacts which we promise will be created by the derivation
#: being currently configured.
#:
#: PromisePaths do exist only at the time of instantiation. Pylightnix converts
#: them into [RefPath](#pylightnix.types.RefPath) before the realization
#: starts. Converted configs change their type to
#: [RConfig](#pylightnix.type.RConfig)
#:
#: Example:
#: ```python
#: from pylightnix import mkconfig, mkdrv, promise
#: def myconfig()->Config:
#:   name = "config-of-some-stage"
#:   promise_binary = [promise, 'usr','bin','hello']
#:   other_params = 42
#:   return mkconfig(locals())
#: dref=mkdrv(..., config=myconfig(), ...)
#: ```
PromisePath = List[Any]

#: Context type is an alias for Python dict which maps
#: [DRefs](#pylightnix.types.DRef) into one or many
#: [RRefs](#pylightnix.types.RRef).
#:
#: For any derivation, Context stores a mapping from it's dependency's
#: derivations to realizations.
Context=Dict[DRef,List[RRef]]

#: Matcher is a type of user-defined functions which select required
#: realizations from the set of all realizations available.
#:
#: Matchers take the derivation reference and the context. They may easily
#: determine the set of existing realizations (see
#: [store_rrefs](#pylightnix.core.store_rrefs) and should return the subset of
#: this set or None which is a request to Pylightnix to produce more
#: realizations.
#:
#: Matchers should follow the below rules:
#:
#: - Matchers should be **pure**. It's output should depend only on the existing
#:   build artifacts of available realizations.
#: - Matchers should be **satisfiable** by realizers of their stages. If matcher
#:   returns None, the core calls realizer and re-run the matcher only once.
#:
#: Matchers may return an empty list and by that instruct Pylightnix to leave it's
#: derivation without realizations.
#:
#: Pylightnix provides a set of built-in matchers:
#:
#: - [match](#pylightnix.core.match) is a generic matcher with rich sorting and
#:   filtering API.
#: - [match_n](#pylightnix.core.match_n) is it's version for fixed number of matches
#: - [match_best](#pylightnix.core.match_best) decision is made based on a named
#:   build artifact
#: - [match_all](#pylightnix.core.match_all) matches any number of realizations, including zero.
#: - [match_some](#pylightnix.core.match_some) matches any existing realizations
#: - [match_only](#pylightnix.core.match_only) matches exactly one existing
#:   realization (asserts if there are more than one realizations)
Matcher = Callable[[DRef,Context],Optional[List[RRef]]]

InstantiateArg=Dict[str,Any]
RealizeArg=Dict[str,Any]

#: Realizer is a type of callback functions which are defined by the user.
#: Realizers should implement the stage-specific
#: [realization](#pylightnix.core.realize) algorithm.
#:
#: Realizer accepts the following arguments:
#:
#: - [Reference to a Derivation](#pylightnix.types.DRef) being build
#: - [Context](#pylightnix.types.Context) encoding the results of dependency
#:   resolution.
#:
#: `DRef` and `Context` allows programmer to access
#: [Configs](#pylightnix.types.Config) of the current derivation and all it's
#: dependencies.
#:
#: Realizers have to return one or many folder paths of realization artifacts
#: (files and folders containing stage-specific data). Those folders will be
#: added to the pool of Realizations of the current derivation.
#: [Matcher](#pylightnix.types.Matcher) will be called to pick some subset of
#: existing realizations. The chosen subset will eventually appear in the
#: Contexts of downstream derivations.
#:
#: Most of the stages defined in Pylightnix use simplified realizer's API
#: provided by the [Build](#pylightnix.types.Build) helper class. The
#: [build_wrapper](#pylightnix.core.build_wrapper) function converts realizers
#: back to standard format.
#:
#: Example:
#:
#: ```python
#: def mystage(m:Manager)->DRef:
#:   def _realize(dref:DRef, context:Context)->List[Path]:
#:     b=mkbuild(dref, context, buildtime=buildtime)
#:     with open(join(build_outpath(b),'artifact'),'w') as f:
#:       f.write('chickenpoop\n')
#:     return [build_outpath(b)]
#:   ...
#:   return mkdrv(m, ...,  _realize)
#: ```
Realizer = Callable[[DRef,Context,RealizeArg],List[Path]]

#: Derivation is the core type of Pylightnix. It keeps all the information about
#: a stage: it's [configuration](#pylightnix.types.Config), how to
#: [realize](#pylightnix.core.realize) it and how to make a
#: [selection](#pylightnix.types.Matcher) among multiple realizations.
#: Information is stored partly on disk (in the Pylightnix storage), partly in
#: memory in form of Python code.
#:
#: Derivations normally appear as a result of [mkdrv](#pylightnix.core.mkdrv)
#: call.
Derivation = NamedTuple('Derivation', [('dref',DRef), ('matcher',Matcher), ('realizer',Realizer) ])

#: Closure is a named tuple, encoding a reference to derivation, the list of
#: it's dependencies, plus maybe some additional derivations. So the closure is
#: complete set of dependencies but not necessary minimal.
#:
#: Closure is typically obtained as a result of the call to
#: [instantiate](#pylightnix.core.instantiate) and is typically consumed by the
#: call to [realizeMany](#pylightnix.core.realizeMany) or it's analogs.
Closure = NamedTuple('Closure', [('dref',DRef),('derivations',List[Derivation])])

class Config:
  """ Config is a JSON-serializable set of user-defined attributes of Pylightnix
  node. Typically, configs should determine node's realization process.

  Configs should match the requirements of `assert_valid_config`. Typically,
  it's `val` dictionary should contain JSON-serializable types only: strings,
  string aliases such as [DRefs](#pylightnix.types.DRef), bools, ints, floats,
  lists or other dicts. No bytes, `numpy.float32` or lambdas are allowed. Tuples
  are also forbidden because they are not preserved (decoded into lists).

  Some fields of a config have a special meaning for Pylightnix:

  * The field named `name` should be a short readable name. It is used to name
    the Derivation. See `assert_valid_name`.
  * Fields of type [RefPath](#pylightnix.types.RefPath) represent the paths to
    the dependency' artifacts
  * Fields of type [PromisePath](#pylightnix.types.PromisePath) represent
    future paths which are to be produced during the current stage's realization.
  * Values of type [DRef](#pylightnix.types.DRef) encode dependencies.
    Pylightnix scans configs to collect such values and plan the order of
    realizaitons.
  * Values of type [RRef](#pylightnix.types.RRef) lead to warning. Placing such
    values into a config is probably an error: Pylightnix doesn't have a chance to
    know how to produce exactly this reference so it can't produce a continuous
    realization plan.

  Example:
  ```python
  def mystage(m:Manager)->Dref:
    def _config()->Config:
      name = 'mystage'
      nepoches = 4
      learning_rate = 1e-5
      hidden_size = 128
      return mkconfig(locals())
    return mkdrv(_config(),...)
  ```
  """
  def __init__(self, d:dict):
    self.val=deepcopy(d)

  def __repr__(self)->str:
    return 'Config('+self.val.__repr__()+')'


class RConfig(Config):
  """ RConfig is a [Config](#pylightnix.types.Config) where all claims and
  promises are resolved."""
  pass


class ConfigAttrs:
  """ `ConfigAttrs` is a helper object allowing to access
  [RConfig](#pylightnix.types.RConfig) fields as Python object attributes.

  DEPRECATED in favour of [Lenses](#pylightnix.lens.Lens).
  """
  def __init__(self, d:dict):
    for k,v in d.items():
      setattr(self,k,v)



BuildArgs = NamedTuple('BuildArgs', [('dref',DRef),
                                     ('context',Context),
                                     ('timeprefix',Optional[str]),
                                     ('iarg',InstantiateArg),
                                     ('rarg',RealizeArg)])

class Build:
  """Build is a helper object which tracks the process of stage's
  [realization](#pylightnix.core.realize). It allows users to define
  [Realizers](#pylightnix.types.Realizer) with a simple one-argument signature.
  [build_wrapper](#pylightnix.core.build_wrapper) function converts
  Build-realizers into regular ones.

  We encode typical build operations in the following associated functions:

  - [build_config](#pylightnix.core.build_config) - Obtain the RConfig object of
    the current stage
  - [build_cattrs](#pylightnix.core.build_cattrs) - Obtain the ConfigAttrs helper
  - [build_path](#pylightnix.core.build_path) - Convert a RefPath or a PromisePath
    into a system file path
  - [build_outpath](#pylightnix.core.build_outpath) - Create and return the output path.
  - [build_deref](#pylightnix.core.build_deref) - Convert a dependency DRef
    into a realization reference.

  [Lenses](#pylightnix.lens.Lens) accept `Build` objects as a source of
  configuration of derivations being realized.

  Build class may be subclassed by applications in order to define
  application-specific build-state.  Underscoped
  [build_wrapper_](#pylightnix.core.build_wrapper_) accepts additional parameter
  which informs the core what subclass to create. Note that derived classes
  should have the same constructor `def __init__(self, ba:BuildArgs)->None`.

  Example:
  ```python
  class TensorFlowModel(Build):
    model:tf.keras.Model

  def train(m:TensorFlowModel)->None:
    o = build_outpath(m)
    m.model = create_model(...)
    ...
    ...

  def mymodel(m:Manager)->DRef:
    return mkdrv(m, ..., build_wrapper_(TensorFlowModel, train))
  ```
  """

  def __init__(self, ba:BuildArgs)->None:
    self.dref=ba.dref
    self.context=ba.context
    self.iarg=ba.iarg
    self.rarg=ba.rarg
    self.timeprefix=ba.timeprefix
    self.outpaths:List[Path]=[]
    self.cattrs_cache:Optional[ConfigAttrs]=None

class Manager:
  """ The derivation manager is a mutable storage where we store derivations
  before combining them into a [Closure](#pylightnix.types.Closure).

  Manager doesn't have any associated user-level operations. It is typically a
  first argument of stage functions which should be passed downstream without
  modifications.

  The [inplace module](#pylightnix.inplace) defines it's own [global derivation
  manager](#pylightnix.inplace.PYLIGHTNIX_MANAGER) to simplify the usage even
  more.  """
  def __init__(self):
    self.builders:Dict[DRef,Derivation]=OrderedDict()

#: From the user's point of view, Stage is a basic building block of
#: Pylightnix.  It is a function that 'introduces'
#: [derivations](#pylightnix.typing.Derivation) to
#: [Manager](#pylightnix.typing.Manager).  Return value is a [derivation
#: reference](#pylightnix.types.DRef) which is a proof that the derivation was
#: introduced sucessfully.
#:
#: Some built-in stages are:
#: - [mknode](#pylightnix.stages.trivial.mknode)
#: - [mkfile](#pylightnix.stages.trivial.mkfile)
#: - [fetchurl](#pylightnix.stages.fetchurl.fetchurl)
#:
#: Note: Real stages often accept additional custom arguments which AFAIK
#: couldn't be handled by the standard Python typesystem. In extended MyPy the
#: definition would be:
#: ```
#: Stage = Callable[[Manager,VarArg(Any),KwArg(Any)],DRef]
#: ```
#: We use `type:ignore` pragmas when we need to pass `**kwargs`.
Stage = Callable[[Manager],DRef]


Key = Callable[[RRef],Optional[Union[int,float,str]]]


