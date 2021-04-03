from pylightnix import (Manager, SPath, RConfig, datahash, PYLIGHTNIX_NAMEPAT,
                        mkdref, mkrref, trimhash, encode, instantiate_,
                        dagroots)

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
  event(str(d))
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
def intdags_permutations(draw):
  """ Return a list of instances of a same DAG. Instances are not nesessarily
  topologically sorted """
  return draw(lists(permutations(draw(intdags())),min_size=3,max_size=3))

# @composite
# def nrrefs(draw):
#   N=draw(integers(min_value=1,max_value=3))
#   acc=[]
#   for nrrefs in range(N):
#     acc.append([f"tag{n}" for n in range(ntags-1)]+[tag_out()])
#   return acc

@composite
def rootstages(draw, min_size:int=1, max_size:int=10, partial_matches:bool=True):
  dag=draw(intdags(min_size=min_size,
                   max_size=max_size).filter(lambda dag: len(dag)>0))
  note(f"DAG: {dag}")
  roots=dagroots([n for n,_ in dag], lambda n:dag[n][1])
  rrefnums={n:draw(integers(min_value=1,max_value=3)) for n,_ in dag}
  note(f"Rref numbers: {rrefnums}")
  if partial_matches:
    nmatches={n:draw(integers(min_value=1,max_value=max(1,rrefnums[n]-1))) for n,_ in dag}
  else:
    nmatches={n:rrefnums[n] for n,_ in dag}
  note(f"NMatches {nmatches}")
  # Signature: (NodeID -> (GroupID -> NonDetValue))
  nondets={n:{i:draw(integers(min_value=1,max_value=5)) for i in range(rrefnums[n])} for n,_ in dag}
  note(f"nondets: {nondets}")

  def _stage(m, root):
    drefs:dict={}
    for n,deps in list(dag):

      def _nondet(ngroup,nn):
        a=nondets[nn]
        return a[ngroup]

      drefs[n]=mkstage(m,
                       config={'name':f'node_{n}',
                               'parents':[drefs[d] for d in deps]},
                       nondet=partial(_nondet,nn=n),
                       nrrefs=rrefnums[n],
                       nmatch=nmatches[n])
    return drefs[root]
  return [partial(_stage, root=root) for root in roots]


