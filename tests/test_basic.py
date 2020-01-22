from pylightnix import (
    instantiate, DRef, RRef, Path, mklogdir, dirhash, assert_valid_dref,
    assert_valid_rref, mknode, store_deps, store_deepdeps, store_gc,
    assert_valid_hash, assert_valid_config, Manager, mkcontext,
    store_rrefs, mkdref, mkrref, unrref, undref, realize, rref2dref )

from tests.imports import (
    given, text, isdir, join, from_regex, islink, get_executable, run,
    dictionaries, binary, one_of, integers )

from tests.generators import (
    rrefs, drefs, configs, dicts, prims )

from tests.setup import (
    setup_testpath, setup_storage )


SHA256SUM=get_executable('sha256sum', 'Please install `sha256sum` tool from `coreutils` package')


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

def test_setup_storage()->None:
  setup_storage('a')
  setup_storage('a')

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

