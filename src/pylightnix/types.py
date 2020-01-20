from pylightnix.imports import deepcopy
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

  The format of *derivation reference* is `<HashPart>-<Name>`, where
  - `<HashPart>` contains first 32 characters of derivation `Config`'s sha256
    hash digest.
  - `<Name>` object contains the name of derivation.

  Derivation reference 'points to' derivation object in pylightnix filesystem
  storage. That means, `$PYLIGHTNIX_STORE/<HashPart>-<Name>/` should exist and
  should be a directory containing `config.json` file.

  Derivation reference is normally a result of successful *instantiation*. See
  [instantiate](#pylightnix.core.instantiate).

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
  - `<HashPart0>` is calculated over particular realization of derivation.
  - `<HashPart1>-<Name>` form valid `DRef` which produced this realizaion.

  Realization reference describes realization object in pylightnix filesystem
  storage.  For valid references, `$PYLIGHTNIX_STORE/<HashPart1>-<Name>/<HashPart0>`
  folder does exist and contains `closure.json` file together with
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

  Names are restircted to only contain charaters matching `PYLIGHTNIX_NAMEPAT`.

  See also `mkname` """
  pass

class RefPath(list):
  """ RefPath is an alias for Python list (of strings). The first item of
  `RefPath` should be a valid `DRef`. Other elements should encode a filepath,
  relative to some unspecified realization of this derivation.  """
  pass

class Config:
  """ `Config` is a JSON-serializable dictionary. It takes the place of soucres
  which specifies how should we realize a derivation.

  `Config` should match the requirements of `assert_valid_config`. Typically,
  it's `__dict__` should contain either simple Python types (strings, string
  aliases including [DRefs](#pylightnix.types.DRef), bools, ints, floats), lists
  or dicts. In particular, no tuples, no `np.float32` and no functions are
  allowed.

  Use [mkconfig](#pylightnix.core.mkconfig) to create new Config objects. """
  def __init__(self, d:dict):
    self.__dict__=deepcopy(d)

class ConfigAttrs(dict):
  """ `ConfigAttrs` is a helper object for providing a read-only access to
  [Config](#pylightnix.types.Config) fields as to Python object attributes """
  __getattr__ = dict.__getitem__ # type:ignore


Closure=Dict[DRef,RRef]

#: `Build` objects track the process of [realization](#pylightnix.core.realize).
#: As seen from signature, they store the timeprefix, the Closure, and the output
#: path. Output path contains the path to existing temporary folder into which
#: user should put various *build artifacts*.
#:
#: User may access build-time objects by calling:
#: - [build_config](#pylightnix.core.build_config)
#: - [build_deref](#pylightnix.core.build_deref)
#: - [build_outpath](#pylightnix.core.build_outpath)
Build = NamedTuple('Build', [('config',Config), ('closure',Closure), ('timeprefix',str), ('outpath',Path)])

Instantiator = Callable[[],Config]

Matcher = Callable[[DRef, Closure],Optional[RRef]]

Realizer = Callable[[DRef,Closure],Build]

Derivation = NamedTuple('Derivation', [('dref',DRef), ('matcher',Matcher), ('realizer',Realizer) ])


class Manager:
  def __init__(self):
    self.builders:List[Derivation]=[]

#: Stages are the building blocks of pylightnix. They are defined by stage
#: functions which take [Manager](#pylightnix.typing.Manager) and return
#: [derivation reference](#pylightnix.types.DRef).
#:
#: Stages are subjects to [instantiation](#pylightnix.core.instantiate) and
#: [realization](#pylightnix.core.realize).
#:
#: Examples of built-in stages:
#: * [mknode](#pylightnix.stages.trivial.mknode)
#: * [mkfile](#pylightnix.stages.trivial.mkfile)
#: * [fetchurl](#pylightnix.stages.fetchurl.fetchurl)
Stage = Callable[[Manager],DRef]


