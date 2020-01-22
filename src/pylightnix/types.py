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
  storage. For any valid DRef, `$PYLIGHTNIX_STORE/<HashPart>-<Name>/` does
  exist and is a directory which contains `config.json` file.

  Derivation reference is normally a result of successful
  [instantiation](#pylightnix.core.instantiate).

  Derivation reference may be converted to a realization reference, by call
  either of:
  - [build_deref](#pylightnix.core.build_deref) at build time.
  - [store_deref](#pylightnix.core.store_deref) to get the existing realization.
  - [realize](#pylightnix.core.realize) to get new realization
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
  [store_rref2path](#pylightnix.core.store_rref2path). """
  pass

class Name(str):
  """ `Name` is an alias for string. It is used in pylightnix to tell the
  typechecker that a given string contains name of a pylightnix storage object.

  Names are restircted to contain charaters matching `PYLIGHTNIX_NAMEPAT`.

  See also `mkname` """
  pass

class RefPath(list):
  """ RefPath is an alias for Python list (of strings). The first item of
  `RefPath` is a [derivation reference](#pylightnix.types.DRef). Other elements
  represent path (names of folders and optionally a filename). The path is
  relative to unspecified realization of this derivation.

  To convert `RefPath` into [system path](#pylightnix.types.Path), one generally
  have to perform the following elementary actions:
  1. Get the reference to realization of current derivation, see
     [store_deref](#pylightnix.core.store_deref) or
     [build_deref](#pylightnix.core.build_deref).
  2. Convert the realization reference into system path with
     [store_rref2path](#pylightnix.core.store_rref2path)
  3. Join the system path with 'relative' part of RRefPath

  The above algorithm is implemented as
  [build_deref_path](#pylightnix.core.build_deref_path) helper function
  """
  pass

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
#: For any node grouped with it's dependencies, pylightnix forces a property of
#: unique realization, which means that no two nodes of a group which depend on
#: same derivation may resolve it to different realizations.
Context=Dict[DRef,RRef]

#: `Build` objects tracks the process of [realization](#pylightnix.core.realize).
#: As may be seen from it's signature, it stores timeprefix, the Context, and the output
#: path. Output path contains the path to existing temporary folder for placing *build artifacts*.
#:
#: Users may access fields of a `Build` object by calling:
#: - [build_config](#pylightnix.core.build_config)
#: - [build_deref](#pylightnix.core.build_deref)
#: - [build_outpath](#pylightnix.core.build_outpath)
Build = NamedTuple('Build', [('dref',DRef), ('context',Context), ('timeprefix',str), ('outpath',Path)])

Instantiator = Callable[[],Config]

Matcher = Callable[[DRef, Context],Optional[RRef]]

Realizer = Callable[[DRef,Context],Path]

Derivation = NamedTuple('Derivation', [('dref',DRef), ('matcher',Matcher), ('realizer',Realizer) ])

Closure = NamedTuple('Closure', [('dref',DRef),('derivations',List[Derivation])])

class Manager:
  def __init__(self):
    self.builders:Dict[DRef,Derivation]=OrderedDict()

#: Stages are the building blocks of pylightnix. They are defined by stage
#: functions which take [Manager](#pylightnix.typing.Manager) and return
#: [derivation reference](#pylightnix.types.DRef).
#:
#: Stages are subjects to [instantiation](#pylightnix.core.instantiate) and
#: [realization](#pylightnix.core.realize).
#:
#: Examples of built-in stages:
#: - [mknode](#pylightnix.stages.trivial.mknode)
#: - [mkfile](#pylightnix.stages.trivial.mkfile)
#: - [fetchurl](#pylightnix.stages.fetchurl.fetchurl)
Stage = Callable[[Manager],DRef]


