from pylightnix.imports import ( deepcopy, OrderedDict )
from typing import ( List, Any, Tuple, Union, Optional, Iterable, IO, Callable,
    Dict, NamedTuple, Set )

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
  reference](#pylightnix.types.RRef) by either dereferencing (that is querying
  for existing realizations) or [realizing](#pylightnix.core.realize) it from
  scratch.

  For derefencing, one can use [build_deref](#pylightnix.core.build_deref) at
  build time or [store_deref](#pylightnix.core.store_deref) otherwise.
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
#: `RefPath` is a [derivation reference](#pylightnix.types.DRef). Other elements
#: represent path (names of folders and optionally a filename). The path is
#: relative to unspecified realization of this derivation.
#:
#: To convert `RefPath` into [system path](#pylightnix.types.Path), one generally
#: have to perform the following elementary actions:
#: 1. Get the reference to realization of current derivation, see
#:    [store_deref](#pylightnix.core.store_deref) or
#:    [build_deref](#pylightnix.core.build_deref).
#: 2. Convert the realization reference into system path with
#:    [rref2path](#pylightnix.core.rref2path)
#: 3. Join the system path with 'relative' part of RRefPath
#:
#: The above algorithm is implemented as
#: [build_deref_path](#pylightnix.core.build_deref_path) helper function
RefPath = List[Any]

class Config:
  """ `Config` is a JSON-serializable dictionary. Configs are required by
  definintion of Stages and should determine the realization process.

  `Config` should match the requirements of `assert_valid_config`. Typically,
  it's `__dict__` should contain JSON-serializable types only: strings, string
  aliases such as [DRefs](#pylightnix.types.DRef), bools, ints, floats, lists or
  other dicts. No bytes, `numpy.float32` or lambdas are allowed. Tuples are also
  forbidden because they are not preserved (decoded into lists).

  Use [mkconfig](#pylightnix.core.mkconfig) to create Configs from dicts. """
  def __init__(self, d:dict):
    self.__dict__=deepcopy(d)

class ConfigAttrs(dict):
  """ `ConfigAttrs` is a helper object for providing a read-only access to
  [Config](#pylightnix.types.Config) fields as to Python object attributes """
  __getattr__ = dict.__getitem__ # type:ignore


#: Context type is an alias for Python dict which maps
#: [DRefs](#pylightnix.types.DRef) into [RRefs](#pylightnix.types.RRef).
#:
#: For any derivation, Context stores a mapping from it's dependencie's
#: derivations to their realizations. In contrast to
#: [Closure](#pylightnix.types.Closure) type, Context contains a minimal closure
#: of derivation's dependencies.
Context=Dict[DRef,RRef]

class Build:
  """Build is a helper object which tracks the process of [realization](#pylightnix.core.realize).

  Useful associated functions are:
  - [build_wrapper](#pylightnix.core.build_wrapper)
  - [build_config](#pylightnix.core.build_config)
  - [build_deref](#pylightnix.core.build_deref)
  - [build_outpath](#pylightnix.core.build_outpath) """
  def __init__(self, dref:DRef, context:Context, timeprefix:str, outpath:Path)->None:
    self.dref=dref
    self.context=context
    self.timeprefix=timeprefix
    self.outpath=outpath

Instantiator = Callable[[],Config]

#: FIXME: Make matchers more algebra-friendly. E.g. one could make them return
#: RRef ranks which could be composed and re-used.
Matcher = Callable[[DRef,Context],Optional[RRef]]

#: Realizer is a user-defined function which defines how to
#: [build](#pylightnix.core.realize) a given derivation in a given
#: [context](#pylightnix.types.Context).
#:
#: For given derivation being built, it's Realizer may access the following
#: objects via [Build helpers](#pylightnix.types.Build):
#: - Configuration of the derivation and configurations of all it's
#:   dependencies. See [build_config](#pylightnix.core.build_config).
#: - Realizations of all the dependencies (and thus, their build artifacts).
#:   See [build_path](#pylightnix.core.build_path).
Realizer = Callable[[DRef,Context],Path]

#: Derivation is a core type of Pylightnix. It keeps all the information about
#: a stage: it's [configuration](#pylightnix.types.Config), how to
#: [realize](#pylightnix.core.realize) it and how to make a selection among
#: multiple realizations. Information is stored partly on disk (in the
#: storage), partly in memory in form of a Python code.
Derivation = NamedTuple('Derivation', [('dref',DRef), ('matcher',Matcher), ('realizer',Realizer) ])

#: Closure is a named tuple, encoding a reference to derivation and a whole list
#: of it's dependencies, plus maybe some additional derivations. So the closure
#: is complete but not necessary minimal.
Closure = NamedTuple('Closure', [('dref',DRef),('derivations',List[Derivation])])

class Manager:
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


