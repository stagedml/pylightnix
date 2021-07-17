from pylightnix import (instantiate, DRef, RRef, Path, SPath, drefdeps,
                        Manager, Context, RealizeArg, Output, realize,
                        rref2dref, Build, match_some, mkdrv, rref2path,
                        alldrefs, build_wrapper, tryread, trywrite,
                        realizeMany, build_outpaths, mklens, Config,
                        rrefdeps, drefrrefs, allrrefs,
                        realizeMany, redefine, match_only, PromiseException,
                        output_matcher, output_realizer, cfgsp, drefcfg_,
                        rootrrefs, rootdrefs)

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, islink, List, randint, sleep, rmtree,
                           system, S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen,
                           PIPE, data, event, settings, reproduce_failure,
                           lists, remove, isfile, isdir)

from tests.generators import (rrefs, drefs, configs, dicts, rootstages,
                              integers)

from tests.setup import ( ShouldHaveFailed, setup_storage, setup_storage2,
                         mkstage, mkstage, pipe_stdout , setup_test_realize,
                         setup_test_match, setup_test_config, mkstageP)


@settings(print_blob=True, deadline=None)
@given(stages=rootstages())
def test_union_of_root_derivations(stages):
  """ Union of dep.closures of root derivations must be equal to the set of all
  derivations. """
  with setup_storage2('test_union_of_root_derivations') as (T,S):
    deps=set()
    for stage in stages:
      clo=instantiate(stage,S=S)
      deps |= drefdeps([clo.dref],S) | set([clo.dref])
    assert deps==set(alldrefs(S))


# @reproduce_failure('5.30.0', b'AAABAAAA')
@settings(print_blob=True, deadline=None)
@given(stages=rootstages())
def test_union_of_root_realizations(stages):
  """ Union of dep.closures of root realizations must be less or equal to the
  set of all realizations. Less - because realizer may produce more
  realizations then the matcher matches"""
  with setup_storage2('test_union_of_root_realizations') as (T,S):
    deps=set()
    for stage in stages:
      rrefs=realizeMany(instantiate(stage,S=S))
      deps|=rrefdeps(rrefs,S) | set(rrefs)
    assert deps<=set(allrrefs(S))

# @settings(deadline=None)
# @given(stages=rootstages())
# def test_group_invariants(stages):
#   """ Group invariants should be fulfilled. """
#   with setup_storage2('test_group_invariants') as (T,S):
#     event(f"Number of top-level stages: {len(stages)}")
#     for stage in stages:
#       rgs=realizeGroups(instantiate(stage,S=S))
#       assert len(set(groups2rrefs(rgs)))==len(groups2rrefs(rgs))
#       event(f"Number of output groups: {len(rgs)}")
#       for rg in rgs:
#         event(f"Number of output tags: {len(rg.keys())}")
#         assert len(rg.keys())>=1
#         assert len(set([rref2dref(rref) for rref in rg.values()]))==1
#         assert tag_out() in rg.keys()
#         assert len(set(rg.keys()))==len(rg.keys())

@settings(max_examples=10)
@given(stages=rootstages(max_size=3, partial_matches=False))
def test_match_only(stages):
  with setup_storage2('test_match_only') as (T,S):
    for stage in stages:
      try:
        rrefs=realizeMany(
              instantiate(
                redefine(stage,new_matcher=match_only()), S=S))
        assert len(rrefs)==1
        event('match_only positive')
      except AssertionError:
        rrefs=realizeMany(instantiate(stage,S=S))
        assert len(rrefs)!=1
        event('match_only negative')


@settings(max_examples=10)
@given(stages=rootstages(max_size=3, partial_matches=False),
       n=integers(min_value=0, max_value=3))
def test_match_some(stages,n):
  with setup_storage2('test_match_some') as (T,S):
    for stage in stages:
      try:
        rrefs=realizeMany(
              instantiate(
                redefine(stage,new_matcher=match_some(n)), S=S))
        assert len(rrefs)>=n
        event('match_some positive')
      except AssertionError:
        rrefs=realizeMany(instantiate(stage,S=S))
        assert len(rrefs)<n
        event('match_some negative')


# @settings(max_examples=30,print_blob=True)
# @given(stages=rootstages(max_size=3, partial_matches=False),
#        topN=integers(min_value=1, max_value=3))
# def test_match_best(stages,topN):
#   with setup_storage2('test_match_best') as (T,S):
#     def _artifact(rref)->float:
#       return float(readstr(join(mklens(rref,S=S).syspath,"artifact")))
#     for stage in stages:
#       artsM=[_artifact(g) for g in realizeMany(
#              instantiate(
#                redefine(stage,new_matcher=match_best("artifact", topN=topN)), S=S))]
#       arts=[_artifact(g) for g in realizeMany(
#              instantiate(stage, S=S))]
#       event(f'match_best topN {topN}')
#       event(f'match_best ngroups {len(arts)}')
#       assert sorted(artsM)==sorted(arts)[-len(artsM):]

# @settings(max_examples=30,print_blob=True)
# @given(stages=rootstages(max_size=3, partial_matches=False),
#        subs=lists(integers(min_value=1, max_value=3),max_size=3))
# def test_match_exact(stages,subs):
#   with setup_storage2('test_match_exact') as (T,S):
#     for stage in stages:
#       rrefs=realizeMany(instantiate(stage, S=S))
#       subset=[rrefs[s%len(rrefs)] for s in subs]
#       try:
#         rrefsM=realizeMany(
#                instantiate(
#                  redefine(stage,new_matcher=match_exact(subset)), S=S))
#         desired=set([tuple(group2sign(g)) for g in subset])
#         actual=set([tuple(rrefsM)])
#         assert actual==desired
#       except AssertionError:
#         assert len(subset)==0

# @settings(max_examples=30,print_blob=True)
# @given(stages=rootstages(max_size=3, partial_matches=False))
# def test_match_all(stages):
#   with setup_storage2('test_match_all') as (T,S):
#     for stage in stages:
#         grs=realizeGroups(
#               instantiate(
#                 redefine(stage,new_matcher=match_all()), S=S))
#         assert len(grs)==0
#         grs2=realizeGroups(instantiate(stage, S=S))
#         grs3=realizeGroups(
#               instantiate(
#                 redefine(stage,new_matcher=match_all()), S=S))
#         assert len(grs3)==len(grs2)

# FIXME: repair this test
# def test_match_latest()->None:
#   def _mknode(m, cfg, matcher, nouts:int, data=0, buildtime=True):
#     def _realize(b:Build)->None:
#       build_setoutpaths(b,nouts)
#       for i,out in enumerate(build_outpaths(b)):
#         assert trywrite(Path(join(out,'artifact')),str(data)+'_'+str(i))
#     return mkdrv(m, Config(cfg), matcher,
#                     build_wrapper(_realize, buildtime=buildtime))
#
#   with setup_storage2('test_match_latest') as (T,S):
#     clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=1, S=S)
#     rref1=realize(clo)
#     assert len(list(drefrrefs(clo.dref,S)))==1
#     sleep(0.01)
#     clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=2, S=S)
#     rref2=realize(clo, force_rebuild=[clo.dref])
#     assert len(list(drefrrefs(clo.dref,S)))==2
#     assert tryread(Path(join(rref2path(rref2,S),'artifact')))==str('2_0')
#
#   with setup_storage2('test_match_latest') as (T,S):
#     clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=1, S=S)
#     rref1=realize(clo)
#     assert len(list(drefrrefs(clo.dref,S)))==1
#     sleep(0.01)
#     clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=2, buildtime=False, S=S)
#     rref2=realize(clo, force_rebuild=[clo.dref])
#     assert len(list(drefrrefs(clo.dref,S)))==2
#     assert tryread(Path(join(rref2path(rref2,S),'artifact')))==str('1_0')
#
#   for i in range(10):
#     with setup_storage2('test_match_latest') as (T,S):
#       nouts=randint(1,10)
#       ntop=randint(1,10)
#       try:
#         clo=instantiate(_mknode, {'a':0}, match_latest(ntop), nouts, S=S)
#         rrefs=realizeMany(clo)
#         times=set([tryread(Path(join(rref2path(rref,S),'__buildtime__.txt'))) for rref in rrefs])
#         assert len(list(times))==1
#       except AssertionError:
#         assert ntop>nouts


@given(stages=rootstages(stagefn=mkstageP, failchances=[50]))
def test_promise(stages):
  with setup_storage2('test_promise') as (T,S):
    for stage in stages:
      try:
        rrefs=realizeMany(instantiate(stage, S=S))
        event('test_promise positive')
      except PromiseException as e:
        event('test_promise negative')
        for (p,rp) in e.failed:
          assert not isfile(join(p,*rp[1:]))
    for rref in allrrefs(S):
      for sp in cfgsp(drefcfg_(rref2dref(rref),S)):
        p=Path(join(rref2path(rref,S),*sp[1][1:]))
        assert isfile(p) or isdir(p)

@given(stages=rootstages())
def test_root_rrefs(stages):
  """ Check that rootrrefs really enumerates roots """
  with setup_storage2('test_root_rrefs') as (T,S):
    assert len(rootrrefs(S))==0
    results=set()
    for stage in stages:
      rrefs=realizeMany(instantiate(stage,S=S))
      results |= set(rrefs)
    roots=rootrrefs(S)
    for rref in results:
      assert rref in roots


@settings(deadline=None)
@given(stages=rootstages())
def test_root_drefs(stages):
  """ Check that rootdrefs really enumerates roots """
  with setup_storage2('test_root_drefs') as (T,S):
    assert len(rootdrefs(S))==0
    results=set()
    for stage in stages:
      results |= set([instantiate(stage,S=S).dref])
    roots=rootdrefs(S)
    for dref in results:
      assert dref in roots

