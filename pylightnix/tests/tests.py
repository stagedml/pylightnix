"""
FIXME: Implement a random storage generator in Hypothesis, and use it in tests
"""

from pylightnix.tests.imports import (
    given, assume, example, note, settings, text, decimals, integers, rmtree,
    characters, gettempdir, isdir, join, makedirs, from_regex, islink, listdir )

from pylightnix import (
    Model, Config, Path, mklogdir, dhash, store_initialize, model_outpath,
    model_save, assert_valid_ref, mknode, store_deps, store_deepdeps, store_gc )

PYLIGHTNIX_TEST:str='/tmp/pylightnix_tests'

def set_storage(tn:str)->str:
  import pylightnix.core
  storepath=f'/tmp/{tn}'
  rmtree(storepath, onerror=lambda a,b,c:())
  pylightnix.core.PYLIGHTNIX_STORE=storepath
  pylightnix.core.PYLIGHTNIX_TMP='/tmp'
  store_initialize(exist_ok=False)
  assert 0==len(listdir(storepath))
  return storepath

def _make_testpath(name:str)->str:
  testpath=join(PYLIGHTNIX_TEST, name)
  rmtree(testpath, onerror=lambda a,b,c:())
  makedirs(testpath, exist_ok=False)
  return testpath

def test_mklogdir1()->None:
  path=_make_testpath('mklogdir1')
  logdir=mklogdir(tag='testtag',logrootdir=Path(path))
  assert isdir(logdir)

@given(strtag=from_regex(r'[a-zA-Z0-9_:-]+', fullmatch=True),
       timetag=from_regex(r'[a-zA-Z0-9_:-]+', fullmatch=True))
def test_mklogdir2(strtag,timetag)->None:
  path=_make_testpath('mklogdir2')
  logdir=mklogdir(tag=strtag,logrootdir=Path(path), timetag=timetag)
  assert isdir(logdir)
  assert islink(join(path,f'_{strtag}_latest'))


def test_dhash()->None:
  path=_make_testpath('dhash')
  h1=dhash(Path(path))
  assert len(h1)>0
  with open(join(path,'_a'),'w') as f:
    f.write('1')
  h2=dhash(Path(path))
  assert len(h2)>0
  assert h1==h2
  with open(join(path,'a'),'w') as f:
    f.write('1')
  h3=dhash(Path(path))
  assert len(h3)>0
  assert h3 != h2



@given(key=text(min_size=1,max_size=10),
       value=text(min_size=1,max_size=10))
def test_node_lifecycle(key,value)->None:
  set_storage('modelcap_store_lifecycle')

  c=Config({key:value})
  m=Model(c)
  o=model_outpath(m)
  with open(join(o,'artifact'),'w') as f:
    f.write('artifact')
  ref=model_save(m)
  assert_valid_ref(ref)

def test_make_storege()->None:
  set_storage('a')
  set_storage('a')


@given(key=text(min_size=1,max_size=10),
       value=text(min_size=1,max_size=10))
def test_mknode(key,value)->None:
  set_storage('modelcap_mknode')

  n1=mknode({key:value})
  assert_valid_ref(n1)
  n2=mknode({key:value, 'parent':n1})
  assert_valid_ref(n1)
  n3=mknode({key:value, 'parent':n2})
  assert_valid_ref(n3)

@given(key=text(min_size=1,max_size=10),
       value=text(min_size=1,max_size=10))
def test_store_deps(key,value)->None:
  set_storage('modelcap_store_deps')

  n1=mknode({key:value})
  n2=mknode({key:value, 'parent':n1})
  n3=mknode({key:value, 'parent':n2})

  n2_deps=store_deps(n2)
  assert n2_deps == [n1]
  n3_deps=store_deps(n3)
  assert n3_deps == [n2]

@given(key=text(min_size=1,max_size=10),
       value=text(min_size=1,max_size=10))
def test_store_deepdeps(key,value)->None:
  set_storage('modelcap_store_deepdeps')

  n1=mknode({key:value})
  n2=mknode({key:value, 'parent':n1})
  n3=mknode({key:value, 'parent':n2})

  n3_deepdeps=store_deepdeps([n3])
  assert set(n3_deepdeps) == set([n1,n2,n3]), f"{n3_deepdeps} != [{n1},{n2},{n3}]"


@given(key=text(min_size=1,max_size=10),
       value=text(min_size=1,max_size=10))
def test_store_gc(key,value)->None:
  set_storage('modelcap_store_gc')

  n1=mknode({key:value, 'n':1})
  n2=mknode({key:value, 'parent':n1})
  n3=mknode({key:value, 'parent':n2})
  n4=mknode({key:value, 'n':4})

  removed=store_gc([n3])
  assert set(removed) == set([n4]), f"{removed} != [{n4}]"

