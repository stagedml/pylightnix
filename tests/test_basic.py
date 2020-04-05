from pylightnix import ( instantiate, DRef, RRef, Path, mklogdir, dirhash,
    assert_valid_dref, assert_valid_rref, mknode, store_deps, store_deepdeps,
    store_gc, assert_valid_hash, assert_valid_config, Manager, mkcontext,
    store_rrefs, mkdref, mkrref, unrref, undref, realize, rref2dref,
    store_initialize, mkconfig, timestring, parsetime, traverse_dict, isrref,
    isdref, scanref_dict )

from tests.imports import ( given, text, isdir, isfile, join, from_regex,
    islink, get_executable, run, dictionaries, binary, one_of, integers,
    timegm, gmtime, settings, HealthCheck )

from tests.generators import (
    rrefs, drefs, configs, dicts, prims, dicts_with_refs )

from tests.setup import (
    ShouldHaveFailed, setup_testpath, setup_storage )


SHA256SUM=get_executable('sha256sum', 'Please install `sha256sum` tool from `coreutils` package')


@given(nsec=integers(min_value=0, max_value=timegm(gmtime())+10*365*24*60*60))
def test_timestring(nsec)->None:
  ts=timestring(nsec)
  st=parsetime(ts)
  ts2=timestring(st)
  assert ts==ts2

@given(dref=drefs())
def test_dref(dref):
  dref2=mkdref(*undref(dref))
  assert dref2==dref

@given(rref=rrefs())
def test_rref(rref):
  rref2=mkrref(*unrref(rref))
  assert rref2==rref
  dref=rref2dref(rref)
  assert_valid_dref(dref)


@given(cfg=configs())
def test_config(cfg):
  assert_valid_config(cfg)

def test_config2()->None:
  try:
    c = mkconfig({'a':(3,1)})
    raise ShouldHaveFailed(f'RConfig {c} is surprizingly valid')
  except AssertionError:
    pass

def test_setup_storage()->None:
  setup_storage('a')
  setup_storage('a')

def test_store_initialize()->None:
  p=setup_testpath('test_store_initialize')
  import pylightnix.core
  try:
    pylightnix.core.PYLIGHTNIX_TMP=join(p,'tmp')
    pylightnix.core.PYLIGHTNIX_STORE=join(p,'store')
    store_initialize(custom_store=None, custom_tmp=None)
    assert isdir(join(p,'tmp'))
    assert isdir(join(p,'store'))
    store_initialize(custom_store=None, custom_tmp=None)
    assert isdir(join(p,'tmp'))
    assert isdir(join(p,'store'))
  finally:
    pylightnix.core.PYLIGHTNIX_TMP=None #type:ignore
    pylightnix.core.PYLIGHTNIX_STORE=None #type:ignore



def test_mklogdir1()->None:
  path=setup_testpath('mklogdir1')
  logdir=mklogdir(tag='testtag',logrootdir=path)
  assert isdir(logdir)
  logdir=mklogdir(tag='testtag',logrootdir=path, subdirs=['a','b'])
  assert isdir(join(logdir,'a'))
  assert isdir(join(logdir,'b'))

@given(strtag=from_regex(r'[a-zA-Z0-9_:-]+', fullmatch=True),
       timetag=from_regex(r'[a-zA-Z0-9_:-]+', fullmatch=True))
def test_mklogdir2(strtag,timetag)->None:
  path=setup_testpath('mklogdir2')
  linkpath=join(path,f'_{strtag}_latest')
  logdir=mklogdir(tag=strtag,logrootdir=Path(path), timetag=timetag)
  open(join(logdir,'a'),'w').write('a')
  assert isdir(logdir)
  assert islink(linkpath)
  assert isfile(join(linkpath,'a'))
  logdir2=mklogdir(tag=strtag,logrootdir=Path(path), timetag=timetag+'2')
  open(join(logdir2,'b'),'w').write('b')
  assert isdir(logdir2)
  assert islink(linkpath)
  assert isfile(join(linkpath,'b'))

def test_dirhash()->None:
  path=setup_testpath('dirhash')
  h1=dirhash(path)
  assert_valid_hash(h1)
  with open(join(path,'_a'),'w') as f:
    f.write('1')
  h2=dirhash(path)
  assert_valid_hash(h2)
  assert h1==h2, "Test expected to ignore files starting with underscope"
  with open(join(path,'a'),'w') as f:
    f.write('1')
  h3=dirhash(path)
  assert_valid_hash(h3)
  assert h3 != h2

@given(b=binary())
def test_dirhash2(b)->None:
  path=setup_testpath('dirhash2')
  with open(join(path,'a'),'wb') as f:
    f.write(b)
  p=run([SHA256SUM, join(path,'a')], stdout=-1, check=True, cwd=path)
  h=dirhash(path)
  assert (p.stdout[:len(h)].decode('utf-8'))==h

@given(d=dicts())
def test_dirhash3(d)->None:
  path=setup_testpath('dirhash3')
  with open(join(path,'a'),'w') as f:
    f.write(str(d))
  p=run([SHA256SUM, join(path,'a')], stdout=-1, check=True, cwd=path)
  h=dirhash(path)
  assert (p.stdout[:len(h)].decode('utf-8'))==h


@given(d=dicts())
def test_traverse(d)->None:
  replacements=0
  def _mutator(k,x):
    nonlocal replacements
    if isinstance(x,str):
      replacements+=1
      dref=DRef("dref:11111111111111111111111111111111-00000000000000000000000000000000-bar")
      assert isdref(dref), 'Fix the test DRef if this fails'
      return dref
    else:
      return x
  traverse_dict(d,_mutator)
  drefs,rrefs=scanref_dict(d)
  assert len(rrefs)==0
  assert len(drefs)==replacements, f"{d}, {replacements}"



