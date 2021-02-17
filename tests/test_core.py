from pylightnix import (instantiate, DRef, RRef, Path, SPath, mklogdir,
                        dirhash, assert_valid_dref, assert_valid_rref,
                        store_deps, store_deepdeps, store_gc,
                        assert_valid_hash, assert_valid_config, Manager,
                        mkcontext, store_realize_group, store_rrefs, mkdref,
                        mkrref, unrref, undref, realize, rref2dref,
                        store_config, mkconfig, Build, Context, build_outpath,
                        match_only, mkdrv, store_deref, store_rref2path,
                        store_rrefs_, config_cattrs, mksymlink, store_cattrs,
                        build_deref, build_path, mkrefpath, build_config,
                        alldrefs, store_rrefs, build_wrapper, build_cattrs,
                        build_name, match_best, tryread, trywrite, match,
                        latest, best, exact, Key, match_latest, match_all,
                        match_some, match_n, realizeMany, build_outpaths,
                        scanref_dict, config_dict, promise, mklens, isrref,
                        Config, RConfig, build_setoutpaths, partial, path2rref,
                        Tag, Group, RRefGroup, concat, linkrrefs, instantiate_,
                        store_dref2path, path2dref, linkdref, storage,
                        dref2rrefs)

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, islink, List, randint, sleep, rmtree, system,
                           S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen, PIPE)

from tests.generators import (
    rrefs, drefs, configs, dicts )

from tests.setup import ( ShouldHaveFailed, setup_testpath, setup_storage,
                         setup_storage2, mktestnode_nondetermenistic,
                         mktestnode, pipe_stdout )


@given(d=dicts())
def test_realize_base(d)->None:
  with setup_storage2('test_realize_base') as S:
    m=Manager(storage(S))
    mktestnode(m, d)
    dref=list(m.builders.values())[-1].dref
    assert_valid_dref(dref)
    assert len(list(store_rrefs(dref, mkcontext(), S))) == 0
    rrefgs=list(m.builders.values())[-1].matcher(S, dref, mkcontext())
    assert rrefgs is None
    rrefg=store_realize_group(dref, mkcontext(),
        list(m.builders.values())[-1].realizer(S, dref, mkcontext(),{})[0], S)
    assert len(list(store_rrefs(dref, mkcontext(), S))) == 1
    assert_valid_rref(rrefg[Tag('out')])
    rrefgs2=list(m.builders.values())[-1].matcher(S, dref, mkcontext())
    assert rrefgs2 is not None
    rrefg2=rrefgs2[0]
    assert rrefg==rrefg2


def test_realize_dependencies()->None:
  with setup_storage2('test_realize_dependencies') as S:
    n1=None; n2=None; n3=None; toplevel=None

    def _setup(m):
      nonlocal n1,n2,n3,toplevel
      n1=mktestnode(m, {'a':1})
      n2=mktestnode(m, {'parent1':n1})
      n3=mktestnode(m, {'parent2':n1})
      toplevel=mktestnode(m, {'n2':n2,'n3':n3})
      return toplevel

    rref=realize(instantiate(_setup,S=S))
    assert_valid_rref(rref)
    assert n1 is not None
    assert n2 is not None
    assert n3 is not None
    assert toplevel is not None

    c=store_config(rref,S)
    assert_valid_config(c)
    cro=store_cattrs(rref,S)
    assert_valid_dref(getattr(cro,'n2'))
    assert_valid_dref(getattr(cro,'n3'))

    assert set(store_deps([n1],S)) == set([])
    assert set(store_deps([n2,n3],S)) == set([n1])
    assert set(store_deps([toplevel],S)) == set([n2,n3])

    assert store_deepdeps([n1],S) == set([])
    assert store_deepdeps([n2,n3],S) == set([n1])
    assert store_deepdeps([toplevel],S) == set([n1,n2,n3])

# def test_detect_rref_deps()->None:
#   with setup_storage('test_detect_rref_deps'):
#     rref=realize(instantiate(mktestnode,{'a':1}))
#     clo=instantiate(mktestnode,{'a':1,'maman':rref})
#     _,rrefs=scanref_dict(config_dict(store_config(clo.dref)))
#     assert len(rrefs)>0

def test_no_dref_deps_without_realizers()->None:
  with setup_storage2('test_no_dref_deps_without_realizers') as S:
    try:
      clo=instantiate(mktestnode,{'a':1},S=S)
      _=realize(instantiate(mktestnode,{'maman':clo.dref},S=S))
      raise ShouldHaveFailed("We shouldn't share DRefs across managers")
    except AssertionError:
      pass

def test_repeated_instantiate()->None:
  with setup_storage2('test_repeated_instantiate') as S:
    def _setting(m:Manager)->DRef:
      return mktestnode(m, {'a':'1'})

    cl1 = instantiate(_setting,S=S)
    cl2 = instantiate(_setting,S=S)
    assert len(cl1.derivations)==1
    assert len(cl2.derivations)==1
    assert cl1.derivations[0].dref == cl2.derivations[0].dref
    assert cl1.dref == cl2.dref


def test_repeated_realize()->None:
  with setup_storage2('test_repeated_realize') as S:
    def _setting(m:Manager)->DRef:
      return mktestnode(m, {'a':'1'})
    dref=instantiate(_setting,S=S)
    rref1=realize(dref)
    rref2=realize(dref)
    rref3=realize(dref, force_rebuild=[instantiate(_setting,S=S).dref])
    assert rref1==rref2 and rref2==rref3
    try:
      rref3=realize(dref, force_rebuild='Foobar') # type:ignore
      raise ShouldHaveFailed
    except AssertionError:
      pass

def test_realize_readonly()->None:
  with setup_storage2('test_realize_readonly') as S:
    rref1 = realize(instantiate(mktestnode, {'a':'1'},S=S))

    try:
      with open(join(store_rref2path(rref1,S),'newfile'),'w') as f:
        f.write('foo')
      raise ShouldHaveFailed('No write-protection??')
    except OSError:
      pass

    try:
      rmtree(store_rref2path(rref1,S))
      raise ShouldHaveFailed('No remove-protection??')
    except OSError:
      pass

    def _realize(b:Build):
      with open(join(build_outpath(b),'exe'),'w') as f:
        f.write('#!/bin/sh\necho "Fooo"')
      chmod(join(build_outpath(b),'exe'), S_IWRITE|S_IREAD|S_IEXEC)
    rref2=realize(instantiate(mkdrv, Config({}),
                              match_only(), build_wrapper(_realize),S=S))
    assert pipe_stdout([join(store_rref2path(rref2,S),'exe')])=='Fooo\n', \
      "Did we lost exec permission?"


def test_minimal_closure()->None:
  with setup_storage2('test_minimal_closure') as S:

    def _somenode(m):
      return mktestnode(m,{'a':0})

    def _anothernode(m):
      n1=mktestnode(m,{'a':1})
      n2=_somenode(m)
      n3=mktestnode(m,{'maman':n1,'papa':n2})
      return n3

    rref1=realize(instantiate(_somenode,S=S))
    rref=realize(instantiate(_anothernode,S=S))
    rref2=store_deref(rref,store_cattrs(rref,S=S).papa,S=S)[Tag('out')]
    assert rref1==rref2, '''
      Nodes with no dependencies should have empty context, regardless of their
      position in the closure.
      '''

def test_realize_nondetermenistic()->None:
  with setup_storage2('test_realize_nondetermenistic') as S:
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
    rref1 = realize(instantiate(_setup,S=S))
    DATA = 2
    rref2 = realize(instantiate(_setup,S=S), force_rebuild=[n2])

    assert len(list(dref2rrefs(n1,S))) == 1
    assert len(list(dref2rrefs(n2,S))) == 2
    assert len(list(dref2rrefs(n3,S))) == 2
    assert rref1 != rref2

    n2_gr1 = store_deref(rref1, n2,S)
    n2_gr2 = store_deref(rref2, n2,S)
    assert n2_gr1 != n2_gr2


def test_no_foreign_dref_deps()->None:
  with setup_storage2('test_no_foreign_dref_deps') as S:
    def _setup(m):
      clo=instantiate(mktestnode, {'foo':'bar'})
      return mktestnode(m,{'bogus':clo.dref})
    try:
      dref = instantiate(_setup,S=S)
      raise ShouldHaveFailed(f"Should fail, but got {dref}")
    except AssertionError:
      pass


def test_no_rref_deps()->None:
  with setup_storage2('test_no_rref_deps') as S:
    def _setup(m):
      rref=realize(instantiate(mktestnode, {'foo':'bar'}))
      n2 = mktestnode(m,{'bogus':rref})
      return n2
    try:
      dref = instantiate(_setup,S=S)
      raise ShouldHaveFailed(f"Should fail, but got {dref}")
    except AssertionError:
      pass


def test_no_recursive_instantiate_with_same_manager()->None:
  with setup_storage2('test_no_recursive_instantiate_with_same_manager') as S:
    def _setup(m):
      derivs = instantiate_(m,_setup)
      n2 = mktestnode(m,{'bogus':derivs.dref})
      return n2
    try:
      dref = instantiate(_setup,S=S)
      raise ShouldHaveFailed(f"Should fail, but got {dref}")
    except AssertionError:
      pass


def test_recursive_realize_with_another_manager()->None:
  with setup_storage2('test_recursive_realize_with_another_manager') as S:
    rref_inner=None
    def _setup_inner(m):
      return mktestnode(m,{'foo':'bar'})
    def _setup_outer(m):
      nonlocal rref_inner
      rref_inner=realize(instantiate(_setup_inner,S=S))
      return mktestnode(m,{'baz':mklens(rref_inner,S=S).foo.val})
    rref=realize(instantiate(_setup_outer,S=S))
    assert len(store_deepdeps([rref2dref(rref)],S=S))==0
    assert len(store_deepdeps([rref2dref(rref_inner)],S=S))==0
    assert mklens(rref_inner,S=S).foo.val=='bar'
    assert mklens(rref,S=S).baz.val=='bar'


def test_config_ro():
  d={'a':1,'b':33}
  c=mkconfig(d)
  cro=config_cattrs(RConfig(config_dict(c))) # We sure we don't have promises here
  for k in d.keys():
    assert getattr(cro,k) == d[k]


def test_mksymlink()->None:
  with setup_storage2('test_mksymlink') as S:
    tp=setup_testpath('test_mksymlink')
    print(tp)

    def _setting1(m:Manager)->DRef:
      return mktestnode_nondetermenistic(m, {'a':'1'}, lambda: 33, buildtime=False)
    def _setting2(m:Manager)->DRef:
      return mktestnode_nondetermenistic(m, {'a':'1'}, lambda: 42, buildtime=True)

    clo=instantiate(_setting1,S=S)
    rref=realize(clo)

    clo2=instantiate(_setting2,S=S)
    rref2=realize(clo2, force_rebuild=True)

    assert clo.dref==clo2.dref
    assert rref2!=rref

    s=mksymlink(rref, tgtpath=tp, name='thelink',S=S)
    assert islink(s)
    assert not isfile(join(s,'__buildtime__.txt'))
    assert tp in s

    s2=mksymlink(rref2, tgtpath=tp, name='thelink',S=S)
    assert islink(s2)
    assert isfile(join(s2,'__buildtime__.txt'))
    assert tp in s

    assert s2!=s, "s2 should have timestamp"

    s3=mksymlink(rref2, tgtpath=tp, name='thelink', withtime=False,S=S)
    assert s3==s

def test_ignored_stage()->None:
  with setup_storage2('test_ignored_stage') as S:
    n1:DRef; n2:DRef; n3:DRef; n4:DRef
    def _setting(m:Manager)->DRef:
      nonlocal n1, n2, n3, n4
      n1 = mktestnode(m, {'a':'1'})
      n2 = mktestnode(m, {'b':'2'}) # this one should not be realized
      n3 = mktestnode(m, {'c':'3', 'maman':n1})
      n4 = mktestnode(m, {'c':'4', 'papa':n3}) # neither this one
      return n3

    cl=instantiate(_setting,S=S)
    rref = realize(cl)
    rrefs:List[RRef] = []
    all_drefs = list(alldrefs(S))
    assert len(all_drefs)==4
    assert len(list(dref2rrefs(n1,S)))==1
    assert len(list(dref2rrefs(n2,S)))==0
    assert len(list(dref2rrefs(n3,S)))==1
    assert len(list(dref2rrefs(n4,S)))==0


def test_overwrite_realizer()->None:
  with setup_storage2('test_overwrite_realizer') as S:
    n1:DRef; n2:DRef; n3:DRef; n4:DRef
    def _setting(m:Manager)->DRef:
      nonlocal n1, n2, n3, n4
      n1 = mktestnode_nondetermenistic(m, {'a':'1'}, lambda:33)
      n2 = mktestnode(m, {'maman':n1})
      n3 = mktestnode_nondetermenistic(m, {'a':'1'}, lambda:42)
      assert n1 == n3
      return n2

    rref_n2=realize(instantiate(_setting, S=S))
    all_drefs = list(alldrefs(S))
    assert len(all_drefs)==2

    rref_n3=store_deref(rref_n2, store_cattrs(rref_n2, S).maman, S)[Tag('out')]
    assert open(join(store_rref2path(rref_n3, S),'artifact'),'r').read() == '42'

def test_match_only()->None:
  with setup_storage2('test_match_only') as S:

    build:int = 0
    def _setting(m:Manager)->DRef:
      def _realize(b:Build)->None:
        nonlocal build
        with open(join(build_outpath(b),'artifact'),'w') as f:f.write(str(build))
        build+=1
      return mkdrv(m, mkconfig({'a':1}), match_only(), build_wrapper(_realize))

    closure = instantiate(_setting,S=S)
    assert len(list(dref2rrefs(closure.dref,S))) == 0
    rref = realize(closure)
    assert len(list(dref2rrefs(closure.dref,S))) == 1
    rref = realize(closure)
    assert len(list(dref2rrefs(closure.dref,S))) == 1
    try:
      rref = realize(closure, force_rebuild=[closure.dref])
      raise ShouldHaveFailed('Should have failed in match_only assertion')
    except AssertionError as e:
      pass
    assert len(list(dref2rrefs(closure.dref,S))) == 2


def test_match_best()->None:
  with setup_storage2('test_match_best') as S:
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

    clo1=instantiate(_mklrg, {'a':1}, matcher=match_best('score'), S=S)
    score='0'
    rref1a=realize(clo1)
    assert isfile(join(store_rref2path(rref1a,S),'score'))
    assert len(list(dref2rrefs(clo1.dref,S))) == 1
    assert tryread(Path(join(store_rref2path(rref1a,S),'score')))=='0'
    score='non-integer'
    rref1b=realize(clo1, force_rebuild=[clo1.dref])
    assert isfile(join(store_rref2path(rref1b,S),'score'))
    assert len(list(dref2rrefs(clo1.dref,S))) == 2
    assert tryread(Path(join(store_rref2path(rref1b,S),'score')))=='0'
    score='1'
    rref1c=realize(clo1, force_rebuild=[clo1.dref])
    assert isfile(join(store_rref2path(rref1c,S),'score'))
    assert len(list(dref2rrefs(clo1.dref,S))) == 3
    assert tryread(Path(join(store_rref2path(rref1c,S),'score')))=='1'
    # Here we refuse to create 'score' file altogether. `match_best` should
    # ignore this realization.
    score='100500'
    fname='baz'
    rref1d=realize(clo1, force_rebuild=[clo1.dref])
    assert not isfile(join(store_rref2path(rref1d,S),'baz'))
    assert len(list(dref2rrefs(clo1.dref,S))) == 4

    # This test case did flicker. The last fix was to sort filenames in
    # `dirhash`.
    #
    # To check, run:
    # 1. `logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)`
    # 2. `dirhash('/tmp/test_match_best/a76762e9bc54e47c09455bdb226e2388-unnamed/'
    #             '0554aac0dbae2d80f67e7d280ab331a4',
    #             verbose=True)`
    #
    # Current output:
    # context.json: 44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a
    # tag.txt: 0b20b35d367ea15c3b95476337549e5add5973dab18f0fc1b3391c40ba82cf8a
    # baz: 6d2909ed88f980f2241835f0f5d76e8b31dbdc90c22d8fb7e446ffe4647eb8f2
    # group.txt: 0554aac0dbae2d80f67e7d280ab331a44c55f0b63f674a3a278411620fbede12
    clo1=instantiate(_mklrg, {'a':1},
      matcher=match([exact([
        RRef('rref:3e8dfe0bf20b217f96590a4f7c7a5a01-a76762e9bc54e47c09455bdb226e2388-unnamed')])]),
                     S=S)
    rref1e=realize(clo1)
    assert isfile(join(store_rref2path(rref1e,S),'baz'))
    assert len(list(dref2rrefs(clo1.dref,S))) == 4

    clo1=instantiate(_mklrg, {'a':1}, matcher=match_best('score'),S=S)
    rref1=realize(clo1)
    assert isfile(join(store_rref2path(rref1,S),'score'))
    assert tryread(Path(join(store_rref2path(rref1,S),'score')))=='1'


def test_match_latest()->None:
  def _mknode(m, cfg, matcher, nouts:int, data=0, buildtime=True):
    def _realize(b:Build)->None:
      build_setoutpaths(b,nouts)
      for i,out in enumerate(build_outpaths(b)):
        assert trywrite(Path(join(out,'artifact')),str(data)+'_'+str(i))
    return mkdrv(m, Config(cfg), matcher,
                    build_wrapper(_realize, buildtime=buildtime))

  with setup_storage2('test_match_latest') as S:
    clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=1, S=S)
    rref1=realize(clo)
    assert len(list(dref2rrefs(clo.dref,S)))==1
    sleep(0.01)
    clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=2, S=S)
    rref2=realize(clo, force_rebuild=[clo.dref])
    assert len(list(dref2rrefs(clo.dref,S)))==2
    assert tryread(Path(join(store_rref2path(rref2,S),'artifact')))==str('2_0')

  with setup_storage2('test_match_latest') as S:
    clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=1, S=S)
    rref1=realize(clo)
    assert len(list(dref2rrefs(clo.dref,S)))==1
    sleep(0.01)
    clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=2, buildtime=False, S=S)
    rref2=realize(clo, force_rebuild=[clo.dref])
    assert len(list(dref2rrefs(clo.dref,S)))==2
    assert tryread(Path(join(store_rref2path(rref2,S),'artifact')))==str('1_0')

  for i in range(10):
    with setup_storage2('test_match_latest') as S:
      nouts=randint(1,10)
      ntop=randint(1,10)
      try:
        clo=instantiate(_mknode, {'a':0}, match_latest(ntop), nouts, S=S)
        rrefs=realizeMany(clo)
        times=set([tryread(Path(join(store_rref2path(rref,S),'__buildtime__.txt'))) for rref in rrefs])
        assert len(list(times))==1
      except AssertionError:
        assert ntop>nouts


def test_match_all()->None:
  """ match_all() should match all the references """
  def _mknode(m,cfg, matcher, nouts:int):
    def _realize(b:Build)->None:
      build_setoutpaths(b,nouts)
      for i,out in enumerate(build_outpaths(b)):
        assert trywrite(Path(join(out,'artifact')),str(nouts+i))
    return mkdrv(m, Config(cfg), matcher, build_wrapper(_realize))

  with setup_storage2('test_match_all_empty') as S:
    clo=instantiate(_mknode, {'a':1}, match_all(), 5, S=S)
    rrefs=realizeMany(clo)
    assert len(rrefs)==0

  for i in range(10):
    data=randint(1,10)
    nouts=randint(1,10)
    with setup_storage2('test_match_all') as S:
      clo=instantiate(_mknode, {'a':data}, match_n(1), nouts, S=S)
      rrefs_1=realizeMany(clo)
      assert len(rrefs_1)==1
      clo=instantiate(_mknode, {'a':data}, match_all(), nouts, S=S)
      rrefs_all=realizeMany(clo)
      assert len(rrefs_all)==nouts

def test_match_some()->None:
  with setup_storage2('test_match_some') as S:
    def _mknode(m, cfg, nouts:int, top:int):
      def _realize(b:Build)->None:
        build_setoutpaths(b,nouts)
        for i,out in enumerate(build_outpaths(b)):
          assert trywrite(Path(join(out,'artifact')),str(nouts+i))
      return mkdrv(m, mkconfig(cfg), match_some(n=top), build_wrapper(_realize))

    for i in range(10):
      nouts=randint(1,10)
      top=randint(1,10)
      clo=instantiate(_mknode, {'a':randint(0,1000)}, nouts, top, S=S)
      try:
        rrefs=realizeMany(clo, force_rebuild=[clo.dref])
        assert top<=nouts
      except AssertionError:
        assert top>nouts


def test_gc()->None:
  with setup_storage2('test_gc') as S:
    def _node1(m:Manager)->DRef:
      return mktestnode(m, {'name':'1'})
    def _node2(m:Manager)->DRef:
      return mktestnode(m, {'name':'2', 'maman':_node1(m)})
    def _node3(m:Manager)->DRef:
      return mktestnode(m, {'name':'3', 'maman':_node1(m)})

    r1=realize(instantiate(_node1,S=S))
    r2=realize(instantiate(_node2,S=S))
    r3=realize(instantiate(_node3,S=S))

    rm_drefs,rm_rrefs=store_gc([],[r2],S)
    assert rm_drefs=={rref2dref(r) for r in [r3]}
    assert rm_rrefs=={x for x in [r3]}

def test_promise()->None:
  with setup_storage2('test_promise') as S:
    def _setting(m:Manager, fullfill:bool)->DRef:
      n1=mktestnode(m, {'name':'1', 'promise':[promise,'artifact']})
      def _realize(b:Build):
        o=build_outpath(b)
        c=build_cattrs(b)
        assert b.dref in c.promise
        assert n1 in store_cattrs(c.maman,S).promise
        assert build_path(b,c.promise)==join(o,'uber-artifact')
        assert build_path(b,store_cattrs(c.maman,S).promise)==build_path(b,c.maman_promise)
        if fullfill:
          with open(build_path(b,c.promise),'w') as f:
            f.write('chickenpoop')

      return mkdrv(m, mkconfig({'name':'2', 'maman':n1,
                                'promise':[promise,'uber-artifact'],
                                'maman_promise':[n1,'artifact']}),
                      matcher=match_only(),
                      realizer=build_wrapper(_realize))

    try:
      rref=realize(instantiate(_setting,False,S=S))
      raise ShouldHaveFailed('Promise trigger')
    except AssertionError:
      pass
    rref=realize(instantiate(_setting,True,S=S))
    assert_valid_rref(rref)

def test_path2rref()->None:
  with setup_storage2('test_path2rref') as S:
    s1=partial(mktestnode, sources={'name':'1', 'promise':[promise,'artifact']})
    rref1=realize(instantiate(s1,S=S))
    rref2=path2rref(store_rref2path(rref1,S))
    assert rref1==rref2
    l=mksymlink(rref1, S, 'result', S=S)
    assert path2rref(Path(l))==rref1
    rref3=path2rref(Path("/foo/00000000000000000000000000000000-bar/11111111111111111111111111111111"))
    assert rref3=='rref:11111111111111111111111111111111-00000000000000000000000000000000-bar'
    for x in [path2rref(Path('')),path2rref(Path('foo'))]:
      assert x is None

def test_path2dref()->None:
  with setup_storage2('test_path2dref') as S:
    s1=partial(mktestnode, sources={'name':'1', 'promise':[promise,'artifact']})
    clo1=instantiate(s1,S=S)
    dref1=clo1.dref
    rref1=realize(clo1)
    dref2=path2dref(store_dref2path(rref2dref(rref1),S=S))
    assert dref1==dref2
    l=linkdref(dref1, S, 'result_dref', S=S)
    assert path2dref(Path(l))==dref1
    dref3=path2dref(Path("/foo/00000000000000000000000000000000-bar"))
    assert dref3=='dref:00000000000000000000000000000000-bar'
    for x in [path2dref(Path('')),path2dref(Path('foo'))]:
      assert x is None

def test_linkrrefs()->None:
  with setup_storage2('test_linkrefs') as S:
    s1=partial(mktestnode, sources={'name':'1', 'promise':[promise,'artifact']})
    rref1=realize(instantiate(s1,S=S))
    l=linkrrefs([rref1, rref1], destdir=S, S=S)
    assert len(l)==2
    assert str(l[0])==join(S,'result-1')
    assert islink(join(S,'result-1'))
    l=linkrrefs([rref1], destdir=S, withtime=True, S=S)
    assert S in l[0]


