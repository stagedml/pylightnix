from pylightnix import (
    Config, instantiate, DRef, RRef, Path, mklogdir, dirhash,
    assert_valid_dref, assert_valid_rref, mknode, store_deps, store_deepdeps,
    store_gc, assert_valid_hash, assert_valid_config, Manager, mkclosure,
    build_realize, store_rrefs, mkdref, mkrref, unrref, undref, realize,
    rref2dref, store_config, mkconfig, mkbuild, Build, Closure, build_outpath,
    only, manage, store_deref, store_rref2path )

from tests.imports import ( given, Any, Callable, join, Optional )

from tests.generators import (
    rrefs, drefs, configs, dicts )

from tests.setup import (
    setup_testpath, setup_storage )


@given(d=dicts())
def test_realize(d)->None:
  setup_storage('test_realize')
  m=Manager()
  mknode(m, d)
  dref=m.builders[-1].dref
  assert_valid_dref(dref)
  assert len(list(store_rrefs(dref))) == 0
  rref=m.builders[-1].matcher(dref, mkclosure())
  assert rref is None
  rref=build_realize(dref, m.builders[-1].realizer(dref, mkclosure()))
  assert len(list(store_rrefs(dref))) == 1
  assert_valid_rref(rref)
  rref2=m.builders[-1].matcher(dref, mkclosure())
  assert rref==rref2


@given(d=dicts())
def test_realize_dependencies(d)->None:
  setup_storage('test_realize_dependencies')
  n1=None; n2=None; n3=None; toplevel=None

  def _setup(m):
    nonlocal n1,n2,n3,toplevel
    n1=mknode(m, d)
    n2=mknode(m, {'parent1':n1})
    n3=mknode(m, {'parent2':n1})
    toplevel=mknode(m, {'n2':n2,'n3':n3})
    return toplevel

  rref=realize(_setup)
  assert_valid_rref(rref)
  assert n1 is not None
  assert n2 is not None
  assert n3 is not None
  assert toplevel is not None

  c=store_config(rref2dref(rref))
  assert_valid_config(c)

  assert set(store_deps([n1])) == set([])
  assert set(store_deps([n2,n3])) == set([n1])
  assert set(store_deps([toplevel])) == set([n2,n3])

  assert set(store_deepdeps([n1])) == set([])
  assert set(store_deepdeps([n2,n3])) == set([n1])
  assert set(store_deepdeps([toplevel])) == set([n1,n2,n3])



def mknode_nondetermenistic(m:Manager, sources:dict, nondet:Callable[[],int])->DRef:
  """ Emulate non-determenistic builds. `nondet` is expected to return
  different values from build to build """
  def _instantiate()->Config:
    return mkconfig(sources)
  def _realize(dref:DRef, closure:Closure)->Build:
    b=mkbuild(dref, closure)
    with open(join(build_outpath(b),'nondet'),'w') as f:
      f.write(str(nondet()))
    return b
  def _match(dref:DRef, closure:Closure)->Optional[RRef]:
    max_i=0
    max_rref=None
    for rref in store_rrefs(dref):
      with open(join(store_rref2path(rref),'nondet'),'r') as f:
        i=int(f.read())
        if i>max_i:
          max_i=i
          max_rref=rref
    return max_rref

  return manage(m, _instantiate, _match, _realize)


@given(d=dicts())
def test_non_determenistic(d)->None:
  setup_storage('test_non_determenistic')

  DATA:int; n1:DRef; n2:DRef; n3:DRef

  def _gen()->int:
    nonlocal DATA
    return DATA

  def _setup(m):
    nonlocal n1, n2, n3
    n1 = mknode(m,d)
    n2 = mknode_nondetermenistic(m,{'maman':n1},_gen)
    n3 = mknode(m,{'papa':n2})
    return n3

  DATA = 1
  rref1 = realize(_setup)
  DATA = 2
  rref2 = realize(_setup, force_rebuild=[n2])

  assert len(list(store_rrefs(n1))) == 1
  assert len(list(store_rrefs(n2))) == 2
  assert len(list(store_rrefs(n3))) == 2
  assert rref1 != rref2

  n2_rref1 = store_deref(rref1, n2)
  n2_rref2 = store_deref(rref2, n2)
  assert n2_rref1 != n2_rref2


@given(d=dicts())
def test_no_multi_realizeirs(d)->None:
  setup_storage('test_no_multi_realizers')

  def _gen()->int:
    return 42

  def _setup(m):
    n1 = mknode_nondetermenistic(m,d,_gen)
    n2 = mknode_nondetermenistic(m,d,_gen)
    return n2

  try:
    rref = instantiate(_setup)
    assert False, f"Should fail, but got {rref}"
  except AssertionError:
    pass

