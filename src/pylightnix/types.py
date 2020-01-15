from typing import (List, Any, Tuple, Union, Optional, Iterable, IO)

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

Ref = Union[DRef,IRef]

class RefPath(list):
  """ RefPath is a path referencing some file in some instance. It is
  represented by a list of strings, where the first string is `RRef` """
  pass

# FIXME: Protocol as defined here is not strictly serializable. Default python
# JSON loader will not re-create values of type Hash, but will create strings
# instead
Protocol=List[Tuple[str,Hash,Any]]
