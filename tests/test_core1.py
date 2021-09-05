from pylightnix import (instantiate, DRef, RRef, Path, SPath, mklogdir, dirhash,
                        assert_valid_dref, assert_valid_rref, drefdeps1,
                        drefdeps, store_gc, assert_valid_config, Registry,
                        mkcontext, allrrefs, mkdref, mkrref, unrref, undref,
                        realize1, rref2dref, drefcfg, mkconfig, Build, Context,
                        build_outpath, mkdrv, rref2path, cfgcattrs, drefattrs,
                        build_deref, build_path, mkrefpath, build_config,
                        alldrefs, build_wrapper, build_cattrs, build_name,
                        tryread, trywrite, realizeMany, scanref_dict, cfgdict,
                        mklens, isrref, Config, RConfig, partial, path2rref,
                        concat, linkrrefs, mkclosure, dref2path, path2dref,
                        linkdref, rrefdeps, drefrrefs, allrrefs, match_only,
                        drefrrefs, drefrrefsC, rrefctx, context_deref,
                        rrefattrs, rrefbstart, fsstorage, current_registry,
                        realize, current_storage, Tuple)

from tests.imports import (given, Any, Callable, join, Optional, islink, isfile,
                           islink, isdir, dirname, List, randint, sleep, rmtree,
                           system, S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen,
                           PIPE, data, readlink)

from tests.generators import (rrefs, drefs, configs, dicts, rootstages,
                              settings)

from tests.setup import ( ShouldHaveFailed, setup_storage2,
                         mkstage, pipe_stdout )


# @given(d=dicts())
# def test_realize_base(d)->None:
#   with setup_storage2('test_realize_base') as S:
#     r=Registry(storage(S))
#     mkstage(r, d)
#     dref=list(r.builders.values())[-1].targets[0]
#     assert_valid_dref(dref)
#     assert len(list(drefrrefsC(dref, mkcontext(), S))) == 0
#     rrefgs=list(r.builders.values())[-1].matcher(S, dref, mkcontext())
#     assert rrefgs is None
#     rrefg=mkrgroup(dref, mkcontext(),
#         list(r.builders.values())[-1].realizer(S, dref, mkcontext(),{})[0], S)
#     assert len(list(store_rrefs(dref, mkcontext(), S))) == 1
#     assert_valid_rref(rrefg[Tag('out')])
#     rrefgs2=list(r.builders.values())[-1].matcher(S, dref, mkcontext())
#     assert rrefgs2 is not None
#     rrefg2=rrefgs2[0]
#     assert rrefg==rrefg2


# def test_realize_dependencies()->None:
#   with setup_storage2('test_realize_dependencies') as S:
#     n1=None; n2=None; n3=None; toplevel=None

#     def _setup(r):
#       nonlocal n1,n2,n3,toplevel
#       n1=mkstage(r, {'a':1})
#       n2=mkstage(r, {'parent1':n1})
#       n3=mkstage(r, {'parent2':n1})
#       toplevel=mkstage(r, {'n2':n2,'n3':n3})
#       return toplevel

#     rref=realize1(mkclosure(_setup,S=S))
#     assert_valid_rref(rref)
#     assert n1 is not None
#     assert n2 is not None
#     assert n3 is not None
#     assert toplevel is not None

#     c=drefcfg(rref,S)
#     assert_valid_config(c)
#     cro=store_cattrs(rref,S)
#     assert_valid_dref(getattr(cro,'n2'))
#     assert_valid_dref(getattr(cro,'n3'))

#     assert set(drefdeps1([n1],S)) == set([])
#     assert set(drefdeps1([n2,n3],S)) == set([n1])
#     assert set(drefdeps1([toplevel],S)) == set([n2,n3])

#     assert drefdeps([n1],S) == set([])
#     assert drefdeps([n2,n3],S) == set([n1])
#     assert drefdeps([toplevel],S) == set([n1,n2,n3])

# def test_detect_rref_deps()->None:
#   with setup_storage('test_detect_rref_deps'):
#     rref=realize1(instantiate(mkstage,{'a':1}))
#     clo=instantiate(mkstage,{'a':1,'maman':rref})
#     _,rrefs=scanref_dict(cfgdict(drefcfg(clo.targets[0])))
#     assert len(rrefs)>0

def test_no_dref_deps_without_realizers()->None:
  with setup_storage2('test_no_dref_deps_without_realizers') as S:
    try:
      _,clo=instantiate(mkstage,{'a':1},S=S)
      _=realize1(instantiate(mkstage,{'maman':clo.targets[0]},S=S))
      raise ShouldHaveFailed("We shouldn't share DRefs across registries")
    except AssertionError:
      pass

def test_repeated_instantiate()->None:
  with setup_storage2('test_repeated_instantiate') as S:
    def _setting(r:Registry)->DRef:
      return mkstage({'a':'1'}, r)
    _,cl1=instantiate(_setting,S=S)
    _,cl2=instantiate(_setting,S=S)
    assert len(cl1.derivations)==1
    assert len(cl2.derivations)==1
    assert cl1.derivations[0].dref == cl2.derivations[0].dref
    assert cl1.targets[0] == cl2.targets[0]


def test_repeated_realize()->None:
  with setup_storage2('test_repeated_realize') as S:
    def _setting(r:Registry)->DRef:
      return mkstage({'a':'1'},r)
    _,clo=instantiate(_setting,S=S)
    rref1=realize1(clo)
    rref2=realize1(clo)
    rref3=realize1(clo, force_rebuild=[clo.targets[0]])
    assert rref1==rref2 and rref2==rref3
    try:
      rref3=realize1(clo, force_rebuild='Foobar') # type:ignore
      raise ShouldHaveFailed
    except AssertionError:
      pass

def test_realize_readonly()->None:
  with setup_storage2('test_realize_readonly') as S:
    rref1 = realize1(instantiate(mkstage,{'a':'1'},S=S))

    try:
      with open(join(rref2path(rref1,S),'newfile'),'w') as f:
        f.write('foo')
      raise ShouldHaveFailed('No write-protection??')
    except OSError:
      pass

    try:
      rmtree(rref2path(rref1,S))
      raise ShouldHaveFailed('No remove-protection??')
    except OSError:
      pass

    def _realize(b:Build):
      with open(join(build_outpath(b),'exe'),'w') as f:
        f.write('#!/bin/sh\necho "Fooo"')
      chmod(join(build_outpath(b),'exe'), S_IWRITE|S_IREAD|S_IEXEC)
    rref2=realize1(instantiate(mkdrv, Config({}),
                              match_only(), build_wrapper(_realize),S=S))
    assert pipe_stdout([join(rref2path(rref2,S),'exe')])=='Fooo\n', \
      "Did we lost exec permission?"


def test_minimal_closure()->None:
  with setup_storage2('test_minimal_closure') as S:

    def _somenode(r):
      return mkstage({'a':0},r)

    def _anothernode(r):
      n1=mkstage({'a':1},r)
      n2=_somenode(r)
      n3=mkstage({'maman':n1,'papa':n2},r)
      return n3

    rref1=realize1(instantiate(_somenode,S=S))
    rref=realize1(instantiate(_anothernode,S=S))
    rref2=context_deref(rrefctx(rref,S),rrefattrs(rref,S=S).papa)[0]
    assert rref1==rref2, '''
      Nodes with no dependencies should have empty context, regardless of their
      position in the closure.
      '''

# FIXME make sure that contexts are inequal
# def test_realize_nondetermenistic()->None:
#   with setup_storage2('test_realize_nondetermenistic') as S:
#     DATA:int; n1:DRef; n2:DRef; n3:DRef

#     def _gen(i)->int:
#       nonlocal DATA
#       return DATA

#     def _setup(r):
#       nonlocal n1, n2, n3
#       n1 = mkstage( {'a':'1'},r)
#       n2 = mkstage(r,{'maman':n1},_gen)
#       n3 = mkstage(r,{'papa':n2})
#       return n3

#     DATA = 1
#     rref1 = realize1(instantiate(_setup,S=S))
#     DATA = 2
#     rref2 = realize1(instantiate(_setup,S=S), force_rebuild=[n2])

#     assert len(list(drefrrefs(n1,S))) == 1
#     assert len(list(drefrrefs(n2,S))) == 2
#     assert len(list(drefrrefs(n3,S))) == 2
#     assert rref1 != rref2

#     n2_gr1 = store_deref(rref1, n2,S)
#     n2_gr2 = store_deref(rref2, n2,S)
#     assert n2_gr1 != n2_gr2


def test_no_foreign_dref_deps()->None:
  with setup_storage2('test_no_foreign_dref_deps') as S:
    with setup_storage2('test_no_foreign_dref_deps_2') as S2:
      def _setup(r):
        _,clo=instantiate(mkstage, {'name':'foreign', 'foo':'bar'}, S=S2)
        return mkstage({'bogus':clo.targets[0]},r)
      try:
        xxx:tuple=instantiate(_setup,S=S)
        raise ShouldHaveFailed(f"Should fail, but got {xxx}")
      except FileNotFoundError:
        pass


def test_no_rref_deps()->None:
  with setup_storage2('test_no_rref_deps') as S:
    def _setup(r):
      rref=realize1(instantiate(mkstage, {'foo':'bar'}))
      n2=mkstage({'bogus':rref},r)
      return n2
    try:
      xxx:tuple=instantiate(_setup,S=S)
      raise ShouldHaveFailed(f"Should fail, but got {xxx}")
    except AssertionError:
      pass


def test_no_recursive_instantiate_with_same_registry()->None:
  with setup_storage2('test_no_recursive_instantiate_with_same_registry') as S:
    def _setup(r):
      derivs:tuple = instantiate(_setup,r=r)
      n2 = mkstage({'bogus':derivs[1].targets[0]},r)
      return n2
    try:
      xxx:tuple=instantiate(_setup,S=S)
      raise ShouldHaveFailed(f"Should fail, but got {xxx}")
    except AssertionError:
      pass


def test_recursive_realize_with_another_registry()->None:
  with setup_storage2('test_recursive_realize_with_another_registry') as S:
    def _setup_inner(r):
      return mkstage({'foo':'bar'},r)
    def _setup_outer(r):
      # nonlocal rref_inner
      rref_inner=realize1(instantiate(_setup_inner,S=S))
      r2=mkstage({'baz':mklens(rref_inner,S=S).foo.val},r)
      return [rref_inner,r2]
    _,clo=instantiate(_setup_outer,S=S)
    rref=realize1(clo)
    [rref_inner,r2]=clo.result
    assert rref_inner is not None
    assert len(drefdeps([rref2dref(rref)],S=S))==0
    assert len(drefdeps([rref2dref(rref_inner)],S=S))==0
    assert mklens(rref_inner,S=S).foo.val=='bar'
    assert mklens(rref,S=S).baz.val=='bar'


def test_config_ro():
  d={'a':1,'b':33}
  c=mkconfig(d)
  cro=cfgcattrs(RConfig(cfgdict(c))) # We sure we don't have promises here
  for k in d.keys():
    assert getattr(cro,k) == d[k]


def test_ignored_stage()->None:
  with setup_storage2('test_ignored_stage') as S:
    n1:DRef; n2:DRef; n3:DRef; n4:DRef
    def _setting(r:Registry)->Tuple[DRef,...]:
      nonlocal n2,n4
      n1 = mkstage({'a':'1'},r)
      n2 = mkstage({'b':'2'},r) # this one should not be realized
      n3 = mkstage({'c':'3','maman':n1},r)
      n4 = mkstage({'c':'4','papa':n3},r) # neither this one
      return n1,n3

    (n1,n3),clo=instantiate(_setting,S=S)
    realize(clo)
    all_drefs=list(alldrefs(S))
    assert len(all_drefs)==4
    assert len(list(drefrrefs(n1,S)))==1
    assert len(list(drefrrefs(n2,S)))==0
    assert len(list(drefrrefs(n3,S)))==1
    assert len(list(drefrrefs(n4,S)))==0


def test_overwrite_realizer()->None:
  with setup_storage2('test_overwrite_realizer') as S:
    n1:DRef; n2:DRef; n3:DRef
    def _setting(r:Registry)->DRef:
      nonlocal n1, n2, n3
      n1 = mkstage({'a':'1'},r,lambda i:33)
      n2 = mkstage({'maman':n1},r)
      n3 = mkstage({'a':'1'},r,lambda i:42)
      return n2

    rref_n2=realize1(instantiate(_setting, S=S))
    all_drefs = list(alldrefs(S))
    assert len(all_drefs)==2

    rref_n3=context_deref(rrefctx(rref_n2,S), rrefattrs(rref_n2, S).maman)[0]
    assert open(join(rref2path(rref_n3, S),'artifact'),'r').read() == '42'



def test_gc()->None:
  with setup_storage2('test_gc') as S:
    def _node1(r:Registry)->DRef:
      return mkstage({'name':'1'},r)
    def _node2(r:Registry)->DRef:
      return mkstage({'name':'2', 'maman':_node1(r)},r)
    def _node3(r:Registry)->DRef:
      return mkstage({'name':'3', 'maman':_node1(r)},r)

    r1=realize1(instantiate(_node1,S=S))
    r2=realize1(instantiate(_node2,S=S))
    r3=realize1(instantiate(_node3,S=S))

    rm_drefs,rm_rrefs=store_gc([],[r2],S)
    assert rm_drefs=={rref2dref(r) for r in [r3]}
    assert rm_rrefs=={x for x in [r3]}

# def test_promise()->None:
#   with setup_storage2('test_promise') as S:
#     def _setting(r:Registry, fullfill:bool)->DRef:
#       n1=mkstage(r, {'name':'1', 'promise':[promise,'artifact']})
#       def _realize(b:Build):
#         o=build_outpath(b)
#         c=build_cattrs(b)
#         assert b.targets[0] in c.promise
#         assert n1 in store_cattrs(c.maman,S).promise
#         assert build_path(b,c.promise)==join(o,'uber-artifact')
#         assert build_path(b,store_cattrs(c.maman,S).promise)==build_path(b,c.maman_promise)
#         if fullfill:
#           with open(build_path(b,c.promise),'w') as f:
#             f.write('chickenpoop')

#       return mkdrv(r, mkconfig({'name':'2', 'maman':n1,
#                                 'promise':[promise,'uber-artifact'],
#                                 'maman_promise':[n1,'artifact']}),
#                       matcher=match_only(),
#                       realizer=build_wrapper(_realize))

#     try:
#       rref=realize1(instantiate(_setting,False,S=S))
#       raise ShouldHaveFailed('Promise trigger')
#     except AssertionError:
#       pass
#     rref=realize1(instantiate(_setting,True,S=S))
#     assert_valid_rref(rref)


@settings(max_examples=10)
@given(dref=drefs())
def test_path2dref(dref):
  with setup_storage2('test_path2dref') as S:
    p=dref2path(dref,S)
    assert isdir(dirname(p))
    dref2=path2dref(p)
    assert dref==dref2

@settings(max_examples=10)
@given(rref=rrefs())
def test_path2rref(rref):
  with setup_storage2('test_path2rref') as S:
    p=rref2path(rref,S)
    assert isdir(dirname(dirname(p)))
    rref2=path2rref(p)
    assert rref==rref2

def test_linkdref()->None:
  with setup_storage2('test_linkdref') as S:
    s1=partial(mkstage, config={'name':'NaMe'})
    dref1:DRef=instantiate(s1,S=S)[0]
    l=linkdref(dref1, destdir=fsstorage(S), format='result-%(N)s', S=S)
    assert str(l)==join(fsstorage(S),'result-NaMe')
    assert islink(join(fsstorage(S),'result-NaMe'))
    assert fsstorage(S) in l
    assert undref(dref1)[0] in readlink(l)

def test_current_registry():
  with setup_storage2('test_current_registry') as S:
    with current_registry(Registry(S)) as r:
      n1=mkstage({'a':'1'})
      n2=mkstage({'b':'2'})
      n3=mkstage({'c':'3','maman':n1})
      n4=mkstage({'c':'4','papa':n3})
      assert_valid_dref(n3)
      assert_valid_dref(n4)

      rref_n3 = realize1(instantiate(n3))
      assert_valid_rref(rref_n3)

      all_drefs = list(alldrefs(S))
      assert len(all_drefs)==4
      assert len(list(drefrrefs(n1)))==1
      assert len(list(drefrrefs(n2)))==0
      assert len(list(drefrrefs(n3)))==1
      assert len(list(drefrrefs(n4)))==0


def test_current_storage():
  with setup_storage2('test_current_storage1') as S1,\
       setup_storage2('test_current_storage2') as S2:
    with current_storage(S1):
      realize1(instantiate(partial(mkstage,config={'a':'1'})))
      realize1(instantiate(partial(mkstage,config={'b':'2'})))
      with current_storage(S2) as S:
        with current_registry(Registry(S)):
          realize1(instantiate(mkstage({'c':'3'})))
        assert len(list(alldrefs()))==1
      assert len(list(alldrefs()))==2
    assert len(list(alldrefs(S1)))==2
    assert len(list(alldrefs(S2)))==1

