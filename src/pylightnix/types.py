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

  Derivation references 'point to' derivation objects in pylightnix filesystem
  storage. That means, `$PYLIGHTNIX_STORE/<HashPart>-<Name>/` should exist and
  should be a directory containing `config.json` file. """
  pass

class RRef(str):
  """ `RRef` is an alias for string. It is used in pylightnix to tell the
  typechecker that a given string refers to a particular realization of a
  derivation.

  The format of *realization reference* is `<HashPart0>-<HashPart1>-<Name>`,
  where:
  - `<HashPart0>` is calculated over particular realization of derivation.
  - `<HashPart1>-<Name>` form valid `DRef` which produced this realizaion.

  Realization references describe realization objects in pylightnix filesystem
  storage.  That means, `$PYLIGHTNIX_STORE/<HashPart1>-<Name>/<HashPart0>`
  should exist and should be a directory containing `closure.json` file and
  various *build artifacts* """
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

  `Config` should match the requirements of `assert_valid_config`. Tupically,
  it's __dict__ should contain either simple Python types (strings, bool, ints,
  floats), lists or dicts. In particular, no tuples, no `np.float32` and no
  functions are allowed. """
  def __init__(self, d:dict):
    self.__dict__=deepcopy(d)

class ConfigAttrs(dict):
  """ `ConfigAttrs` is a helper object for read-only access of dict fields as
  attributes """
  __getattr__ = dict.__getitem__ # type:ignore


Closure=Dict[DRef,RRef]

#: `Build` object is used to track the process of realization.
Build = NamedTuple('Build', [('config',Config), ('closure',Closure), ('timeprefix',str), ('outpath',Path)])

Instantiator = Callable[[],Config]

Matcher = Callable[[DRef, Closure],Optional[RRef]]

Realizer = Callable[[DRef,Closure],Build]

Derivation = NamedTuple('Derivation', [('dref',DRef), ('matcher',Matcher), ('realizer',Realizer) ])


class Manager:
  def __init__(self):
    self.builders:List[Derivation]=[]

Stage = Callable[[Manager],DRef]

