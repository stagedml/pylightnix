from pylightnix import ( instantiate, DRef, RRef, Path, mklogdir,
    dirhash, assert_valid_dref, assert_valid_rref, store_deps, store_deepdeps,
    store_gc, assert_valid_hash, assert_valid_config, Manager, mkcontext,
    store_realize, store_rrefs, mkdref, mkrref, unrref, undref, realize,
    rref2dref, store_config, mkconfig, Build, Context, build_outpath,
    match_only, mkdrv, store_deref, rref2path, store_rrefs_, config_cattrs,
    mksymlink, store_cattrs, build_deref, build_path, mkrefpath, build_config,
    store_drefs, store_rrefs, store_rrefs_, build_wrapper, recursion_manager,
    build_cattrs, build_name, match_best, tryread, trywrite,
    assert_recursion_manager_empty, match, latest, best, exact, Key,
    match_latest, match_all, match_some, match_n, realizeMany, build_outpaths,
    scanref_dict, config_dict, promise, checkpaths, mklens, isrref, Config,
    RConfig, build_setoutpaths, partial, path2rref )

from tests.imports import ( given, Any, Callable, join, Optional, islink,
    isfile, List, randint, sleep, rmtree, system, S_IWRITE, S_IREAD, S_IEXEC,
    chmod, Popen, PIPE )

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
    assert rrefs is None
    rref=store_realize(dref, mkcontext(), list(m.builders.values())[-1].realizer(dref, mkcontext(),{})[0])
    assert len(list(store_rrefs(dref, mkcontext()))) == 1
    assert_valid_rref(rref)
    rrefs2=list(m.builders.values())[-1].matcher(dref, mkcontext())
    assert rrefs2 is not None
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

def test_detect_rref_deps()->None:
  with setup_storage('test_detect_rref_deps'):
    rref=realize(instantiate(mktestnode,{'a':1}))
    clo=instantiate(mktestnode,{'a':1,'maman':rref})
    _,rrefs=scanref_dict(config_dict(store_config(clo.dref)))
    assert len(rrefs)>0

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
    dref=instantiate(_setting)
    rref1=realize(dref)
    rref2=realize(dref)
    rref3=realize(dref, force_rebuild=[instantiate(_setting).dref])
    assert rref1==rref2 and rref2==rref3
    try:
      rref3=realize(dref, force_rebuild='Foobar') # type:ignore
      raise ShouldHaveFailed
    except AssertionError:
      pass

def test_realize_readonly()->None:
  with setup_storage('test_realize_readonly'):
    rref1 = realize(instantiate(mktestnode, {'a':'1'}))

    try:
      with open(join(rref2path(rref1),'newfile'),'w') as f:
        f.write('foo')
      raise ShouldHaveFailed('No write-protection??')
    except OSError as err:
      pass

    try:
      rmtree(rref2path(rref1))
      raise ShouldHaveFailed('No remove-protection??')
    except OSError as err:
      pass

    def _realize(b:Build):
      with open(join(build_outpath(b),'exe'),'w') as f:
        f.write('#!/bin/sh\necho "Fooo"')
      chmod(join(build_outpath(b),'exe'), S_IWRITE|S_IREAD|S_IEXEC)
    rref2=realize(instantiate(mkdrv, Config({}),
                              match_only(), build_wrapper(_realize)))
    assert Popen([join(rref2path(rref2),'exe')],
        stdout=PIPE).stdout.read()=='Fooo\n'.encode('utf-8'), \
        "Did we lost exec permission?"


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
    assert rref1==rref2, '''
      Nodes with no dependencies should have empty context, regardless of their
      position in the closure.
      '''

def test_realize_nondetermenistic()->None:
  with setup_storage('test_realize_nondetermenistic'):
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
  cro=config_cattrs(RConfig(config_dict(c))) # We sure we don't have promises here
  for k in d.keys():
    assert getattr(cro,k) == d[k]


def test_mksymlink()->None:
  with setup_storage('test_mksymlink'):
    tp=setup_testpath('test_mksymlink')
    print(tp)

    def _setting1(m:Manager)->DRef:
      return mktestnode_nondetermenistic(m, {'a':'1'}, lambda: 33, buildtime=False)
    def _setting2(m:Manager)->DRef:
      return mktestnode_nondetermenistic(m, {'a':'1'}, lambda: 42, buildtime=True)

    clo=instantiate(_setting1)
    rref=realize(clo)

    clo2=instantiate(_setting2)
    rref2=realize(clo2, force_rebuild=True)

    assert clo.dref==clo2.dref
    assert rref2!=rref

    s=mksymlink(rref, tgtpath=tp, name='thelink')
    assert islink(s)
    assert not isfile(join(s,'__buildtime__.txt'))
    assert tp in s

    s2=mksymlink(rref2, tgtpath=tp, name='thelink')
    assert islink(s2)
    assert isfile(join(s2,'__buildtime__.txt'))
    assert tp in s

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
      return mkdrv(m, _instantiate(), match_only(), build_wrapper(_realize))

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
        o = build_outpath(b)
        assert hasattr(c,'a')
        assert hasattr(c,'b')
        assert not hasattr(c,'c')
        c.c = 'foo'
        c2 = build_cattrs(b) # Should use the cache
        assert hasattr(c2,'c')
        return
      return mkdrv(m, _instantiate(), match_only(), build_wrapper(_realize))

    rref = realize(instantiate(_setting))
    assert_valid_rref(rref)

def test_build_name()->None:
  with setup_storage('test_build_name'):
    def _setting(m:Manager)->DRef:
      def _realize(b)->None:
        n=build_name(b)
        assert n=='foobar'
        o=build_outpath(b)
      return mkdrv(m, mkconfig({'name':'foobar'}), match_only(), build_wrapper(_realize))
    rref=realize(instantiate(_setting))
    assert isrref(rref)
    assert 'foobar' in rref

def test_build_exception()->None:
  with setup_storage('test_build_name'):
    def _setting(m:Manager)->DRef:
      def _realize(b)->None:
        raise ValueError('Oops')
      return mkdrv(m, mkconfig({}), match_only(), build_wrapper(_realize))
    try:
      rref=realize(instantiate(_setting))
      raise ShouldHaveFailed()
    except ValueError as e:
      assert 'Oops' in str(e)

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

def test_match_only()->None:
  with setup_storage('test_match_only'):

    build:int = 0
    def _setting(m:Manager)->DRef:
      def _realize(b:Build)->None:
        nonlocal build
        with open(join(build_outpath(b),'artifact'),'w') as f: f.write(str(build))
        build+=1
      return mkdrv(m, mkconfig({'a':1}), match_only(), build_wrapper(_realize))

    closure = instantiate(_setting)
    assert len(list(store_rrefs_(closure.dref))) == 0
    rref = realize(closure)
    assert len(list(store_rrefs_(closure.dref))) == 1
    rref = realize(closure)
    assert len(list(store_rrefs_(closure.dref))) == 1
    try:
      rref = realize(closure, force_rebuild=[closure.dref])
      raise ShouldHaveFailed('Should have failed in match_only assertion')
    except AssertionError as e:
      pass
    assert len(list(store_rrefs_(closure.dref))) == 2


def test_match_best()->None:
  with setup_storage('test_match_best'):
    fname:str='score'
    score:str='0'
    def _mklrg(m, cfg, matcher):
      def _instantiate()->Config:
        return mkconfig(cfg)
      def _realize(b:Build)->None:
        nonlocal score, fname, matcher
        with open(join(build_outpath(b),fname),'w') as f:
          f.write(score)
      return mkdrv(m, _instantiate(), matcher, build_wrapper(_realize))

    clo1=instantiate(_mklrg, {'a':1}, matcher=match_best('score'))
    score='0'
    rref1a=realize(clo1)
    assert isfile(join(rref2path(rref1a),'score'))
    assert len(list(store_rrefs_(clo1.dref))) == 1
    assert tryread(Path(join(rref2path(rref1a),'score')))=='0'
    score='non-integer'
    rref1b=realize(clo1, force_rebuild=[clo1.dref])
    assert isfile(join(rref2path(rref1b),'score'))
    assert len(list(store_rrefs_(clo1.dref))) == 2
    assert tryread(Path(join(rref2path(rref1b),'score')))=='0'
    score='1'
    rref1c=realize(clo1, force_rebuild=[clo1.dref])
    assert isfile(join(rref2path(rref1c),'score'))
    assert len(list(store_rrefs_(clo1.dref))) == 3
    assert tryread(Path(join(rref2path(rref1c),'score')))=='1'
    score='100500'
    fname='baz'
    rref1d=realize(clo1, force_rebuild=[clo1.dref])
    assert not isfile(join(rref2path(rref1d),'baz'))
    assert len(list(store_rrefs_(clo1.dref))) == 4

    clo1=instantiate(_mklrg, {'a':1},
      matcher=match([exact([
        RRef('rref:64617f2a2a9446340241b071413f6f68-a76762e9bc54e47c09455bdb226e2388-unnamed')])]))
    rref1e=realize(clo1)
    assert isfile(join(rref2path(rref1e),'baz'))
    assert len(list(store_rrefs_(clo1.dref))) == 4

    clo1=instantiate(_mklrg, {'a':1}, matcher=match_best('score'))
    rref1=realize(clo1)
    assert isfile(join(rref2path(rref1),'score'))
    assert tryread(Path(join(rref2path(rref1),'score')))=='1'


def test_match_latest():
  def _mknode(m, cfg, matcher, nouts:int, data=0, buildtime=True):
    def _realize(b:Build)->None:
      build_setoutpaths(b,nouts)
      for i,out in enumerate(build_outpaths(b)):
        assert trywrite(Path(join(out,'artifact')),str(data)+'_'+str(i))
    return mkdrv(m, Config(cfg), matcher,
                    build_wrapper(_realize, buildtime=buildtime))

  with setup_storage('test_match_latest'):
    clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=1)
    rref1=realize(clo)
    assert len(list(store_rrefs_(clo.dref)))==1
    sleep(0.01)
    clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=2)
    rref2=realize(clo, force_rebuild=[clo.dref])
    assert len(list(store_rrefs_(clo.dref)))==2
    assert tryread(Path(join(rref2path(rref2),'artifact')))==str('2_0')

  with setup_storage('test_match_latest'):
    clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=1)
    rref1=realize(clo)
    assert len(list(store_rrefs_(clo.dref)))==1
    sleep(0.01)
    clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=2, buildtime=False)
    rref2=realize(clo, force_rebuild=[clo.dref])
    assert len(list(store_rrefs_(clo.dref)))==2
    assert tryread(Path(join(rref2path(rref2),'artifact')))==str('1_0')

  for i in range(10):
    with setup_storage('test_match_latest'):
      nouts=randint(1,10)
      ntop=randint(1,10)
      try:
        clo=instantiate(_mknode, {'a':0}, match_latest(ntop), nouts)
        rrefs=realizeMany(clo)
        times=set([tryread(Path(join(rref2path(rref),'__buildtime__.txt'))) for rref in rrefs])
        assert len(list(times))==1
      except AssertionError:
        assert ntop>nouts


def test_match_all():
  """ match_all() should match all the references """
  def _mknode(m,cfg, matcher, nouts:int):
    def _realize(b:Build)->None:
      build_setoutpaths(b,nouts)
      for i,out in enumerate(build_outpaths(b)):
        assert trywrite(Path(join(out,'artifact')),str(nouts+i))
    return mkdrv(m, Config(cfg), matcher, build_wrapper(_realize))

  with setup_storage('test_match_all_empty'):
    clo=instantiate(_mknode, {'a':1}, match_all(), 5)
    rrefs=realizeMany(clo)
    assert len(rrefs)==0

  for i in range(10):
    data=randint(1,10)
    nouts=randint(1,10)
    with setup_storage('test_match_all'):
      clo=instantiate(_mknode, {'a':data}, match_n(1), nouts)
      rrefs_1=realizeMany(clo)
      assert len(rrefs_1)==1
      clo=instantiate(_mknode, {'a':data}, match_all(), nouts)
      rrefs_all=realizeMany(clo)
      assert len(rrefs_all)==nouts

def test_match_some():
  with setup_storage('test_match_some'):
    def _mknode(m, cfg, nouts:int, top:int):
      def _realize(b:Build)->None:
        build_setoutpaths(b,nouts)
        for i,out in enumerate(build_outpaths(b)):
          assert trywrite(Path(join(out,'artifact')),str(nouts+i))
      return mkdrv(m, mkconfig(cfg), match_some(n=top), build_wrapper(_realize))

    for i in range(10):
      nouts=randint(1,10)
      top=randint(1,10)
      clo=instantiate(_mknode, {'a':randint(0,1000)}, nouts, top)
      try:
        rrefs=realizeMany(clo, force_rebuild=[clo.dref])
        assert top<=nouts
      except AssertionError:
        assert top>nouts


def test_gc():
  with setup_storage('test_gc'):
    def _node1(m:Manager)->DRef:
      return mktestnode(m, {'name':'1'})
    def _node2(m:Manager)->DRef:
      return mktestnode(m, {'name':'2', 'maman':_node1(m)})
    def _node3(m:Manager)->DRef:
      return mktestnode(m, {'name':'3', 'maman':_node1(m)})

    r1=realize(instantiate(_node1))
    r2=realize(instantiate(_node2))
    r3=realize(instantiate(_node3))

    rm_drefs,rm_rrefs=store_gc([],[r2])
    assert rm_drefs=={rref2dref(r) for r in [r3]}
    assert rm_rrefs=={x for x in [r3]}

def test_promise():
  with setup_storage('test_promise'):
    def _setting(m:Manager, fullfill:bool)->DRef:
      n1=mktestnode(m, {'name':'1', 'promise':[promise,'artifact']})
      def _realize(b:Build):
        o=build_outpath(b)
        c=build_cattrs(b)
        assert b.dref in c.promise
        assert n1 in store_cattrs(c.maman).promise
        assert build_path(b,c.promise)==join(o,'uber-artifact')
        assert build_path(b,store_cattrs(c.maman).promise)==build_path(b,c.maman_promise)
        if fullfill:
          with open(build_path(b,c.promise),'w') as f:
            f.write('chickenpoop')

      return mkdrv(m, mkconfig({'name':'2', 'maman':n1,
                                'promise':[promise,'uber-artifact'],
                                'maman_promise':[n1,'artifact']}),
                      matcher=match_only(),
                      realizer=build_wrapper(_realize))

    try:
      rref=realize(instantiate(_setting,False))
      raise ShouldHaveFailed('Promise trigger')
    except AssertionError:
      pass
    rref=realize(instantiate(_setting,True))
    assert_valid_rref(rref)


def test_checkfiles():
  with setup_storage('test_checkfiles'):

    def _setting(m:Manager)->DRef:
      n1=mktestnode(m, {'name':'1', 'promise':[promise,'artifact']})
      n2=mktestnode(m, {'name':'2', 'promise':[promise,'artifact']})
      n3=checkpaths(m, {'f1':mklens(n1).promise.refpath,
                        'f2':mklens(n2).promise.refpath})
      return n3

    rrefs=realizeMany(instantiate(_setting))
    assert len(rrefs)==2

def test_path2rref():
  with setup_storage('test_path2rref') as s:
    s1=partial(mktestnode, sources={'name':'1', 'promise':[promise,'artifact']})
    rref1=realize(instantiate(s1))
    rref2=path2rref(rref2path(rref1))
    assert rref1==rref2
    l=mksymlink(rref1, s, 'result')
    assert path2rref(Path(l))==rref1
    rref3=path2rref(Path("/foo/00000000000000000000000000000000-bar/11111111111111111111111111111111"))
    assert rref3=='rref:11111111111111111111111111111111-00000000000000000000000000000000-bar'
    for x in [path2rref(Path('')),path2rref(Path('foo'))]:
      assert x is None



