from pylightnix.imports import (chain, join, isfile, isdir, islink, defaultdict)

from pylightnix.types import (Any, DRef, RRef, Dict, List, Union, RealizeArg,
                              Realizer, Closure, Iterable, Optional, Matcher,
                              SPath, Context, Tuple, Callable, Config, Path,
                              RConfig, Manager, Set, Hash, NewType, TypeVar)

from pylightnix.core import (realizeSeq, drefrrefsC, store_rref2path, unrref,
                             reserved, config_dict, store_config_,
                             mkrealization, rref2dref, mkdrv, context_deref)

from pylightnix.utils import (parsetime, tryreadjson_def, traverse_dict, isrref,
                              isdref, dirhash, writejson, readjson, concat)


#: Realization Tag is a user-defined string without spaces and newline symbols.
#: There is a special tag named 'out' which is used by default. Users may choose
#: to introduce other tags, like 'doc','man' or 'checkpoint'. User-tagged
#: realizations should refer to some specific 'out' realization.  For
#: realizations, Having the same tag would mean that those realizations share
#: some functionality, e.g. contain documentation or are ML model checkpoints.
#:
#: Every 'out' realization plus zero-to-many other tagged realizations form a
#: [Group](#pylightnix.types.Group). The group behaves as a whole during
#: [Matching](#pylightnix.types.Matcher).
#:
#: Tag invariants:
#: - Each RRef has its Tag, the default tag name is 'out'
#: - Several realization of a derivation may have the same tag. That means they
#:   contain functionally equivalent artifacts.
Tag = NewType('Tag', str)

#: RRefGroup unites [tagged](#pylightnix.types.Tag) realizations. For
#: example, there may be a Group containing tags ['out',log'] and another Group
#: containing realizations tagged with ['out','log','docs']. Each group must
#: contain at least one realization tagged with tag 'out' Only 'out'
#: realizations are subjects for [matching](#pylightnix.types.Matcher).
#:
#: Group invariants:
#: - There are no empty Groups
#: - Each realization belongs to exactly one Group
#: - All realizations of a Group originates from the same derivation
#: - All realizations of a Group have the same Context
#: - At least one realization of a group hase tag 'out'
#: - All realizations of a Group have different tags
RRefGroup = Dict[RRef,Tag]

#: Group information record. Fields are 'tag' and 'group'.
GInfo = Dict[str,str]

#: Group identifoer, which consists of sorted hash strings separated with '|'
GSig = NewType('GSig', str)

GRealizer = Callable[[SPath,DRef,Context,RealizeArg],List[Dict[Path,Tag]]]

GMatcher = Callable[[SPath,DRef,Context],Optional[List[RRefGroup]]]

Key = Callable[[RRefGroup,SPath],Optional[Union[int,float,str]]]

#: PromisePath is an alias for Python list of strings. The first item is a
#: special tag (the [promise](#pylightnix.core.promise) or the
#: [claim](#pylightnix.core.claim)) and the subsequent
#: items should represent a file or directory path parts. PromisePaths are
#: typically fields of [Configs](#pylightnix.types.Config). They represent
#: paths to the artifacts which we promise will be created by the derivation
#: being currently configured.
#:
#: PromisePaths do exist only at the time of instantiation. Pylightnix converts
#: them into [RefPath](#pylightnix.types.RefPath) before the realization
#: starts. Converted configs change their type to
#: [RConfig](#pylightnix.type.RConfig)
#:
#: Example:
#: ```python
#: from pylightnix import mkconfig, mkdrv, promise
#: def myconfig()->Config:
#:   name = "config-of-some-stage"
#:   promise_binary = [promise, 'usr','bin','hello']
#:   other_params = 42
#:   return mkconfig(locals())
#: dref=mkdrv(..., config=myconfig(), ...)
#: ```
PromisePath = List[Any]

#  ____                      _
# |  _ \ _ __ ___  _ __ ___ (_)___  ___  ___
# | |_) | '__/ _ \| '_ ` _ \| / __|/ _ \/ __|
# |  __/| | | (_) | | | | | | \__ \  __/\__ \
# |_|   |_|  \___/|_| |_| |_|_|___/\___||___/

def config_promises(c:Config, r:DRef)->List[Tuple[str,PromisePath]]:
  promises=[]
  def _mut(key:Any, val:Any):
    nonlocal promises
    if ispromise(val):
      promises.append((str(key),val))
    return val
  traverse_dict(config_dict(c),_mut)
  return promises

def assert_promise_fulfilled(k:str, p:PromisePath, o:Path)->None:
  ppath=join(o,*p[1:])
  assert isfile(ppath) or isdir(ppath) or islink(ppath), (
      f"Promise '{k}' of {p[0]} is not fulfilled. "
      f"{ppath} is expected to be a file or a directory.")

def checkpromise(ma:GMatcher)->GMatcher:
  """ A matcher that checks that all group promises are fulfilled """
  def _matcher(S:SPath, dref:DRef, ctx:Context)->Optional[List[RRefGroup]]:
    grps=ma(S,dref,ctx)
    if grps is None:
      return None
    for key,promisepath in config_promises(store_config_(dref,S),dref):
      for g in grps:
        assert_promise_fulfilled(key,promisepath,store_rref2path(groupmain(g),S))
    return grps
  return _matcher

def config_substitutePromises(c:Config, r:DRef)->RConfig:
  """ Replace all Promise tags with DRef `r`. In particular, all PromisePaths
  are converted into RefPaths. """
  d=config_dict(c)
  def _mut(k:Any,val:Any):
    if ispromise(val) or isclaim(val):
      return [DRef(r)]+val[1:]
    else:
      return val
  traverse_dict(d,_mut)
  return RConfig(d)

def mktag(s:str)->Tag:
  for c in ['\n',' ']:
    assert c not in s, f"Invalid symbol '{c}' in tag '{s}'"
  return Tag(s)

def store_config(r:Union[DRef,RRef],S=None)->RConfig:
  """ Read the [Config](#pylightnix.types.Config) of the derivation and
  [resolve](#pylightnix.core.config_substitutePromises) all its promises and
  claims. """
  assert isrref(r) or isdref(r), (
      f"Invalid reference '{r}'. Expected either RRef or DRef." )
  if isrref(r):
    dref=rref2dref(RRef(r))
  else:
    dref=DRef(r)
  return config_substitutePromises(store_config_(dref,S),dref)

#: *Do not change!*
#: A tag to mark the start of [PromisePaths](#pylightnix.types.PromisePath).
PYLIGHTNIX_PROMISE_TAG = "__promise__"

#: *Do not change!*
#: A tag to mark the start of [PromisePaths](#pylightnix.types.PromisePath). In
#: contrast to promises, Pylightnix doesn't check the claims
PYLIGHTNIX_CLAIM_TAG = "__claim__"


#: Promise is a magic constant required to create
#: [PromisePath](#pylightnix.types.PromisePath), where it is used as a start
#: marker. Promise paths do exist only during
#: [instantiation](#pylightnix.core.instantiate) pass. The core replaces all
#: PromisePaths with corresponding [RefPaths](#pylightnix.type.RefPath)
#: automatically before it starts the realization pass (see
#: [store_config](#pylightnix.core.store_config)).
#:
#: Ex-PromisePaths may be later converted into filesystem paths by
#: [build_path](#pylightnix.core.build_path) or by
#: [Lenses](#pylightnix.lens.Lens) as usual.
promise = PYLIGHTNIX_PROMISE_TAG

#: Claim is a [promise](#pylightnix.core.promise) which is not checked by the
#: Pylightnix. All other properties of promises are valid for claims.  All
#: PromisPaths which start from `claim` are substituted with corresponding
#: RefPaths by Pylightnix and may be later converted into system paths.
claim = PYLIGHTNIX_CLAIM_TAG

def ispromisepath(p:Any)->bool:
  return isinstance(p,list) and len(p)>0 and all([isinstance(x,str) for x in p]) and \
         p[0]==PYLIGHTNIX_PROMISE_TAG

def ispromiselike(p:Any, ptag:str):
  return isinstance(p,list) and len(p)>0 and (p[0]==ptag) and \
         all([isinstance(x,str) for x in p])

def ispromise(p:Any)->bool:
  return ispromiselike(p,PYLIGHTNIX_PROMISE_TAG)

def isclaim(p:Any)->bool:
  return ispromiselike(p,PYLIGHTNIX_CLAIM_TAG)

#  ____
# / ___|_ __ ___  _   _ _ __  ___
#| |  _| '__/ _ \| | | | '_ \/ __|
#| |_| | | | (_) | |_| | |_) \__ \
# \____|_|  \___/ \__,_| .__/|___/
#                      |_|

# def mkrgroup(dref:DRef, ctx:Context,
#              og:Dict[Tag,Path], S=None)->RRefGroup:
#   """ Create [realization group](#pylightnix.types.Group) in storage `S` by
#   iteratively calling [mkrealization](#pylightnix.core.mkrealization). """
#   rrefg={}
#   rrefg[tag_out()]=mkrealization(dref,ctx,og[tag_out()],leader=None,S=S)
#   for tag,o in og.items():
#     if tag!=tag_out():
#       rrefg[tag]=mkrealization(dref,ctx,o,leader=(tag,rrefg[tag_out()]),S=S)
#   return rrefg


def tag_out()->Tag:
  """ Pre-defined default Tag name """
  return mktag('out')

# def mkgroup(s:str)->Group:
#   for c in ['\n',' ']:
#     assert c not in s
#   return Group(s)

# def store_tag(rref:RRef,S=None)->Tag:
#   """ Return the [Tag](#pylightnix.types.tag) of a Realization. Default Tag
#   name is 'out'. """
#   return mktag(tryreadjson_def(
#     reserved(store_rref2path(rref,S),'group.json'),{}).get('tag','out'))

def pathginfo(path:Path)->List[GInfo]:
  """ Return group identifier of the realization """
  return readjson(join(path,'groups.json'))

def rrefgroups(rref:RRef,S=None)->List[GInfo]:
  """ Return group identifier of the realization """
  return pathginfo(store_rref2path(rref,S))


_A3 = TypeVar('_A3')
def vals2groups_(vals:Iterable[_A3],
                 fpath:Callable[[_A3],Path])->List[Dict[_A3,Tag]]:
  """ Split RRefs to a set of [Groups](#pylightnix.types.Group), according to
  their [Tags](#pylightnix.types.Tag)

  FIXME: re-implement with a complexity better than O(N^2)
  """
  acc:Dict[Any,Dict[_A3,Tag]]=defaultdict(dict)
  for val in vals:
    for ginfo in pathginfo(fpath(val)):
      acc[tuple(ginfo['peers'])][val]=mktag(ginfo['tag'])
  return list(acc.values())

def paths2groups(paths:Iterable[Path])->List[Dict[Path,Tag]]:
  return vals2groups_(paths, lambda x:x)

def rrefs2groups(rrefs:Iterable[RRef],S=None)->List[RRefGroup]:
  return vals2groups_(rrefs, lambda rref:store_rref2path(rref,S=S))

  # return [({store_tag(rref,S):rref for rref in rrefs if store_group(rref,S)==g})
  #   for g in sorted({store_group(rref,S) for rref in rrefs})]


_A1 = TypeVar('_A1')
def groups2vals_(grs:List[Dict[_A1,Tag]])->List[_A1]:
  return list(sorted(set(chain.from_iterable([gr.keys() for gr in grs]))))

def groups2paths(grs:List[Dict[Path,Tag]])->List[Path]:
  return groups2vals_(grs)

def groups2rrefs(grs:List[Dict[RRef,Tag]])->List[RRef]:
  return groups2vals_(grs)


def groupsig(g:RRefGroup)->GSig:
  """ Get the group signature of RRefGroup """
  ginfos=set.intersection(*concat([rrefgroups(rref) for rref in g.keys()]))
  assert len(ginfos)==1
  return GSig(ginfos.pop()['group'])

# def grouprref(gr:RRefGroup)->RRef:
#   return gr[tag_out()]
_A2 = TypeVar('_A2')
def groupmain(rg:Dict[_A2,Tag])->_A2:
  vals=[val for val,tag in rg.items() if tag==tag_out()]
  assert len(vals)==1
  return vals[0]

# def group2sign(grp:RRefGroup)->List[Tuple[RRef,Tag]]:
#   return list(sorted([(rref,tag) for rref,tag in grp.items()]))
# def group_in(grp:RRefGroup, grps:List[RRefGroup])->bool:
#   return group2sign(grp) in set({group2sign(gr) for gr in grps})


def mkrealizer(r:GRealizer)->Realizer:
  def _ungroup(S:SPath,dref:DRef,ctx:Context,rarg:RealizeArg)->List[Path]:
    gpaths:List[Dict[Path,Tag]]=r(S,dref,ctx,rarg)
    # Check promises
    for key,promisepath in config_promises(store_config_(dref,S),dref):
      for gp in gpaths:
        assert_promise_fulfilled(key,promisepath,groupmain(gp))
    # Record group information
    path2gid:Dict[Path,List[int]]=defaultdict(list)
    path2hash:Dict[Path,Hash]={}

    for gid,tagpaths in enumerate(gpaths):
      for path,tag in tagpaths.items():
        path2gid[path].append(gid)
    for path in path2gid.keys():
      path2hash[path]=dirhash(path)
    def _mkgsig(gid:int, path:Path)->dict:
      return {'tag':gpaths[gid][path],
              'group':sorted([path2hash[p] for p in gpaths[gid].keys()])}
    for path,gids in path2gid.items():
      writejson(
        join(path,'groups.json'),
        sorted([_mkgsig(gid, path) for gid in gids],
               key=lambda x:(x['tag'],x['group'])))

    return groups2paths(gpaths)
  return _ungroup


def mkdrvG(m:Manager, config:Config, matcher:GMatcher, realizer:GRealizer)->DRef:
  return mkdrv(m,config,mkmatch(matcher),mkrealizer(realizer))


def context_derefG(ctx:Context, dref:DRef, S=None)->List[RRefGroup]:
  return rrefs2groups(context_deref(ctx,dref),S=S)


#  __  __       _       _
# |  \/  | __ _| |_ ___| |__   ___ _ __ ___
# | |\/| |/ _` | __/ __| '_ \ / _ \ '__/ __|
# | |  | | (_| | || (__| | | |  __/ |  \__ \
# |_|  |_|\__,_|\__\___|_| |_|\___|_|  |___/

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
    grps={groupmain(gr):gr for gr in rrefs2groups(drefrrefsC(dref,context,S))}
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
      with open(join(store_rref2path(groupmain(gr),S),'__buildtime__.txt'),'r') as f:
        t=parsetime(f.read())
        return float(0 if t is None else t)
    except OSError:
      return float(0)
  return _key


def best(filename:str)->Key:
  def _key(gr:RRefGroup,S=None)->Optional[Union[int,float,str]]:
    try:
      with open(join(store_rref2path(groupmain(gr),S),filename),'r') as f:
        return float(f.readline())
    except OSError:
      return float('-inf')
    except ValueError:
      return float('-inf')
  return _key


def texthash()->Key:
  def _key(gr:RRefGroup,S=None)->Optional[Union[int,float,str]]:
    return str(unrref(groupmain(gr))[0])
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



