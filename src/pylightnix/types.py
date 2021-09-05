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

from typing import (List, Any, Tuple, Union, Optional, Iterable, IO, Callable,
                    Dict, NamedTuple, Set, Generator, TypeVar, NewType,
                    SupportsAbs, Generic, Iterator)

class Path(str):
  """ `Path` is an alias for string. It is used in pylightnix to
  tell the typechecker that a given string contains a filesystem path. """
  pass

class SPath(Path):
  """ `SPath` is an alias for string. It is used in pylightnix to
  tell the typechecker that a given string contains a path to storage. """
  pass

#: Stoarge settings contains a path for the main stoarge and a path for
#: temporary directories. These paths need to be on the same device in order to
#: atomic rename work.
StorageSettings=NamedTuple('StorageSettings',[('root',Optional[Path]),
                                              ('storage',Optional[Path]),
                                              ('tmpdir',Optional[Path])])

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
  """ `DRef` stands for *derivation reference*. It is a string identifier of a
  filesystem part of [Derivation](#pylightnix.types.Derivation) object.

  The format of derivation reference is `<HashPart>-<Name>`, where:
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
  [realizing](#pylightnix.core.realize1) it from scratch.

  - For derefencing dependencies at the build time, see
    [build_deref](#pylightnix.core.build_deref).
  - For querying the storage, see [store_deref](#pylightnix.core.store_deref).
  """
  pass

class RRef(str):
  """ `RRef` stands for *realization reference*. It identifies the collection of
  artifacts of a [Stage](#pylightnix.types.Stage).

  The format of realization reference is `<HashPart0>-<HashPart1>-<Name>`,
  where:
  - `<HashPart0>` is calculated over realization's
    [Context](#pylightnix.types.Context) and build artifacts.
  - `<HashPart1>-<Name>` forms valid [DRef](#pylightnix.types.DRef) which
    this realizaion was [realized](#pylightnix.core.realize1) from.

  Realization reference is obtained from the process called
  [realization](#pylightnix.core.realize1).

  Valid realization references may be dereferenced down to system paths of
  *build artifacts* by calling [rref2path](#pylightnix.core.rref2path) or by
  using [lenses](#pyligntix.lens.Lens). """
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
#:    [rref2path](#pylightnix.core.store_rref2path)
#: 3.  Join the system path with `[1:]` part of RefPath to get the real filename.
#:
#: The algorithm described above is implemented as
#: [build_path](#pylightnix.core.build_path) helper function.
RefPath = List[Union[DRef,str]]

class PylightnixException(Exception):
  """ Base class of Pylightnix exceptions"""
  pass

class PromiseException(PylightnixException):
  def __init__(self, dref:DRef, failed:List[Tuple[Path,RefPath]]):
    super(PromiseException, self).__init__(
      f"The realizer of '{dref}' has failed to produce an artifact "
      f"to be referenced as {['/'.join(f[1][1:]) for f in failed]}")
    self.dref=dref
    self.failed=failed

#: Type variable intended to be either a `Path` or `RRef`
_REF=TypeVar('_REF')

class Output(Generic[_REF]):
  """ Output is a base class for 'organized collections of realizations', either
  in form of temporary Paths or RRefs.

  TODO: Rename into something which has a meaning of `PromisedOuput` """
  def __init__(self,val:Iterable[_REF]):
    self.val:List[_REF]=list(val)


#: Context type is an alias for Python dict which maps
#: [DRefs](#pylightnix.types.DRef) into one or many
#: [RRefs](#pylightnix.types.RRef).
#:
#: For any derivation, the Context stores a mapping from it's dependency's
#: derivations to realizations.
Context=Dict[DRef,List[RRef]]

#: Type of user-defined arguments to pass to the Config
InstantiateArg=Dict[str,Any]

#: Type of user-defined arguments to pass to the Realizer
RealizeArg=Dict[str,Any]

#: Matchers are user-defined Python functions with fixed signature. They serve
#: two purposes:
#: 1. Decide whether to launch a new realization or re-use existing
#:    realizations.
#: 2. Filter a matched subset of a realization groups out of the set of
#:    available realizations.
#:
#: Matchers answer 'yes' to the first question by returning None. Non-none value
#: specifies the matched set of groups.
#:
#: Matcher invariants are:
#:
#: - Matcher outputs should only depend on the immutable realizations passed to
#:   them as inputs. Matchers should avoid having side-effects.
#: - Matchers must be satisfiable. If the matcher returns None, the core
#:   re-runs runs the realization and calls the matcher once again. Returning
#:   None again would be an error.
#:
#: Pylightnix includes a set of built-in matchers:
#:
#: - [match_latest](#pylightnix.core.match_latest) prefers the latest
#: realizations
#: - [match_all](#pylightnix.core.match_all) takes everything
#: - [match_some](#pylightnix.core.match_some) takes not less than N realizations
#: - [match_only](#pylightnix.core.match_only) expects exactly one realization
Matcher = Callable[[Optional[StorageSettings],List[RRef]],
                   Optional[List[RRef]]]
MatcherO = Callable[[Optional[StorageSettings],Output[RRef]],
                    Optional[Output[RRef]]]
# TODO: Splitting Matcher into two parts would allow us to rid of
# `force_interrupt` argument.


#: Realizers are user-defined Python functions. Realizers typically
#: implement [application-specific algorithms](#pylightnix.core.realize1) which
#: take some configuration parameters and produce some artifacts.
#:
#: Realizer accepts the following arguments:
#:
#: - Path to a global Pylightnix storage
#: - A [Derivation reference](#pylightnix.types.DRef) being built
#: - A [Context](#pylightnix.types.Context) encoding the results of dependency
#:   resolution.
#: - Set of additional user-defined arguments
#:
#: Context is the key to accessing the dependency artifacts.
#:
#: Derivation reference is required to access [configuration
#: parameters](#pylightnix.types.Config) of the algorithm.
#:
#: Realizers must return one or many folders of realization artifacts (files and
#: folders containing application-specific data). Every folder is treated as an
#: alternative realization.  [Matcher](#pylightnix.types.Matcher) is later used
#: to pick the subset of realizations which matches some application-specific
#: criteria.  This subset will eventually appear as the `Context`s of downstream
#: realizaions.
#:
#: Pylightnix stages may use the simplified realizer API
#: provided by the [Build](#pylightnix.types.Build) helper class.
#:
#: Example:
#:
#: ```python
#: def mystage(r:Registry)->DRef:
#:   def _realize(dref:DRef, context:Context)->List[Path]:
#:     b=mkbuild(dref, context, buildtime=buildtime)
#:     with open(join(build_outpath(b),'artifact'),'w') as f:
#:       f.write('chickenpoop\n')
#:     return [build_outpath(b)]
#:   ...
#:   return mkdrv(r, ...,  _realize)
#: ```
Realizer = Callable[[Optional[StorageSettings],DRef,Context,RealizeArg],List[Path]]
RealizerO = Callable[[Optional[StorageSettings],DRef,Context,RealizeArg],Output[Path]]

#: Derivation is a core Pylightnix entity. It holds the information required to
#: produce artifacts of individual [Stage](#pylightnix.types.stage).
#:
#: Fields include:
#: * [Configuration](#pylightnix.types.Config) objects serialized on disk.
#: * [Matcher](#pylightnix.types.Matcher) Python function
#: * [Realizer](#pylightnix.core.realize1) Python function
#:
#: The actual configuration is stored in the Pylightnix filesystem storage.
#: Derivation holds the [DRef](#pylightnix.types.DRef) access key.
#:
#: Derivations normally appear as a result of [mkdrv](#pylightnix.core.mkdrv)
#: calls.
Derivation = NamedTuple('Derivation', [('dref',DRef),
                                       ('matcher',Matcher),
                                       ('realizer',Realizer)])
# TODO: Think about storing Stage function here as well. This would allow us to
# organize catamorphism-like mappers.

#: Closure describes the realization plan of some
#: [Derivation](#pylightnix.types.Derivation).
#:
#: The plan is represented by a sequence of
#: [Derivations](#pylightnix.types.Derivation) one need to realize1 in order to
#: realize1 a given target derivation.
#:
#: Closures are typically obtained as a result of the
#: [instantiate](#pylightnix.core.instantiate) and is typically consumed by the
#: call to [realize1](#pylightnix.core.realize1) or it's analogs.
Closure = NamedTuple('Closure', [('result',Any),
                                 ('targets',List[DRef]),
                                 ('derivations',List[Derivation]),
                                 ('S',Optional[StorageSettings])])

class Config:
  """ Config is a JSON-serializable dict-like object containing user-defined
  attributes. Together with [Realizers](#pylightnix.types.Realizer) and
  [Matchers](#pylightnix.types.Matcher), configs describe
  [Stage](#pylightnix.types.Stage) objects.

  Configs carry Python dictionaries that should contain JSON-serializable types.
  Strings, bools, ints, floats, lists or other dicts are fine, but no bytes,
  `numpy.float32` or lambdas are allowed. Tuples are also forbidden because they
  are not preserved (decoded into lists). Special emphasis is placed on
  [DRef](#pylightnix.types.DRef) support which link dependent stages together.

  Config of a derivation can't include the Derivation reference to itself,
  because it contains the config hash as its part.

  Some field names of a config have a special meaning for Pylightnix:

  * String `name` field will be used as a part of references to
    a derivation associated with this config.
  * [RefPaths](#pylightnix.types.RefPath) represent paths to
    artifacts within the stage artifact folders.
  * [SelfRef](#pylightnix.core.selfref) paths represent output paths to be
    produced during the stage's realization.
  * [DRef](#pylightnix.types.DRef) represent stage dependencies.  Pylightnix
    collects derivation references and plan the realization order based on them.

  Storing an [RRef](#pylightnix.types.RRef) in the config leads to a warning.
  Pylightnix does not necessarily knows how to produce the exact reference, so
  the end result may not match the expectations.

  Configs are normally created from Python dicts by the
  [mkconfig](#pylightnix.core.mkconfig) function.

  Example:
  ```python
  def mystage(r:Registry)->Dref:
    def _config()->dict:
      name = 'mystage'
      nepoches = 4
      learning_rate = 1e-5
      hidden_size = 128
      return locals()
    return mkdrv(mkconfig(_config()),...)
  ```
  """
  def __init__(self, d:dict):
    self.val=deepcopy(d)

  def __repr__(self)->str:
    return 'Config('+self.val.__repr__()+')'


class RConfig(Config):
  """ `RConfig` is a [Config](#pylightnix.types.Config) where all
  [Self-referenes](#pylightnix.types.PYLIGHTNIX_SELF_TAG) are resolved. RConfig
  stands for 'Resolved Config'.  """
  pass


class ConfigAttrs:
  """ `ConfigAttrs` is a helper object allowing to access
  [RConfig](#pylightnix.types.RConfig) fields as Python object attributes.

  DEPRECATED in favour of [Lenses](#pylightnix.lens.Lens).
  """
  def __init__(self, d:dict):
    for k,v in d.items():
      setattr(self,k,v)



BuildArgs = NamedTuple('BuildArgs', [('S',Optional[StorageSettings]),
                                     ('dref',DRef),
                                     ('context',Context),
                                     ('starttime',Optional[str]),
                                     ('stoptime',Optional[str]),
                                     ('iarg',InstantiateArg),
                                     ('rarg',RealizeArg)])

class Build:
  """Build objects track the process of stage's
  [realization](#pylightnix.core.realize1). Build allows users to define
  [Realizers](#pylightnix.types.Realizer) with only a simple one-argument
  signature. The [build_wrapper](#pylightnix.core.build_wrapper) function
  converts simplified Build-realizers into the regular ones.

  Typical Build operations include:

  - [build_config](#pylightnix.core.build_config) - Obtain the RConfig object of
    the current stage
  - [build_cattrs](#pylightnix.core.build_cattrs) - Obtain the ConfigAttrs
    helper
  - [build_path](#pylightnix.core.build_path) - Convert a RefPath or a
    self-ref path
    into a system file path
  - [build_setoutgroups](#pylightnix.build.build_setoutgroups) - Initialize and
    return groups of output folders
  - [build_deref](#pylightnix.core.build_deref) - Convert a dependency DRef
    into a realization reference.

  [Lenses](#pylightnix.lens.Lens) accept `Build` objects as a configuration
  source for derivations being realized.

  Build class may be subclassed by applications in order to define
  application-specific build-state.  Underscoped
  [build_wrapper_](#pylightnix.core.build_wrapper_) accepts additional callback
  parameter which informs the core what subclass to create. Note that derived
  classes should have the same constructor `def __init__(self,
  ba:BuildArgs)->None`.

  Example:
  ```python
  class TensorFlowModel(Build):
    model:tf.keras.Model

  def train(r:TensorFlowModel)->None:
    o = build_outpath(r)
    r.model = create_model(...)
    ...

  def mymodel(r:Registry)->DRef:
    return mkdrv(r, ..., build_wrapper_(TensorFlowModel, train))
  ```
  """

  def __init__(self, ba:BuildArgs)->None:
    self.S=ba.S
    self.dref=ba.dref
    self.context=ba.context
    self.iarg=ba.iarg
    self.rarg=ba.rarg
    self.starttime=ba.starttime
    self.stoptime=ba.stoptime
    self.outpaths:Optional[Output[Path]]=None
    self.cattrs_cache:Optional[ConfigAttrs]=None


class Registry:
  """ The derivation registry is a mutable storage object where Pylightnix
  stores derivations before combining them into a
  [Closure](#pylightnix.types.Closure).

  Registry doesn't requre any special operations besides creating and passing
  around. By convention, Registry objects are first arguments of user-defined
  stage functions and the `mkdrv` API function of Pylightnix.
  """
  def __init__(self, S:Optional[StorageSettings]=None):
    self.builders:Dict[DRef,Derivation]=OrderedDict()
    self.S:Optional[StorageSettings]=S
    self.in_instantiate:bool=False


#: DRefLike is a type variable holding DRefs or any of its derivatives
DRefLike = TypeVar('DRefLike',bound=DRef)

StageResult=Union[DRef,List[DRef],Dict[Any,DRef],Tuple[DRef,...]]

#: Functions with the `Stage` signature are the top-level building blocks of
#: Pylightnix. Stage functions call [mkdrv](#pylightnix.core.mkdrv) and each
#: other to produce linked [Derivations](#pylightnix.types.Derivation) and
#: register them in the [Registry](#pylightnix.types.Registry).
#:
#: Some built-in stages are:
#: - [mknode](#pylightnix.stages.trivial.mknode)
#: - [mkfile](#pylightnix.stages.trivial.mkfile)
#: - [fetchurl](#pylightnix.stages.fetchurl.fetchurl)
#:
#: Note: Real stages often accept additional custom arguments which AFAIK
#: couldn't be handled by the simple MyPy. In a somewhat extended MyPy the Stage
#: definition would look like:
#:
#: ```Python
#: Stage = Callable[[Registry,VarArg(Any),KwArg(Any)],DRef]
#: ```
#:
#: Stage's return value is a [derivation reference](#pylightnix.types.DRef)
#: which could be either used in other stages, or
#: [instantiated](#pylightnix.core.instantiate) into the stage realization plan.
Stage=Callable[...,StageResult]


