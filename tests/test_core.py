"""
FIXME: Implement a random storage generator in Hypothesis, and use it in tests
"""

from pylightnix import (
    Build, Config, instantiate, DRef, RRef, Path, RefPath, mklogdir, dirhash,
    store_initialize, build_outpath, assert_valid_dref, assert_valid_rref,
    mknode, store_deps, store_deepdeps, store_gc, assert_valid_hash,
    assert_serializable, assert_valid_config, Manager, mkclosure, build_realize,
    store_rrefs, datahash, PYLIGHTNIX_NAMEPAT, mkdref, mkrref, trimhash, unrref,
    undref, emerge, mkdrefR, store_config )

from tests.imports import (
    given, assume, example, note, settings, text, decimals, integers, rmtree,
    characters, gettempdir, isdir, join, makedirs, from_regex, islink, listdir,
    get_executable, run, dictionaries, one_of, lists, recursive, printable,
    none, booleans, floats, re_compile, composite, event )


PYLIGHTNIX_TEST:str='/tmp/pylightnix_tests'
SHA256SUM=get_executable('sha256sum', 'Please install `sha256sum` tool from `coreutils` package')

def setup_storage(tn:str)->str:
  import pylightnix.core
  storepath=f'/tmp/{tn}'
  rmtree(storepath, onerror=lambda a,b,c:())
  pylightnix.core.PYLIGHTNIX_STORE=storepath
  pylightnix.core.PYLIGHTNIX_TMP='/tmp'
  store_initialize(exist_ok=False)
  assert 0==len(listdir(storepath))
  return storepath

def setup_testpath(name:str)->Path:
  testpath=join(PYLIGHTNIX_TEST, name)
  rmtree(testpath, onerror=lambda a,b,c:())
  makedirs(testpath, exist_ok=False)
  return Path(testpath)


#   ____                           _
#  / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __ ___
# | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__/ __|
# | |_| |  __/ | | |  __/ | | (_| | || (_) | |  \__ \
#  \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|  |___/


@composite
def dicts(draw):
  d=draw(
    dictionaries(
      keys=text(printable),
      values=recursive(none() | booleans() | floats() | text(printable) | integers(),
                lambda children:
                  lists(children) |
                  dictionaries(text(printable), children),
                  max_leaves=10)
      ))
  event(str(d))
  return d

@composite
def configs(draw):
  d=draw(dicts())
  name=draw(one_of(none(), names()))
  if name is not None:
    d.update({'name':name})
  return Config(d)

def names():
  return from_regex(re_compile(f'^{PYLIGHTNIX_NAMEPAT}+$'))

def hashes():
  return text().map(lambda x: datahash([x]))

@composite
def drefs(draw):
  return mkdref(trimhash(draw(hashes())), draw(names()))

@composite
def rrefs(draw):
  return mkrref(trimhash(draw(hashes())), trimhash(draw(hashes())), draw(names()))








# _____         _
#|_   _|__  ___| |_ ___
#  | |/ _ \/ __| __/ __|
#  | |  __/\__ \ |_\__ \
#  |_|\___||___/\__|___/


@given(dref=drefs())
def test_dref(dref):
  dref2=mkdref(*undref(dref))
  assert dref2==dref

@given(rref=rrefs())
def test_rref(rref):
  rref2=mkrref(*unrref(rref))
  assert rref2==rref
  dref=mkdrefR(rref)
  assert_valid_dref(dref)


@given(cfg=configs())
def test_config(cfg):
  assert_valid_config(cfg)

def test_mklogdir1()->None:
  path=setup_testpath('mklogdir1')
  logdir=mklogdir(tag='testtag',logrootdir=Path(path))
  assert isdir(logdir)

@given(strtag=from_regex(r'[a-zA-Z0-9_:-]+', fullmatch=True),
       timetag=from_regex(r'[a-zA-Z0-9_:-]+', fullmatch=True))
def test_mklogdir2(strtag,timetag)->None:
  path=setup_testpath('mklogdir2')
  logdir=mklogdir(tag=strtag,logrootdir=Path(path), timetag=timetag)
  assert isdir(logdir)
  assert islink(join(path,f'_{strtag}_latest'))


def test_dirhash()->None:
  path=setup_testpath('dirhash')
  h1=dirhash(path)
  assert_valid_hash(h1)
  with open(join(path,'_a'),'w') as f:
    f.write('1')
  h2=dirhash(path)
  assert_valid_hash(h2)
  assert h1==h2, "Test expected to ignore files starting from underscope"
  with open(join(path,'a'),'w') as f:
    f.write('1')
  h3=dirhash(path)
  assert_valid_hash(h3)
  assert h3 != h2


@given(d=dictionaries(keys=text(), values=text()))
def test_dirhash2(d)->None:
  path=setup_testpath('dirhash2')
  with open(join(path,'a'),'w') as f:
    f.write(str(d))
  p=run([SHA256SUM, join(path,'a')], stdout=-1, check=True, cwd=path)
  h=dirhash(path)
  assert (p.stdout[:len(h)].decode('utf-8'))==h

def test_setup_storege()->None:
  setup_storage('a')
  setup_storage('a')


@given(d=dicts())
def test_mknode(d)->None:
  setup_storage('test_mknode')
  m=Manager()
  mknode(m, d)
  dref=m.builders[-1][0]
  assert_valid_dref(dref)
  assert len(list(store_rrefs(dref))) == 0
  rref=m.builders[-1][2](dref, mkclosure())
  assert rref is None
  rref=build_realize(dref, m.builders[-1][1](dref, mkclosure()))
  assert len(list(store_rrefs(dref))) == 1
  assert_valid_rref(rref)
  rref2=m.builders[-1][2](dref, mkclosure())
  assert rref==rref2


@given(d=dicts())
def test_emerge(d)->None:
  setup_storage('test_emerge')

  def _setup(m):
    n1=mknode(m, d)
    n2=mknode(m, {'parent1':n1})
    n3=mknode(m, {'parent2':n1})
    toplevel=mknode(m, {'n1':n1,'n2':n2,'n3':n3})
    return toplevel

  rref=emerge(_setup)
  assert_valid_rref(rref)

  c=store_config(mkdrefR(rref))
  assert_valid_config(c)



# @given(key=text(min_size=1,max_size=10),
#        value=text(min_size=1,max_size=10))
# def test_mknode(key,value)->None:
#   setup_storage('modelcap_mknode')

#   n1=mknode({key:value})
#   assert_valid_ref(n1)
#   n2=mknode({key:value, 'parent':n1})
#   assert_valid_ref(n1)
#   n3=mknode({key:value, 'parent':n2})
#   assert_valid_ref(n3)

# @given(key=text(min_size=1,max_size=10),
#        value=text(min_size=1,max_size=10))
# def test_store_deps(key,value)->None:
#   setup_storage('modelcap_store_deps')

#   n1=mknode({key:value})
#   n2=mknode({key:value, 'parent':n1})
#   n3=mknode({key:value, 'parent':n2})

#   n2_deps=store_deps(n2)
#   assert n2_deps == [n1]
#   n3_deps=store_deps(n3)
#   assert n3_deps == [n2]

# @given(key=text(min_size=1,max_size=10),
#        value=text(min_size=1,max_size=10))
# def test_store_deepdeps(key,value)->None:
#   setup_storage('modelcap_store_deepdeps')

#   n1=mknode({key:value})
#   n2=mknode({key:value, 'parent':n1})
#   n3=mknode({key:value, 'parent':n2})

#   n3_deepdeps=store_deepdeps([n3])
#   assert set(n3_deepdeps) == set([n1,n2,n3]), f"{n3_deepdeps} != [{n1},{n2},{n3}]"


# @given(key=text(min_size=1,max_size=10),
#        value=text(min_size=1,max_size=10))
# def test_store_gc(key,value)->None:
#   setup_storage('modelcap_store_gc')

#   n1=mknode({key:value, 'n':1})
#   n2=mknode({key:value, 'parent':n1})
#   n3=mknode({key:value, 'parent':n2})
#   n4=mknode({key:value, 'n':4})

#   removed=store_gc([n3])
#   assert set(removed) == set([n4]), f"{removed} != [{n4}]"

