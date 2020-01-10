from typing import (List, Any, Tuple, Union, Optional, Iterable, IO)

class Ref(str):
  pass

class Path(str):
  pass

class Hash(str):
  pass

class RefPath(list):
  pass

# FIXME: Protocol as defined here is not strictly serializable. Default python
# JSON loader will not re-create values of type Hash, but will create strings
# instead
Protocol=List[Tuple[str,Hash,Any]]
