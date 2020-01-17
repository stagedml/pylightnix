from pylightnix.types import ( Callable, List, Enum )
from pylightnix import Ref

class InstantiateMode(Enum):
  FORCE_SEARCH=0
  FORCE_BUILD=1
  SEARCH_OR_REBUILD=2

class Options:
  def __init__(self, mode:InstantiateMode=InstantiateMode.SEARCH_OR_REBUILD)->None:
    self.mode=mode


def instantiate(o:Options,
                fsearch:Callable[[],List[Ref]],
                fbuild:Callable[[],Ref]) -> Ref:
  """ Instantiate helper and a poor man's Maybe monad """

  def _report_search_failure():
    assert False, "Search didn't find anything"

  def _do_search(notfound_handler)->Ref:
    refs = fsearch()
    if len(refs)>0:
      if len(refs)==1:
        return refs[0]
      else:
        assert False, f"Multiple search results ({refs}), Consider checking search criteria."
    else:
      return notfound_handler()

  if o.mode==InstantiateMode.FORCE_SEARCH:
    return _do_search(_report_search_failure)
  elif o.mode==InstantiateMode.FORCE_BUILD:
    return fbuild()
  elif o.mode==InstantiateMode.SEARCH_OR_REBUILD:
    return _do_search(fbuild)
  else:
    assert False, f"Invalid instantiate mode {o.mode}"

