from pylightnix.imports import (chain, join, isfile, isdir, islink)

from pylightnix.types import (Any, DRef, RRef, Dict, List, Union, RealizeArg,
                              Realizer, Closure, Iterable, Optional, Matcher,
                              SPath, Context, Tuple, Callable, Config, Path)

from pylightnix.core import (realizeSeq, drefrrefsC, rref2path, unrref,
                             reserved, config_dict, store_config_,
                             mkrealization)

from pylightnix.utils import (parsetime, tryreadjson_def, traverse_dict)

from pylightnix.groups import (mkmatch, maponly, mapmin, mkgmatch, latest, best,
                              exact)


def match_all()->Matcher:
  """ [Match](#pylightnix.types.Matcher) **all** the available realizations,
  including zero. Never call to a realizer. """
  return mkmatch(mkgmatch([]))


def match_some(minN:int=1)->Matcher:
  """ Call to a realizer if there are less than `minN` realizations in storage.
  Matche `minN` or more realizations. """
  assert minN>=0, f"Argument of match_some should be >=0, not {minN}"
  return mkmatch(mapmin(minN,mkgmatch([])))


def match_only()->Matcher:
  """ Matches one or more realizations, but asserts if there are more than one
  realizations matched. """
  return mkmatch(maponly(mapmin(minN=1,ma=mkgmatch([]))))


def match_latest(minN:int=1, topN:int=1)->Matcher:
  """ Match up to `topN` oldest realizations. Call to a realizer if there are
  less than `minN` realizations available. """
  # assert topN>=minN, "Invalid match_latest arguments, should be topN>=minN"
  return mkmatch(mapmin(minN,mkgmatch([latest()],topN=topN)))


def match_best(filename:str, minN:int=1, topN:int=1)->Matcher:
  """ [Match](#pylightnix.types.Matcher) up to `topN` best matches, but not
  less than minN. The score is expected to reside in a file named `filename`.
  """
  # assert topN>=minN, "Invalid match_best arguments, should be topN>=minN"
  return mkmatch(mapmin(minN,mkgmatch([best(filename)],topN=topN)))


# FIXME: repair match_exact
# def match_exact(grps:List[RRefGroup])->Matcher:
#   """ Match exact these groups. Call to a realizer if no groups were seen."""
#   return mkmatch(mapmin(1,mkgmatch([exact(grps)])))
