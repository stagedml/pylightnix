from pylightnix import (instantiate, DRef, RRef, Path, SPath, mklogdir, dirhash,
                        assert_valid_dref, assert_valid_rref, drefdeps1,
                        drefdeps, store_gc, assert_valid_config, Manager,
                        mkcontext, allrrefs, mkdref, mkrref, unrref, undref,
                        realize, rref2dref, drefcfg, mkconfig, Build, Context,
                        build_outpath, mkdrv, rref2path, config_cattrs,
                        mksymlink, drefattrs, build_deref, build_path,
                        mkrefpath, build_config, alldrefs, build_wrapper,
                        build_cattrs, build_name, tryread, trywrite,
                        realizeMany, scanref_dict, config_dict, mklens, isrref,
                        Config, RConfig, build_setoutpaths, partial, path2rref,
                        concat, linkrrefs, instantiate_, dref2path,
                        path2dref, linkdref, storage, rrefdeps,
                        drefrrefs, allrrefs, match_only, drefrrefs, drefrrefsC,
                        rrefctx, context_deref, rrefattrs )

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, islink, List, randint, sleep, rmtree, system,
                           S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen, PIPE, data)

from tests.generators import (rrefs, drefs, configs, dicts, rootstages)

from tests.setup import ( ShouldHaveFailed, setup_storage, setup_storage2,
                         mkstage, mkstage, pipe_stdout )


# @given(d=dicts())
# def test_realize_base(d)->None:
#   with setup_storage2('test_realize_base') as (T,S):
#     m=Manager(storage(S))
#     mkstage(m, d)
#     dref=list(m.builders.values())[-1].dref
#     assert_valid_dref(dref)
#     assert len(list(drefrrefsC(dref, mkcontext(), S))) == 0
#     rrefgs=list(m.builders.values())[-1].matcher(S, dref, mkcontext())
#     assert rrefgs is None
#     rrefg=mkrgroup(dref, mkcontext(),
#         list(m.builders.values())[-1].realizer(S, dref, mkcontext(),{})[0], S)
#     assert len(list(store_rrefs(dref, mkcontext(), S))) == 1
#     assert_valid_rref(rrefg[Tag('out')])
#     rrefgs2=list(m.builders.values())[-1].matcher(S, dref, mkcontext())
#     assert rrefgs2 is not None
#     rrefg2=rrefgs2[0]
#     assert rrefg==rrefg2


# def test_realize_dependencies()->None:
#   with setup_storage2('test_realize_dependencies') as (T,S):
#     n1=None; n2=None; n3=None; toplevel=None

#     def _setup(m):
#       nonlocal n1,n2,n3,toplevel
#       n1=mkstage(m, {'a':1})
#       n2=mkstage(m, {'parent1':n1})
#       n3=mkstage(m, {'parent2':n1})
#       toplevel=mkstage(m, {'n2':n2,'n3':n3})
#       return toplevel

#     rref=realize(instantiate(_setup,S=S))
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
#     rref=realize(instantiate(mkstage,{'a':1}))
#     clo=instantiate(mkstage,{'a':1,'maman':rref})
#     _,rrefs=scanref_dict(config_dict(drefcfg(clo.dref)))
#     assert len(rrefs)>0

def test_no_dref_deps_without_realizers()->None:
  with setup_storage2('test_no_dref_deps_without_realizers') as (T,S):
    try:
      clo=instantiate(mkstage,{'a':1},S=S)
      _=realize(instantiate(mkstage,{'maman':clo.dref},S=S))
      raise ShouldHaveFailed("We shouldn't share DRefs across managers")
    except AssertionError:
      pass

def test_repeated_instantiate()->None:
  with setup_storage2('test_repeated_instantiate') as (T,S):
    def _setting(m:Manager)->DRef:
      return mkstage(m, {'a':'1'})

    cl1 = instantiate(_setting,S=S)
    cl2 = instantiate(_setting,S=S)
    assert len(cl1.derivations)==1
    assert len(cl2.derivations)==1
    assert cl1.derivations[0].dref == cl2.derivations[0].dref
    assert cl1.dref == cl2.dref


def test_repeated_realize()->None:
  with setup_storage2('test_repeated_realize') as (T,S):
    def _setting(m:Manager)->DRef:
      return mkstage(m, {'a':'1'})
    clo=instantiate(_setting,S=S)
    rref1=realize(clo)
    rref2=realize(clo)
    rref3=realize(clo, force_rebuild=[clo.dref])
    assert rref1==rref2 and rref2==rref3
    try:
      rref3=realize(clo, force_rebuild='Foobar') # type:ignore
      raise ShouldHaveFailed
    except AssertionError:
      pass

def test_realize_readonly()->None:
  with setup_storage2('test_realize_readonly') as (T,S):
    rref1 = realize(instantiate(mkstage, {'a':'1'},S=S))

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
    rref2=realize(instantiate(mkdrv, Config({}),
                              match_only(), build_wrapper(_realize),S=S))
    assert pipe_stdout([join(rref2path(rref2,S),'exe')])=='Fooo\n', \
      "Did we lost exec permission?"


def test_minimal_closure()->None:
  with setup_storage2('test_minimal_closure') as (T,S):

    def _somenode(m):
      return mkstage(m,{'a':0})

    def _anothernode(m):
      n1=mkstage(m,{'a':1})
      n2=_somenode(m)
      n3=mkstage(m,{'maman':n1,'papa':n2})
      return n3

    rref1=realize(instantiate(_somenode,S=S))
    rref=realize(instantiate(_anothernode,S=S))
    rref2=context_deref(rrefctx(rref,S),rrefattrs(rref,S=S).papa)[0]
    assert rref1==rref2, '''
      Nodes with no dependencies should have empty context, regardless of their
      position in the closure.
      '''

# FIXME make sure that contexts are inequal
# def test_realize_nondetermenistic()->None:
#   with setup_storage2('test_realize_nondetermenistic') as (T,S):
#     DATA:int; n1:DRef; n2:DRef; n3:DRef

#     def _gen(i)->int:
#       nonlocal DATA
#       return DATA

#     def _setup(m):
#       nonlocal n1, n2, n3
#       n1 = mkstage(m, {'a':'1'})
#       n2 = mkstage(m,{'maman':n1},_gen)
#       n3 = mkstage(m,{'papa':n2})
#       return n3

#     DATA = 1
#     rref1 = realize(instantiate(_setup,S=S))
#     DATA = 2
#     rref2 = realize(instantiate(_setup,S=S), force_rebuild=[n2])

#     assert len(list(drefrrefs(n1,S))) == 1
#     assert len(list(drefrrefs(n2,S))) == 2
#     assert len(list(drefrrefs(n3,S))) == 2
#     assert rref1 != rref2

#     n2_gr1 = store_deref(rref1, n2,S)
#     n2_gr2 = store_deref(rref2, n2,S)
#     assert n2_gr1 != n2_gr2


def test_no_foreign_dref_deps()->None:
  with setup_storage2('test_no_foreign_dref_deps') as (T,S):
    def _setup(m):
      clo=instantiate(mkstage, {'foo':'bar'})
      return mkstage(m,{'bogus':clo.dref})
    try:
      dref = instantiate(_setup,S=S)
      raise ShouldHaveFailed(f"Should fail, but got {dref}")
    except AssertionError:
      pass


def test_no_rref_deps()->None:
  with setup_storage2('test_no_rref_deps') as (T,S):
    def _setup(m):
      rref=realize(instantiate(mkstage, {'foo':'bar'}))
      n2 = mkstage(m,{'bogus':rref})
      return n2
    try:
      dref = instantiate(_setup,S=S)
      raise ShouldHaveFailed(f"Should fail, but got {dref}")
    except AssertionError:
      pass


def test_no_recursive_instantiate_with_same_manager()->None:
  with setup_storage2('test_no_recursive_instantiate_with_same_manager') as (T,S):
    def _setup(m):
      derivs = instantiate_(m,_setup)
      n2 = mkstage(m,{'bogus':derivs.dref})
      return n2
    try:
      dref = instantiate(_setup,S=S)
      raise ShouldHaveFailed(f"Should fail, but got {dref}")
    except AssertionError:
      pass


def test_recursive_realize_with_another_manager()->None:
  with setup_storage2('test_recursive_realize_with_another_manager') as (T,S):
    rref_inner=None
    def _setup_inner(m):
      return mkstage(m,{'foo':'bar'})
    def _setup_outer(m):
      nonlocal rref_inner
      rref_inner=realize(instantiate(_setup_inner,S=S))
      return mkstage(m,{'baz':mklens(rref_inner,S=S).foo.val})
    rref=realize(instantiate(_setup_outer,S=S))
    assert rref_inner is not None
    assert len(drefdeps([rref2dref(rref)],S=S))==0
    assert len(drefdeps([rref2dref(rref_inner)],S=S))==0
    assert mklens(rref_inner,S=S).foo.val=='bar'
    assert mklens(rref,S=S).baz.val=='bar'


def test_config_ro():
  d={'a':1,'b':33}
  c=mkconfig(d)
  cro=config_cattrs(RConfig(config_dict(c))) # We sure we don't have promises here
  for k in d.keys():
    assert getattr(cro,k) == d[k]


def test_mksymlink()->None:
  with setup_storage2('test_mksymlink') as (T,S):
    tp=T

    def _setting1(m:Manager)->DRef:
      return mkstage(m, {'a':'1'}, lambda i:33, buildtime=False)
    def _setting2(m:Manager)->DRef:
      return mkstage(m, {'a':'1'}, lambda i:42, buildtime=True)

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
  with setup_storage2('test_ignored_stage') as (T,S):
    n1:DRef; n2:DRef; n3:DRef; n4:DRef
    def _setting(m:Manager)->DRef:
      nonlocal n1, n2, n3, n4
      n1 = mkstage(m, {'a':'1'})
      n2 = mkstage(m, {'b':'2'}) # this one should not be realized
      n3 = mkstage(m, {'c':'3', 'maman':n1})
      n4 = mkstage(m, {'c':'4', 'papa':n3}) # neither this one
      return n3

    cl=instantiate(_setting,S=S)
    rref = realize(cl)
    rrefs:List[RRef] = []
    all_drefs = list(alldrefs(S))
    assert len(all_drefs)==4
    assert len(list(drefrrefs(n1,S)))==1
    assert len(list(drefrrefs(n2,S)))==0
    assert len(list(drefrrefs(n3,S)))==1
    assert len(list(drefrrefs(n4,S)))==0


def test_overwrite_realizer()->None:
  with setup_storage2('test_overwrite_realizer') as (T,S):
    n1:DRef; n2:DRef; n3:DRef; n4:DRef
    def _setting(m:Manager)->DRef:
      nonlocal n1, n2, n3, n4
      n1 = mkstage(m, {'a':'1'}, lambda i:33)
      n2 = mkstage(m, {'maman':n1})
      n3 = mkstage(m, {'a':'1'}, lambda i:42)
      assert n1 == n3
      return n2

    rref_n2=realize(instantiate(_setting, S=S))
    all_drefs = list(alldrefs(S))
    assert len(all_drefs)==2

    rref_n3=context_deref(rrefctx(rref_n2,S), rrefattrs(rref_n2, S).maman)[0]
    assert open(join(rref2path(rref_n3, S),'artifact'),'r').read() == '42'



def test_gc()->None:
  with setup_storage2('test_gc') as (T,S):
    def _node1(m:Manager)->DRef:
      return mkstage(m, {'name':'1'})
    def _node2(m:Manager)->DRef:
      return mkstage(m, {'name':'2', 'maman':_node1(m)})
    def _node3(m:Manager)->DRef:
      return mkstage(m, {'name':'3', 'maman':_node1(m)})

    r1=realize(instantiate(_node1,S=S))
    r2=realize(instantiate(_node2,S=S))
    r3=realize(instantiate(_node3,S=S))

    rm_drefs,rm_rrefs=store_gc([],[r2],S)
    assert rm_drefs=={rref2dref(r) for r in [r3]}
    assert rm_rrefs=={x for x in [r3]}

# def test_promise()->None:
#   with setup_storage2('test_promise') as (T,S):
#     def _setting(m:Manager, fullfill:bool)->DRef:
#       n1=mkstage(m, {'name':'1', 'promise':[promise,'artifact']})
#       def _realize(b:Build):
#         o=build_outpath(b)
#         c=build_cattrs(b)
#         assert b.dref in c.promise
#         assert n1 in store_cattrs(c.maman,S).promise
#         assert build_path(b,c.promise)==join(o,'uber-artifact')
#         assert build_path(b,store_cattrs(c.maman,S).promise)==build_path(b,c.maman_promise)
#         if fullfill:
#           with open(build_path(b,c.promise),'w') as f:
#             f.write('chickenpoop')

#       return mkdrv(m, mkconfig({'name':'2', 'maman':n1,
#                                 'promise':[promise,'uber-artifact'],
#                                 'maman_promise':[n1,'artifact']}),
#                       matcher=match_only(),
#                       realizer=build_wrapper(_realize))

#     try:
#       rref=realize(instantiate(_setting,False,S=S))
#       raise ShouldHaveFailed('Promise trigger')
#     except AssertionError:
#       pass
#     rref=realize(instantiate(_setting,True,S=S))
#     assert_valid_rref(rref)

# def test_path2rref()->None:
#   with setup_storage2('test_path2rref') as (T,S):
#     s1=partial(mkstage, config={'name':'1', 'promise':[promise,'artifact']})
#     rref1=realize(instantiate(s1,S=S))
#     rref2=path2rref(rref2path(rref1,S))
#     assert rref1==rref2
#     l=mksymlink(rref1, S, 'result', S=S)
#     assert path2rref(Path(l))==rref1
#     rref3=path2rref(Path("/foo/00000000000000000000000000000000-bar/11111111111111111111111111111111"))
#     assert rref3=='rref:11111111111111111111111111111111-00000000000000000000000000000000-bar'
#     for x in [path2rref(Path('')),path2rref(Path('foo'))]:
#       assert x is None

# def test_path2dref()->None:
#   with setup_storage2('test_path2dref') as (T,S):
#     s1=partial(mkstage, config={'name':'1', 'promise':[promise,'artifact']})
#     clo1=instantiate(s1,S=S)
#     dref1=clo1.dref
#     rref1=realize(clo1)
#     dref2=path2dref(dref2path(rref2dref(rref1),S=S))
#     assert dref1==dref2
#     l=linkdref(dref1, S, 'result_dref', S=S)
#     assert path2dref(Path(l))==dref1
#     dref3=path2dref(Path("/foo/00000000000000000000000000000000-bar"))
#     assert dref3=='dref:00000000000000000000000000000000-bar'
#     for x in [path2dref(Path('')),path2dref(Path('foo'))]:
#       assert x is None

# def test_linkrrefs()->None:
#   with setup_storage2('test_linkrefs') as (T,S):
#     s1=partial(mkstage, config={'name':'1', 'promise':[promise,'artifact']})
#     rref1=realize(instantiate(s1,S=S))
#     l=linkrrefs([rref1, rref1], destdir=S, S=S)
#     assert len(l)==2
#     assert str(l[0])==join(S,'result-1')
#     assert islink(join(S,'result-1'))
#     l=linkrrefs([rref1], destdir=S, withtime=True, S=S)
#     assert S in l[0]

