from pylightnix.imports import deepcopy
from typing import ( List, Any, Tuple, Union, Optional, Iterable, IO, Callable,
    Dict, NamedTuple, Set )

class Path(str):
  pass

class Hash(str):
  pass

class HashPart(str):
  pass

class DRef(str):
  """ Derivation Reference is a string containing a name of Derivation """
  pass

class RRef(str):
  """ Realization reference is a string containing a name of Derivation Instance """
  pass

class Name(str):
  """ A stage's name is what you see in the last part of the reference """
  pass

class RefPath(list):
  """ RefPath is a path referencing some file in some instance. It is
  represented by a list of strings, where the first string is `RRef` """
  pass

class Config:
  """ Config is a JSON-serializable configuration object. It should match the
  requirements of `assert_valid_config`. Tupically, it's __dict__ should
  contain only either simple Python types (strings, bool, ints, floats), lists
  or dicts. No tuples, no `np.float32`, no functions. Fields with names
  starting from '_' are may be added after construction, but they are not
  preserved during the serialization."""
  def __init__(self, d:dict):
    self.__dict__=deepcopy(d)

class ConfigAttrs(dict):
  """ Helper object allowing to access dict fields as attributes """
  __getattr__ = dict.__getitem__ # type:ignore


Closure=Dict[DRef,RRef]


Build = NamedTuple('Build', [('config',Config),
                             ('closure',Closure),
                             ('timeprefix',str),
                             ('outpath',Path)])

Instantiator = Callable[[],Config]

Matcher = Callable[[DRef, Closure],Optional[RRef]]

Realizer = Callable[[DRef,Closure],Build]

Derivation = NamedTuple('Derivation', [('dref',DRef),
                                       ('matcher',Matcher),
                                       ('realizer',Realizer) ])


class Manager:
  def __init__(self):
    self.builders:List[Derivation]=[]

Stage = Callable[[Manager],DRef]

