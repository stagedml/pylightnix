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

""" Main types used in Pylightnix are defined here. """


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
  - `<HashPart>` contains first 32 characters of derivation `Config`'s sha256
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

#: PromisePath is an alias for Python list of strings. The first item is a
#: special tag (the [promise](#pylightnix.core.promise)) and the subsequent
#: items should represent a file or directory path parts. PromisePaths are to
#: be used in [Configs](#pylightnix.types.Config). They typically represent
#: paths to the artifacts which we promise will be created by the derivation
#: being currently configured.
#:
#: PromisePaths do exist only at the time of instantiation. Pylightnix converts
#: them into [RefPath](#pylightnix.types.RefPath) before the realization
#: starts.
PromisePath = List[Any]

#: Context type is an alias for Python dict which maps
#: [DRefs](#pylightnix.types.DRef) into one or many
#: [RRefs](#pylightnix.types.RRef).
#:
#: For any derivation, Context stores a mapping from it's dependency's
#: derivations to realizations.
Context=Dict[DRef,List[RRef]]

#: Matcher is a type of user-defined functions which select required
#: realizations from the set of all available. Matchers also may ask the caller
#: to build new realizations by returning None.
#:
#: There are certain rules for matchers:
#:
#: - Matchers should be **pure**. It's output should depend only on the existing
#:   build artifacts of available realizations.
#: - Matchers should be **satisfiable** by the their realizaitons. If
#:   matcher returns None, the core calls realizer and re-run the matcher only
#:   once.
#:
#: Matchers may return an empty list instructs Pylightnix to leave it's
#: derivation without realizations.
Matcher = Callable[[DRef,Context],Optional[List[RRef]]]

#: Realizer is a type of user-defined functions implementing the
#: [realization](#pylightnix.core.realize) of derivation in a given
#: [context](#pylightnix.types.Context).
#:
#: Realizer accepts the following arguments:
#: - Derivation reference to build the realizations of
#: - A Context encoding the result of dependency resolution.
#:
#: Realizer should return one or many system paths of output folders containing
#: realization artifacts. Those folders will be destroyed (moved) by the core at
#: the final stage of realization. [Build](#pylightnix.types.Build) helper
#: objects may be used for simplified output path management and dependency
#: access.
Realizer = Callable[[DRef,Context],List[Path]]

#: Derivation is the core type of Pylightnix. It keeps all the information about
#: a stage: it's [configuration](#pylightnix.types.Config), how to
#: [realize](#pylightnix.core.realize) it and how to make a selection among
#: multiple realizations. Information is stored partly on disk (in the
#: storage), partly in memory in form of Python code.
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

  `Config` should match the requirements of `assert_valid_config`. Typically,
  it's `__dict__` should contain JSON-serializable types only: strings, string
  aliases such as [DRefs](#pylightnix.types.DRef), bools, ints, floats, lists or
  other dicts. No bytes, `numpy.float32` or lambdas are allowed. Tuples are also
  forbidden because they are not preserved (decoded into lists).

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
    values into a config is probably an error: Pylightnix can't know how to
    produce exactly this reference and so it can't produce a continuous
    realization plan.

  Example:
  ```python
  def mystage(m:Manager)->Dref:
    def _config():
      name = 'mystage'
      nepoches = 4
      learning_rate = 1e-5
      hidden_size = 128
      return mkconfig(locals())
    return mkdrv(_config(),...)
  ```
  """
  def __init__(self, d:dict):
    self.__dict__=deepcopy(d)

  def __repr__(self)->str:
    return self.__dict__.__repr__()

class ConfigAttrs:
  """ `ConfigAttrs` is a helper object allowing to access
  [Config](#pylightnix.types.Config) fields as Python object attributes """
  def __init__(self, d:dict):
    for k,v in d.items():
      setattr(self,k,v)

BuildArgs = NamedTuple('BuildArgs', [('dref',DRef), ('cattrs',ConfigAttrs),
                                     ('context',Context), ('timeprefix',str),
                                     ('buildtime',bool)])

class Build:
  """Build is a helper object which tracks the process of stage's
  [realization](#pylightnix.core.realize).

  We encode typical build operations in the following associated functions:

  - [build_config](#pylightnix.core.build_config) - Obtain the Config object of
    the current stage
  - [build_cattrs](#pylightnix.core.build_cattrs) - Obtain the ConfigAttrs helper
  - [build_path](#pylightnix.core.build_path) - Convert a RefPath or a PromisePath
    into a system file path
  - [build_outpath](#pylightnix.core.build_outpath) - Create and return the output path.
  - [build_deref](#pylightnix.core.build_deref) - Convert a dependency DRef
    into a realization reference.
  """

  def __init__(self, ba:BuildArgs)->None:
    self.dref=ba.dref
    self.cattrs=ba.cattrs
    self.context=ba.context
    self.timeprefix=ba.timeprefix
    self.buildtime=ba.buildtime
    self.outpaths:List[Path]=[]

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
#: Some built-in stages are: - [mknode](#pylightnix.stages.trivial.mknode) -
#: [mkfile](#pylightnix.stages.trivial.mkfile) -
#: [fetchurl](#pylightnix.stages.fetchurl.fetchurl)
Stage = Callable[[Manager],DRef]


Key = Callable[[RRef],Optional[Union[int,float,str]]]


