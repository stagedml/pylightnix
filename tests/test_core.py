from pylightnix import (
    Config, instantiate, DRef, RRef, Path, mklogdir, dirhash,
    assert_valid_dref, assert_valid_rref, store_deps, store_deepdeps, store_gc,
    assert_valid_hash, assert_valid_config, Manager, mkcontext, store_realize,
    store_rrefs, mkdref, mkrref, unrref, undref, realize, rref2dref,
    store_config, mkconfig, Build, Context, build_outpath, only, mkdrv,
    store_deref, rref2path, store_rrefs_, config_cattrs, mksymlink,
    store_cattrs, build_deref, build_path, mkrefpath, build_config,
    store_drefs, store_rrefs, store_rrefs_, build_wrapper, recursion_manager,
    build_cattrs, build_name, largest, tryread, assert_recursion_manager_empty)

from tests.imports import ( given, Any, Callable, join, Optional, islink,
    isfile, List )

from tests.generators import (
    rrefs, drefs, configs, dicts )

from tests.setup import (
    ShouldHaveFailed, setup_testpath, setup_storage, mktestnode_nondetermenistic, mktestnode )


@given(d=dicts())
def test_realize(d)->None:
  with setup_storage('test_realize'):
    m=Manager()
    mktestnode(m, d)
    dref=list(m.builders.values())[-1].dref
    assert_valid_dref(dref)
    assert len(list(store_rrefs(dref, mkcontext()))) == 0
    rrefs=list(m.builders.values())[-1].matcher(dref, mkcontext())
    assert rrefs==[]
    rref=store_realize(dref, mkcontext(), list(m.builders.values())[-1].realizer(dref, mkcontext())[0])
    assert len(list(store_rrefs(dref, mkcontext()))) == 1
    assert_valid_rref(rref)
    rrefs2=list(m.builders.values())[-1].matcher(dref, mkcontext())
    rref2=rrefs2[0]
    assert rref==rref2


def test_realize_dependencies()->None:
  with setup_storage('test_realize_dependencies'):
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

    c=store_config(rref)
    assert_valid_config(c)
    cro=store_cattrs(rref)
    assert_valid_dref(getattr(cro,'n2'))
    assert_valid_dref(getattr(cro,'n3'))

    assert set(store_deps([n1])) == set([])
    assert set(store_deps([n2,n3])) == set([n1])
    assert set(store_deps([toplevel])) == set([n2,n3])

    assert store_deepdeps([n1]) == set([])
    assert store_deepdeps([n2,n3]) == set([n1])
    assert store_deepdeps([toplevel]) == set([n1,n2,n3])

def test_no_rref_deps()->None:
  with setup_storage('test_no_rref_deps'):
    try:
      rref=realize(instantiate(mktestnode,{'a':1}))
      clo=instantiate(mktestnode,{'a':1,'maman':rref})
      raise ShouldHaveFailed('rref deps are forbidden')
    except AssertionError:
      pass

def test_no_dref_deps_without_realizers()->None:
  with setup_storage('test_no_dref_deps_without_realizers'):
    try:
      clo=instantiate(mktestnode,{'a':1})
      rref=realize(instantiate(mktestnode,{'maman':clo.dref}))
      raise ShouldHaveFailed("We shouldn't share DRefs across managers")
    except AssertionError:
      pass

def test_repeated_instantiate()->None:
  with setup_storage('test_repeated_instantiate'):
    def _setting(m:Manager)->DRef:
      return mktestnode(m, {'a':'1'})

    cl1 = instantiate(_setting)
    cl2 = instantiate(_setting)
    assert len(cl1.derivations)==1
    assert len(cl2.derivations)==1
    assert cl1.derivations[0].dref == cl2.derivations[0].dref
    assert cl1.dref == cl2.dref


def test_repeated_realize()->None:
  with setup_storage('test_repeated_realize'):
    def _setting(m:Manager)->DRef:
      return mktestnode(m, {'a':'1'})
    rref1 = realize(instantiate(_setting))
    rref2 = realize(instantiate(_setting))
    rref3 = realize(instantiate(_setting), force_rebuild=[instantiate(_setting).dref])
    assert rref1==rref2 and rref2==rref3


def test_non_determenistic()->None:
  with setup_storage('test_non_determenistic'):
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

def test_no_recursive_realize()->None:
  with setup_storage('test_no_recursive_realize'):

    def _setup(m):
      rref1 = realize(instantiate(_setup))
      n2 = mktestnode(m,{'bogus':rref1})
      return n2

    try:
      rref = realize(instantiate(_setup))
      raise ShouldHaveFailed(f"Should fail, but got {rref}")
    except AssertionError:
      pass

def test_no_recursive_instantiate()->None:
  with setup_storage('test_no_recursive_instantiate'):

    def _setup(m):
      derivs = instantiate(_setup)
      n2 = mktestnode(m,{'bogus':derivs.dref})
      return n2

    try:
      rref = instantiate(_setup)
      raise ShouldHaveFailed(f"Should fail, but got {rref}")
    except AssertionError:
      pass

def test_recursion_manager()->None:
  try:
    with recursion_manager('foo'): pass
    raise ShouldHaveFailed(f"Should have failed")
  except AssertionError:
    pass

def test_config_ro():
  d={'a':1,'b':33}
  c=mkconfig(d)
  cro=config_cattrs(c)
  for k in d.keys():
    assert getattr(cro,k) == d[k]


def test_mksymlink()->None:
  with setup_storage('test_mksymlink'):
    tp=setup_testpath('test_mksymlink')

    def _setting1(m:Manager)->DRef:
      return mktestnode(m, {'a':'1'}, buildtime=False)
    def _setting2(m:Manager)->DRef:
      return mktestnode(m, {'a':'1'}, buildtime=True)

    clo=instantiate(_setting1)
    clo2=instantiate(_setting2)
    assert clo.dref==clo2.dref

    rref=realize(clo)
    s=mksymlink(rref, tgtpath=tp, name='thelink')
    assert islink(s)
    assert not isfile(join(s,'__buildtime__.txt'))
    assert tp in s

    rref2=realize(clo2, force_rebuild=[clo2.dref])
    s2=mksymlink(rref2, tgtpath=tp, name='thelink')
    assert islink(s2)
    assert isfile(join(s2,'__buildtime__.txt'))
    assert tp in s

    assert rref2==rref, "Should be (==), because configs are the same"
    assert s2!=s, "s2 should have timestamp"

    s3=mksymlink(rref2, tgtpath=tp, name='thelink', withtime=False)
    assert s3==s

def test_build_deref()->None:
  with setup_storage('test_build_deref'):

    def _depuser(m:Manager, sources:dict)->DRef:
      def _instantiate()->Config:
        return mkconfig(sources)
      def _realize(b)->None:
        o = build_outpath(b)
        c = build_cattrs(b)
        with open(join(o,'proof_papa'),'w') as f:
          f.write(str(build_deref(b, c.papa)))
        with open(join(o,'proof_maman'),'w') as d:
          with open(build_path(b, c.maman),'r') as s:
            d.write(s.read())
        return
      return mkdrv(m, _instantiate, only(), build_wrapper(_realize))

    def _setting(m:Manager)->DRef:
      n1 = mktestnode_nondetermenistic(m, {'a':'1'}, lambda : 42)
      n2 = mktestnode(m, {'b':'2'})
      n3 = _depuser(m, {'maman':mkrefpath(n1,['artifact']), 'papa':n2})
      return n3

    rref = realize(instantiate(_setting))
    assert_valid_rref(rref)

def test_build_cattrs():
  with setup_storage('test_build_cattrs'):
    def _setting(m:Manager)->DRef:
      def _instantiate()->Config:
        return mkconfig({'a':1,'b':2})
      def _realize(b)->None:
        c = build_cattrs(b)
        assert hasattr(c,'a')
        assert hasattr(c,'b')
        assert not hasattr(c,'c')
        c.c = 'foo'
        assert hasattr(c,'c')
        return
      return mkdrv(m, _instantiate, only(), build_wrapper(_realize))

    rref = realize(instantiate(_setting))
    assert_valid_rref(rref)

def test_ignored_stage()->None:
  with setup_storage('test_ignored_stage'):
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


def test_overwrite_realizer()->None:
  with setup_storage('test_overwrite_realizer'):
    n1:DRef; n2:DRef; n3:DRef; n4:DRef
    def _setting(m:Manager)->DRef:
      nonlocal n1, n2, n3, n4
      n1 = mktestnode_nondetermenistic(m, {'a':'1'}, lambda:33)
      n2 = mktestnode(m, {'maman':n1})
      n3 = mktestnode_nondetermenistic(m, {'a':'1'}, lambda:42)
      assert n1 == n3
      return n2

    rref_n2=realize(instantiate(_setting))
    all_drefs = list(store_drefs())
    assert len(all_drefs)==2

    rref_n3=store_deref(rref_n2, store_cattrs(rref_n2).maman)
    assert open(join(rref2path(rref_n3),'artifact'),'r').read() == '42'

def test_only()->None:
  with setup_storage('test_only'):

    build:int = 0
    def _setting(m:Manager)->DRef:
      def _instantiate()->Config:
        return mkconfig({'a':1})
      def _realize(b:Build)->None:
        nonlocal build
        with open(join(build_outpath(b),'artifact'),'w') as f: f.write(str(build))
        build+=1
      return mkdrv(m, _instantiate, only(), build_wrapper(_realize))

    closure = instantiate(_setting)
    assert len(list(store_rrefs_(closure.dref))) == 0
    rref = realize(closure)
    assert len(list(store_rrefs_(closure.dref))) == 1
    rref = realize(closure)
    assert len(list(store_rrefs_(closure.dref))) == 1
    try:
      rref = realize(closure, force_rebuild=[closure.dref])
      raise ShouldHaveFailed('Should have failed in only assertion')
    except AssertionError as e:
      pass
    assert len(list(store_rrefs_(closure.dref))) == 2

def test_build_name()->None:
  with setup_storage('test_build_name'):
    n:str = ""
    def _setting(m:Manager)->DRef:
      def _instantiate()->Config:
        return mkconfig({'name':'foobar'})
      def _realize(b)->None:
        nonlocal n
        n = build_name(b)
      return mkdrv(m, _instantiate, only(), build_wrapper(_realize))

    rref=realize(instantiate(_setting))
    assert n=='foobar'


def test_largest()->None:
  with setup_storage('test_largest'):

    fname:str='score'
    score:str='0'
    def _mklrg(m, cfg):
      def _instantiate()->Config:
        return mkconfig(cfg)
      def _realize(b:Build)->None:
        nonlocal score, fname
        with open(join(build_outpath(b),fname),'w') as f:
          f.write(score)
      return mkdrv(m, _instantiate, largest('score'), build_wrapper(_realize))

    clo1=instantiate(_mklrg, {'a':1})

    score='0'
    rref1a=realize(clo1)
    assert isfile(join(rref2path(rref1a),'score'))
    assert len(list(store_rrefs_(clo1.dref))) == 1
    assert tryread(Path(join(rref2path(rref1a),'score')))=='0'
    score='non-integer'
    rref1b=realize(clo1, force_rebuild=[clo1.dref])
    assert isfile(join(rref2path(rref1b),'score'))
    assert len(list(store_rrefs_(clo1.dref))) == 2
    assert tryread(Path(join(rref2path(rref1b),'score')))=='non-integer'
    score='1'
    rref1c=realize(clo1, force_rebuild=[clo1.dref])
    assert isfile(join(rref2path(rref1c),'score'))
    assert len(list(store_rrefs_(clo1.dref))) == 3
    assert tryread(Path(join(rref2path(rref1c),'score')))=='1'
    score='100500'
    fname='baz'
    rref1d=realize(clo1, force_rebuild=[clo1.dref])
    assert not isfile(join(rref2path(rref1d),'score'))
    assert len(list(store_rrefs_(clo1.dref))) == 4

    rref1=realize(clo1)
    assert isfile(join(rref2path(rref1),'score'))
    assert tryread(Path(join(rref2path(rref1),'score')))=='1'


def test_minimal_closure():
  with setup_storage('test_minimal_closure'):

    def _somenode(m):
      return mktestnode(m,{'a':0})

    def _anothernode(m):
      n1=mktestnode(m,{'a':1})
      n2=_somenode(m)
      n3=mktestnode(m,{'maman':n1,'papa':n2})
      return n3

    assert_recursion_manager_empty()

    rref1=realize(instantiate(_somenode))
    rref=realize(instantiate(_anothernode))
    rref2=store_deref(rref,store_cattrs(rref).papa)
    assert rref1==rref2

