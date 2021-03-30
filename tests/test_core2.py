from pylightnix import (instantiate, DRef, RRef, Path, SPath, mklogdir,
                        dirhash, assert_valid_dref, assert_valid_rref,
                        drefdeps1, drefdeps, store_gc,
                        assert_valid_hash, assert_valid_config, Manager,
                        mkcontext, allrrefs, mkdref, mkrref,
                        unrref, undref, realize, rref2dref, drefcfg,
                        mkconfig, Build, Context, build_outpath, match_some,
                        mkdrv, store_deref, store_rref2path, store_rrefs_,
                        config_cattrs, mksymlink, store_cattrs, build_deref,
                        build_path, mkrefpath, build_config, alldrefs,
                        store_rrefs, build_wrapper, build_cattrs, build_name,
                        match_best, tryread, trywrite, latest, best, exact,
                        Key, match_latest, match_all, realizeMany,
                        build_outpaths, scanref_dict, config_dict, promise,
                        mklens, isrref, Config, RConfig, build_setoutpaths,
                        partial, path2rref, Tag, Group, RRefGroup, concat,
                        linkrrefs, instantiate_, store_dref2path, path2dref,
                        linkdref, storage, rrefdeps, drefrrefs,
                        allrrefs, realizeGroups, tag_out, groups2rrefs,
                        redefine, match_only, readstr, match_exact, group2sign)

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, islink, List, randint, sleep, rmtree,
                           system, S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen,
                           PIPE, data, event, settings, reproduce_failure,
                           lists)

from tests.generators import (rrefs, drefs, configs, dicts, rootstages,
                              integers)

from tests.setup import ( ShouldHaveFailed, setup_storage, setup_storage2,
                         mkstage, mkstage, pipe_stdout )


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
@settings(print_blob=True)
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

@settings(deadline=None)
@given(stages=rootstages())
def test_group_invariants(stages):
  """ Group invariants should be fulfilled. """
  with setup_storage2('test_group_invariants') as (T,S):
    event(f"Number of top-level stages: {len(stages)}")
    for stage in stages:
      rgs=realizeGroups(instantiate(stage,S=S))
      assert len(set(groups2rrefs(rgs)))==len(groups2rrefs(rgs))
      event(f"Number of output groups: {len(rgs)}")
      for rg in rgs:
        event(f"Number of output tags: {len(rg.keys())}")
        assert len(rg.keys())>=1
        assert len(set([rref2dref(rref) for rref in rg.values()]))==1
        assert tag_out() in rg.keys()
        assert len(set(rg.keys()))==len(rg.keys())

@settings(max_examples=10)
@given(stages=rootstages(max_size=3, partial_matches=False))
def test_match_only(stages):
  with setup_storage2('test_match_only') as (T,S):
    for stage in stages:
      try:
        rgs=realizeGroups(
              instantiate(
                redefine(stage,new_matcher=match_only()), S=S))
        assert len(rgs)==1
        event('match_only positive')
      except AssertionError:
        rgs=realizeGroups(instantiate(stage,S=S))
        assert len(rgs)!=1
        event('match_only negative')

@settings(max_examples=10)
@given(stages=rootstages(max_size=3, partial_matches=False),
       n=integers(min_value=0, max_value=3))
def test_match_some(stages,n):
  with setup_storage2('test_match_some') as (T,S):
    for stage in stages:
      try:
        rgs=realizeGroups(
              instantiate(
                redefine(stage,new_matcher=match_some(n)), S=S))
        assert len(rgs)>=n
        event('match_some positive')
      except AssertionError:
        rgs=realizeGroups(instantiate(stage,S=S))
        assert len(rgs)<n
        event('match_some negative')

@settings(max_examples=30,print_blob=True)
@given(stages=rootstages(max_size=3, partial_matches=False),
       topN=integers(min_value=1, max_value=3))
def test_match_best(stages,topN):
  with setup_storage2('test_match_best') as (T,S):
    def _artifact(rg)->float:
      return float(readstr(join(mklens(rg[tag_out()],S=S).syspath,"artifact")))
    for stage in stages:
      artsM=[_artifact(g) for g in realizeGroups(
             instantiate(
               redefine(stage,new_matcher=match_best("artifact", topN=topN)), S=S))]
      arts=[_artifact(g) for g in realizeGroups(
             instantiate(stage, S=S))]
      event(f'match_best topN {topN}')
      event(f'match_best ngroups {len(arts)}')
      assert sorted(artsM)==sorted(arts)[-len(artsM):]

@settings(max_examples=30,print_blob=True)
@given(stages=rootstages(max_size=3, partial_matches=False),
       subs=lists(integers(min_value=1, max_value=3),max_size=3))
def test_match_exact(stages,subs):
  with setup_storage2('test_match_exact') as (T,S):
    for stage in stages:
      grs=realizeGroups(
             instantiate(stage, S=S))
      subset=[grs[s%len(grs)] for s in subs]
      try:
        grsM=realizeGroups(
               instantiate(
                 redefine(stage,new_matcher=match_exact(subset)), S=S))
        desired=set([tuple(group2sign(g)) for g in subset])
        actual=set([tuple(group2sign(g)) for g in grsM])
        assert actual==desired
      except AssertionError:
        assert len(subset)==0

@settings(max_examples=30,print_blob=True)
@given(stages=rootstages(max_size=3, partial_matches=False))
def test_match_all(stages):
  with setup_storage2('test_match_all') as (T,S):
    for stage in stages:
        grs=realizeGroups(
              instantiate(
                redefine(stage,new_matcher=match_all()), S=S))
        assert len(grs)==0
        grs2=realizeGroups(instantiate(stage, S=S))
        grs3=realizeGroups(
              instantiate(
                redefine(stage,new_matcher=match_all()), S=S))
        assert len(grs3)==len(grs2)

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
#     assert tryread(Path(join(store_rref2path(rref2,S),'artifact')))==str('2_0')
#
#   with setup_storage2('test_match_latest') as (T,S):
#     clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=1, S=S)
#     rref1=realize(clo)
#     assert len(list(drefrrefs(clo.dref,S)))==1
#     sleep(0.01)
#     clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=2, buildtime=False, S=S)
#     rref2=realize(clo, force_rebuild=[clo.dref])
#     assert len(list(drefrrefs(clo.dref,S)))==2
#     assert tryread(Path(join(store_rref2path(rref2,S),'artifact')))==str('1_0')
#
#   for i in range(10):
#     with setup_storage2('test_match_latest') as (T,S):
#       nouts=randint(1,10)
#       ntop=randint(1,10)
#       try:
#         clo=instantiate(_mknode, {'a':0}, match_latest(ntop), nouts, S=S)
#         rrefs=realizeMany(clo)
#         times=set([tryread(Path(join(store_rref2path(rref,S),'__buildtime__.txt'))) for rref in rrefs])
#         assert len(list(times))==1
#       except AssertionError:
#         assert ntop>nouts
