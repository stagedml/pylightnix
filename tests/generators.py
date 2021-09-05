from pylightnix import (Registry, RConfig, datahash, PYLIGHTNIX_NAMEPAT, mkdref,
                        mkrref, trimhash, encode, dagroots, List,
                        DRef, Callable)

from tests.imports import (given, assume, example, note, settings, text,
                           decimals, integers, rmtree, characters, gettempdir,
                           isdir, join, makedirs, from_regex, islink, listdir,
                           get_executable, run, dictionaries, one_of, lists,
                           recursive, printable, none, booleans, floats,
                           re_compile, composite, event, binary, just, sets,
                           permutations, sampled_from, partial)


from tests.setup import (mkstage)

#   ____                           _
#  / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __ ___
# | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__/ __|
# | |_| |  __/ | | |  __/ | | (_| | || (_) | |  \__ \
#  \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|  |___/

@composite
def drefs(draw):
  return mkdref(trimhash(draw(hashes())), draw(names()))

@composite
def rrefs(draw):
  return mkrref(trimhash(draw(hashes())), trimhash(draw(hashes())), draw(names()))

@composite
def dicts(draw, prims=none()):
  d=draw(
    dictionaries(
      keys=text(printable),
      values=recursive(none() | booleans() | floats() | text(printable) | integers() | prims,
                lambda children:
                  lists(children) |
                  dictionaries(text(printable), children),
                  max_leaves=10)
      ))
  return d

def dicts_with_refs():
  return dicts(prims=rrefs() | drefs())

@composite
def configs(draw):
  d=draw(dicts())
  name=draw(one_of(none(), names()))
  if name is not None:
    d.update({'name':name})
  return RConfig(d)

def names():
  return from_regex(re_compile(f'^{PYLIGHTNIX_NAMEPAT}+$'))

def hashes():
  return text().map(lambda x: datahash([('testhash',encode(x))]))

def prims():
  return one_of(none(), booleans(), floats(), text(printable), integers(), binary())

def bindata():
  return one_of(one_of(booleans(), floats(), integers()).map(lambda x: str(x)).map(lambda x: bytes(x,'utf-8')),
                text(printable).map(lambda x: bytes(x,'utf-8')),
                binary())

@composite
def artifacts(draw):
  ns=draw(lists(names(),min_size=1))
  vals=draw(lists(bindata(),min_size=len(ns),max_size=len(ns)))
  return {n:v for n,v in zip(ns,vals)}

@composite
def intdags(draw, min_size:int=1, max_size:int=10):
  """ Return random DAG as List[Tuple[int,Set[int]]]. Returned DAGs are
  topologically sorted by construction. """
  N=draw(integers(min_value=min_size,max_value=max_size))
  seen:list=[]
  acc:list=[]
  for n in range(N):
    deps=draw(sets(sampled_from(seen))) if seen else []
    acc.append((n,set(deps)))
    seen.append(n)
  return acc

@composite
def intdags_permutations(draw, min_size:int=1, max_size:int=10):
  """ Produce instances of a same DAG. Instances are not nesessarily
  topologically sorted """
  return draw(lists(permutations(draw(intdags())),
                    min_size=min_size,
                    max_size=max_size))

@composite
def rootstages(draw,
               min_size:int=1,
               max_size:int=10,
               partial_matches:bool=True,
               failchances:List[int]=[],
               stagefn=mkstage):
  """ Produce Pylightnix stage hierarchies
  Note: A signature of `nondets` is: (NodeID -> (RRefID -> NonDetValue))
  `failchances` indicates how many errors to introduce into a hierarchy. For
  example, setting it to `[100,100]` would make 2 attempts to mark some stage
  with a 'deliberate error' flag.

  DEPRECATED in favor of `hierarchies`
  """
  assert all([x>=0 and x<=100 for x in failchances])
  dag=draw(intdags(min_size=min_size,
                   max_size=max_size).filter(lambda dag: len(dag)>0))
  note(f"DAG: {dag}")
  roots=dagroots([n for n,_ in dag], lambda n:dag[n][1])
  nrrefs={n:draw(integers(min_value=1,max_value=3)) for n,_ in dag}
  note(f"Rref numbers: {nrrefs}")
  nmatches={n:draw(integers(min_value=1,max_value=max(1,nrrefs[n]-1)))
            for n,_ in dag} if partial_matches else {n:nrrefs[n] for n,_ in dag}
  note(f"NMatches {nmatches}")
  nondets={n:{i:draw(integers(min_value=1,max_value=5))
              for i in range(nrrefs[n])} for n,_ in dag}
  nfails={n:False for n,_ in dag}
  for pfail in failchances:
    fail=draw(sampled_from(([True]*pfail)+([False]*(100-pfail))))
    if fail:
      nfails[draw(sampled_from([n for n,_ in dag]))]=True

  def _nondet(ngroup,nn):
    return nondets[nn][ngroup]

  def _stage(r, root):
    drefs:dict={}
    for n,deps in list(dag):
      drefs[n]=stagefn(config={'name':f'node_{n}',
                               'parents':[drefs[d] for d in deps]},
                       r=r,
                       nondet=partial(_nondet,nn=n),
                       nrrefs=nrrefs[n],
                       nmatch=nmatches[n],
                       mustfail=nfails[n])
    return drefs[root]
  return [partial(_stage, root=root) for root in roots]


@composite
def stages(draw,
           min_nrrefs=1, max_nrrefs=3,
           min_nmatch=1, max_nmatch=3,
           pfail=0):
  assert pfail>=0 and pfail<=100
  nrrefs=draw(integers(min_value=min_nrrefs,max_value=max_nrrefs))
  nmatch=draw(integers(min_value=min_nmatch,max_value=max_nmatch))
  mustfail=draw(sampled_from(([True]*pfail)+([False]*(100-pfail))))
  return (lambda r,config:mkstage(
                 config=config,
                 r=r,
                 nondet=lambda n:0,
                 starttime='AUTO',
                 nrrefs=nrrefs,
                 nmatch=nmatch,
                 mustfail=mustfail
                 ))


@composite
def hierarchies(draw, min_size=1, max_size=10, stages=stages):
  dag=draw(intdags(min_size=min_size,
                   max_size=max_size).filter(lambda dag: len(dag)>0))
  nroot=draw(sampled_from(list(dagroots([n for n,_ in dag],
                                        lambda n:dag[n][1]))))
  ss=[]
  for n,_ in list(dag):
    ss.append(draw(stages()))
  def _hierarchy(r, **kwargs):
    drefs:dict={}
    for s,(n,ps) in zip(ss,dag):
      drefs[n]=s(r,{"name":f"teststage_{n}",
                    "parents":[drefs[p] for p in ps]}, **kwargs)
    return drefs[nroot]
  return _hierarchy


