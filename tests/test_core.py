from pylightnix import (
    Config, instantiate, DRef, RRef, Path, mklogdir, dirhash,
    assert_valid_dref, assert_valid_rref, store_deps, store_deepdeps,
    store_gc, assert_valid_hash, assert_valid_config, Manager, mkcontext,
    build_realize, store_rrefs, mkdref, mkrref, unrref, undref, realize,
    rref2dref, store_config, mkconfig, mkbuild, Build, Context, build_outpath,
    only, mkdrv, store_deref, store_rref2path, store_rrefs_, config_ro,
    mksymlink, store_config_ro, build_deref, build_deref_path, mkrefpath,
    build_config, store_drefs, store_rrefs, store_rrefs_)

from tests.imports import ( given, Any, Callable, join, Optional, islink, List )

from tests.generators import (
    rrefs, drefs, configs, dicts )

from tests.setup import (
    setup_testpath, setup_storage, mktestnode_nondetermenistic, mktestnode )


@given(d=dicts())
def test_realize(d)->None:
  setup_storage('test_realize')
  m=Manager()
  mktestnode(m, d)
  dref=list(m.builders.values())[-1].dref
  assert_valid_dref(dref)
  assert len(list(store_rrefs(dref, mkcontext()))) == 0
  rref=list(m.builders.values())[-1].matcher(dref, mkcontext())
  assert rref is None
  rref=build_realize(dref, mkcontext(), list(m.builders.values())[-1].realizer(dref, mkcontext()))
  assert len(list(store_rrefs(dref, mkcontext()))) == 1
  assert_valid_rref(rref)
  rref2=list(m.builders.values())[-1].matcher(dref, mkcontext())
  assert rref==rref2


def test_realize_dependencies()->None:
  setup_storage('test_realize_dependencies')
  n1=None; n2=None; n3=None; toplevel=None

  def _setup(m):
    nonlocal n1,n2,n3,toplevel
    n1=mktestnode(m, {'a':1})
    n2=mktestnode(m, {'parent1':n1})
    n3=mktestnode(m, {'parent2':n1})
    toplevel=mktestnode(m, {'n2':n2,'n3':n3})
    return toplevel

  rref=realize(instantiate(_setup))
  assert_valid_rref(rref)
  assert n1 is not None
  assert n2 is not None
  assert n3 is not None
  assert toplevel is not None

  c=store_config(rref2dref(rref))
  assert_valid_config(c)
  cro=store_config_ro(rref2dref(rref))
  assert_valid_dref(getattr(cro,'n2'))
  assert_valid_dref(getattr(cro,'n3'))

  assert set(store_deps([n1])) == set([])
  assert set(store_deps([n2,n3])) == set([n1])
  assert set(store_deps([toplevel])) == set([n2,n3])

  assert store_deepdeps([n1]) == set([])
  assert store_deepdeps([n2,n3]) == set([n1])
  assert store_deepdeps([toplevel]) == set([n1,n2,n3])

def test_repeated_instantiate()->None:
  setup_storage('test_repeated_instantiate')

  def _setting(m:Manager)->DRef:
    return mktestnode(m, {'a':'1'})

  cl1 = instantiate(_setting)
  cl2 = instantiate(_setting)
  assert len(cl1.derivations)==1
  assert len(cl2.derivations)==1
  assert cl1.derivations[0].dref == cl2.derivations[0].dref
  assert cl1.dref == cl2.dref


def test_repeated_realize()->None:
  setup_storage('test_repeated_realize')

  def _setting(m:Manager)->DRef:
    return mktestnode(m, {'a':'1'})

  rref1 = realize(instantiate(_setting))
  rref2 = realize(instantiate(_setting))
  rref3 = realize(instantiate(_setting), force_rebuild=[instantiate(_setting).dref])
  assert rref1==rref2 and rref2==rref3


def test_non_determenistic()->None:
  setup_storage('test_non_determenistic')

  DATA:int; n1:DRef; n2:DRef; n3:DRef

  def _gen()->int:
    nonlocal DATA
    return DATA

  def _setup(m):
    nonlocal n1, n2, n3
    n1 = mktestnode(m, {'a':'1'})
    n2 = mktestnode_nondetermenistic(m,{'maman':n1},_gen)
    n3 = mktestnode(m,{'papa':n2})
    return n3

  DATA = 1
  rref1 = realize(instantiate(_setup))
  DATA = 2
  rref2 = realize(instantiate(_setup), force_rebuild=[n2])

  assert len(list(store_rrefs_(n1))) == 1
  assert len(list(store_rrefs_(n2))) == 2
  assert len(list(store_rrefs_(n3))) == 2
  assert rref1 != rref2

  n2_rref1 = store_deref(rref1, n2)
  n2_rref2 = store_deref(rref2, n2)
  assert n2_rref1 != n2_rref2


def test_no_multi_realizers()->None:
  d={'a':1}
  setup_storage('test_no_multi_realizers')

  def _gen()->int:
    return 42

  def _setup(m):
    n1 = mktestnode_nondetermenistic(m,d,_gen)
    n2 = mktestnode_nondetermenistic(m,d,_gen)
    return n2

  try:
    rref = instantiate(_setup)
    assert False, f"Should fail, but got {rref}"
  except AssertionError:
    pass

def test_no_recursive_realize()->None:
  setup_storage('test_no_recursive_realize')

  def _setup(m):
    rref1 = realize(instantiate(_setup))
    n2 = mktestnode(m,{'bogus':rref1})
    return n2

  try:
    rref = realize(instantiate(_setup))
    assert False, f"Should fail, but got {rref}"
  except AssertionError:
    pass

def test_no_recursive_instantiate()->None:
  setup_storage('test_no_recursive_instantiate')

  def _setup(m):
    derivs = instantiate(_setup)
    n2 = mktestnode(m,{'bogus':derivs.dref})
    return n2

  try:
    rref = instantiate(_setup)
    assert False, f"Should fail, but got {rref}"
  except AssertionError:
    pass

def test_config_ro():
  d={'a':1,'b':33}
  c=mkconfig(d)
  cro=config_ro(c)
  for k in d.keys():
    assert getattr(cro,k) == d[k]


def test_mksymlink():
  setup_storage('test_mksymlink')
  tp=setup_testpath('test_mksymlink')

  def _setting(m:Manager)->DRef:
    return mktestnode(m, {'a':'1'})

  rref=realize(instantiate(_setting))
  s=mksymlink(rref, tgtpath=tp, name='thelink')
  assert islink(s)
  assert tp in s

def test_build_deref():
  setup_storage('test_build_deref')

  def _depuser(m:Manager, sources:dict)->DRef:
    def _instantiate()->Config:
      return mkconfig(sources)
    def _realize(dref:DRef, context:Context)->Path:
      b = mkbuild(dref, context)
      o = build_outpath(b)
      c = config_ro(build_config(b))
      with open(join(o,'proof_papa'),'w') as f:
        f.write(str(build_deref(b, c.papa)))
      with open(join(o,'proof_maman'),'w') as d:
        with open(build_deref_path(b, c.maman),'r') as s:
          d.write(s.read())
      return o
    return mkdrv(m, _instantiate, only, _realize)

  def _setting(m:Manager)->DRef:
    n1 = mktestnode_nondetermenistic(m, {'a':'1'}, lambda : 42)
    n2 = mktestnode(m, {'b':'2'})
    n3 = _depuser(m, {'maman':mkrefpath(n1,['nondet']), 'papa':n2})
    return n3

  rref = realize(instantiate(_setting))
  assert_valid_rref(rref)


def test_ignored_stage():
  setup_storage('test_ignored_stage')
  n1:DRef; n2:DRef; n3:DRef; n4:DRef
  def _setting(m:Manager)->DRef:
    nonlocal n1, n2, n3, n4
    n1 = mktestnode(m, {'a':'1'})
    n2 = mktestnode(m, {'b':'2'}) # this one should not be realized
    n3 = mktestnode(m, {'c':'3', 'maman':n1})
    n4 = mktestnode(m, {'c':'4', 'papa':n3}) # neither this one
    return n3

  cl=instantiate(_setting)
  rref = realize(cl)
  rrefs:List[RRef] = []
  all_drefs = list(store_drefs())
  assert len(all_drefs)==4
  assert len(list(store_rrefs_(n1)))==1
  assert len(list(store_rrefs_(n2)))==0
  assert len(list(store_rrefs_(n3)))==1
  assert len(list(store_rrefs_(n4)))==0



