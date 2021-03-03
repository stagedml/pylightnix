from pylightnix import (Manager, SPath, RConfig, datahash, PYLIGHTNIX_NAMEPAT,
                        mkdref, mkrref, trimhash, encode, instantiate_,
                        dagroots, tag_out)

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
def intdags(draw):
  """ Return random DAG as List[Tuple[int,Set[int]]]. Returned DAGs are
  topologically sorted by construction. """
  N=draw(integers(min_value=1,max_value=10))
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

@composite
def tagsets(draw):
  N=draw(integers(min_value=1,max_value=3))
  acc=[]
  for ngroup in range(N):
    ntags=draw(integers(min_value=1,max_value=3))
    acc.append([f"tag{n}" for n in range(ntags-1)]+[tag_out()])
  return acc

@composite
def rootstages(draw):
  dag=draw(intdags().filter(lambda dag: len(dag)>0))
  roots=dagroots([n[0] for n in dag], lambda n:dag[n][1])
  # tss={n[0]:draw(tagsets()) for n in dag}
  tss={n[0]:[[tag_out()], [tag_out()]] for n in dag}
  # print(tss)
  # nmatches={n[0]:draw(integers(min_value=1,max_value=2)) for n in dag}
  nmatches={n[0]:99 for n in dag}
  # print('NNNNNNNNN',nmatches)

  def _stage(m, root):
    drefs:dict={}
    for n,deps in list(dag):
      drefs[n]=mkstage(m,
                       config={'name':f'node_{n}',
                               'parents':[drefs[d] for d in deps]},
                       tagset=tss[n],
                       nmatch=nmatches[n])
    return drefs[root]
  return [partial(_stage, root=root) for root in roots]


