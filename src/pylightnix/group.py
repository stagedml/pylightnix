from pylightnix.imports import (chain, join)

from pylightnix.types import (DRef, RRef, Dict, List, Union, RealizeArg,
                              Realizer, RRefGroup, Closure, Iterable, Key,
                              Optional, Matcher, SPath, Context, Tuple, Tag,
                              Callable, Group)

from pylightnix.core import (realizeSeq, drefrrefsC, store_rref2path, unrref,
                             reserved)

from pylightnix.utils import (parsetime, tryreadjson_def)

def mktag(s:str)->Tag:
  for c in ['\n',' ']:
    assert c not in s, f"Invalid symbol '{c}' in tag '{s}'"
  return Tag(s)


def tag_out()->Tag:
  """ Pre-defined default Tag name """
  return mktag('out')


def mkgroup(s:str)->Group:
  for c in ['\n',' ']:
    assert c not in s
  return Group(s)

def store_tag(rref:RRef,S=None)->Tag:
  """ Return the [Tag](#pylightnix.types.tag) of a Realization. Default Tag
  name is 'out'. """
  return mktag(tryreadjson_def(
    reserved(store_rref2path(rref,S),'group.json'),{}).get('tag','out'))

def store_group(rref:RRef,S=None)->Group:
  """ Return group identifier of the realization """
  return mkgroup(tryreadjson_def(
    reserved(store_rref2path(rref,S),'group.json'),{}).get('group',rref))

def rrefs2groups(rrefs:Iterable[RRef], S=None)->List[RRefGroup]:
  """ Split RRefs to a set of [Groups](#pylightnix.types.Group), according to
  their [Tags](#pylightnix.types.Tag)

  FIXME: re-implement with a complexity better than O(N^2)
  """
  return [({store_tag(rref,S):rref for rref in rrefs if store_group(rref,S)==g})
    for g in sorted({store_group(rref,S) for rref in rrefs})]


def groups2rrefs(grs:List[RRefGroup])->List[RRef]:
  """ Merges several [Groups](#pylightnix.types.Group) of RRefs into a plain
  list of RRefs """
  return list(chain.from_iterable([gr.values() for gr in grs]))

def grouprref(gr:RRefGroup)->RRef:
  return gr[tag_out()]

def group2sign(grp:RRefGroup)->List[Tuple[RRef,Tag]]:
  return list(sorted([(rref,tag) for tag,rref in grp.items()]))

def group_in(grp:RRefGroup, grps:List[RRefGroup])->bool:
  return group2sign(grp) in set({group2sign(gr) for gr in grps})


def realizeGroups(closure:Closure,
                 force_rebuild:Union[List[DRef],bool]=[],
                 assert_realized:List[DRef]=[],
                 realize_args:Dict[DRef,RealizeArg]={})->List[RRefGroup]:
  """ Return a collection of tagged [realizations](#pylightnix.types.RRef)
  references.
  """
  res:List[RRefGroup]
  force_interrupt:List[DRef]=[]
  if isinstance(force_rebuild,bool):
    if force_rebuild:
      force_interrupt=[closure.dref]
  elif isinstance(force_rebuild,list):
    force_interrupt=force_rebuild
  else:
    assert False, "Ivalid type of `force_rebuild` argument"
  try:
    gen=realizeSeq(closure,force_interrupt=force_interrupt,
                           assert_realized=assert_realized,
                           realize_args=realize_args)
    next(gen)
    while True:
      gen.send((None,False)) # Ask for default action
  except StopIteration as e:
    res=e.value
  return res

#  __  __       _       _
# |  \/  | __ _| |_ ___| |__   ___ _ __ ___
# | |\/| |/ _` | __/ __| '_ \ / _ \ '__/ __|
# | |  | | (_| | || (__| | | |  __/ |  \__ \
# |_|  |_|\__,_|\__\___|_| |_|\___|_|  |___/

GMatcher = Callable[[SPath,DRef,Context],Optional[List[RRefGroup]]]

def mkmatch(gmatch:GMatcher)->Matcher:
  def _matcher(S:SPath, dref:DRef, context:Context)->Optional[List[RRef]]:
    grps=gmatch(S,dref,context)
    return groups2rrefs(grps) if grps is not None else None
  return _matcher


def mkgmatch(keys:List[Key], topN:Optional[int]=None)->GMatcher:
  """ Create a [Matcher](#pylightnix.types.Matcher) by combining different
  sorting keys and selecting a top-n threshold.

  Only realizations which have [tag](#pylightnix.types.Tag) 'out' (which is a
  default tag name) participate in matching. After the matching, Pylightnix
  adds all non-'out' realizations which share [group](#pylightnix.types.Group)
  with at least one matched realization.

  Arguments:
  - `keys`: A list of [Key](#pylightnix.types.Key) functions.
  - `topN`: Limits the number of best matches to thin number.
  """
  keys=keys+[texthash()]
  def _gmatcher(S:SPath, dref:DRef, context:Context)->Optional[List[RRefGroup]]:
    # Find realizations tagged with 'out' among the available realizations
    grps={grouprref(gr):gr for gr in rrefs2groups(drefrrefsC(dref,context,S))}
    # Calculate a list of keys for every group
    keymap:Dict[RRef,List[Optional[Union[int,float,str]]]]=\
      {rref:[k(gr,S) for k in keys] for rref,gr in grps.items()}
    # Filter-out None results and sort the remaining groups by keys
    goodkeys=\
      sorted(filter(lambda rref: None not in keymap[rref], grps.keys()),
             key=lambda rref:keymap[rref], reverse=True)
    # Return topN best matches
    return [grps[gk] for gk in goodkeys][:topN]
  return _gmatcher


def exact(grps:List[RRefGroup])->Key:
  signs=[group2sign(g) for g in grps]
  def _key(grp:RRefGroup,S=None)->Optional[Union[int,float,str]]:
    return 1 if group2sign(grp) in signs else None
  return _key


def latest()->Key:
  def _key(gr:RRefGroup,S=None)->Optional[Union[int,float,str]]:
    try:
      with open(join(store_rref2path(grouprref(gr),S),'__buildtime__.txt'),'r') as f:
        t=parsetime(f.read())
        return float(0 if t is None else t)
    except OSError:
      return float(0)
  return _key


def best(filename:str)->Key:
  def _key(gr:RRefGroup,S=None)->Optional[Union[int,float,str]]:
    try:
      with open(join(store_rref2path(grouprref(gr),S),filename),'r') as f:
        return float(f.readline())
    except OSError:
      return float('-inf')
    except ValueError:
      return float('-inf')
  return _key


def texthash()->Key:
  def _key(gr:RRefGroup,S=None)->Optional[Union[int,float,str]]:
    return str(unrref(grouprref(gr))[0])
  return _key


def mappred(pred:Callable[[List[RRefGroup]],bool], ma:GMatcher)->GMatcher:
  """ Calls for a realizer if the number of matches is below the minimum """
  def _matcher(S:SPath, dref:DRef, ctx:Context)->Optional[List[RRefGroup]]:
    grps=ma(S,dref,ctx)
    if grps is None:
      return None
    if not pred(grps):
      return None
    return grps
  return _matcher


def mapmin(minN:int, ma:GMatcher)->GMatcher:
  """ Call for a realizer if the number of matches is below the number """
  return mappred(lambda grps:len(grps)>=minN,ma)


def mapsome(ma:GMatcher)->GMatcher:
  """ Call for a realizer if the number of matches is zero. """
  return mapmin(1,ma)


def maponly(ma:GMatcher)->GMatcher:
  def _matcher(S:SPath, dref:DRef, ctx:Context)->Optional[List[RRefGroup]]:
    grps=ma(S,dref,ctx)
    if grps is None:
      return None
    assert len(grps)==1, (
      f"Matcher expects exactly one realization, but there are {len(grps)}:\n"
      f"{grps}")
    return grps
  return _matcher


def match_all()->Matcher:
  """ [Match](#pylightnix.types.Matcher) **all** the available realizations,
  including zero. Never call to a realizer. """
  return mkmatch(mkgmatch([]))


def match_some(minN:int=1)->Matcher:
  """ Call to a realizer if there are less than `minN` realizations in storage.
  Matche `minN` or more realizations. """
  assert minN>=0, f"Arguement of match_some should be >=0, not {minN}"
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


def match_exact(grps:List[RRefGroup])->Matcher:
  """ Match exact these groups. Call to a realizer if no groups were seen."""
  return mkmatch(mapmin(1,mkgmatch([exact(grps)])))

