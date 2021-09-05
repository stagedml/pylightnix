from pylightnix import (instantiate, DRef, RRef, Path, SPath, drefdeps,
                        Registry, Context, RealizeArg, Output, realize1,
                        rref2dref, Build, match_some, mkdrv, rref2path,
                        alldrefs, build_wrapper, tryread, trywrite,
                        realizeMany, build_outpaths, mklens, Config,
                        rrefdeps, drefrrefs, allrrefs,
                        realizeMany, redefine, match_only, PromiseException,
                        output_matcher, output_realizer, cfgsp, drefcfg_,
                        rootrrefs, rootdrefs, match_exact, match_latest,
                        timestring, rrefbstart, parsetime)

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, islink, List, randint, sleep, rmtree,
                           system, S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen,
                           PIPE, data, event, settings, reproduce_failure,
                           lists, remove, isfile, isdir, note, partial)

from tests.generators import (rrefs, drefs, configs, dicts, rootstages,
                              integers, composite, hierarchies)

from tests.setup import ( ShouldHaveFailed, setup_storage2, mkstage, mkstage,
                         pipe_stdout , setup_test_realize, setup_test_match,
                         setup_test_config, mkstageP)


@given(stages=rootstages())
def test_union_of_root_derivations(stages):
  """ Union of dep.closures of root derivations must be equal to the set of all
  derivations. """
  with setup_storage2('test_union_of_root_derivations') as S:
    deps=set()
    for stage in stages:
      _,clo=instantiate(stage,S=S)
      deps |= drefdeps([clo.targets[0]],S) | set([clo.targets[0]])
    assert deps==set(alldrefs(S))


# @reproduce_failure('5.30.0', b'AAABAAAA')
@given(stages=rootstages())
def test_union_of_root_realizations(stages):
  """ Union of dep.closures of root realizations must be less or equal to the
  set of all realizations. Less - because realizer may produce more
  realizations then the matcher matches"""
  with setup_storage2('test_union_of_root_realizations') as S:
    deps=set()
    for stage in stages:
      rrefs=realizeMany(instantiate(stage,S=S))
      deps|=rrefdeps(rrefs,S) | set(rrefs)
    assert deps<=set(allrrefs(S))

# @given(stages=rootstages())
# def test_group_invariants(stages):
#   """ Group invariants should be fulfilled. """
#   with setup_storage2('test_group_invariants') as S:
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
  with setup_storage2('test_match_only') as S:
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
       n=integers(min_value=1, max_value=3))
def test_match_some(stages,n):
  with setup_storage2('test_match_some') as S:
    for stage in stages:
      try:
        rrefs=realizeMany(
              instantiate(
                redefine(stage,new_matcher=match_some(n)), S=S))
        assert len(rrefs)==n
        event('match_some positive')
      except AssertionError:
        rrefs=realizeMany(instantiate(stage,S=S))
        assert len(rrefs)<n
        event('match_some negative')


# @settings(max_examples=30)
# @given(stages=rootstages(max_size=3, partial_matches=False),
#        topN=integers(min_value=1, max_value=3))
# def test_match_best(stages,topN):
#   with setup_storage2('test_match_best') as S:
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

@settings(max_examples=30)
@given(stages=rootstages(max_size=3, partial_matches=False),
       subs=lists(integers(min_value=1, max_value=3),max_size=3))
def test_match_exact(stages,subs):
  with setup_storage2('test_match_exact') as S:
    for stage in stages:
      rrefs=realizeMany(instantiate(stage, S=S))
      note(f"rrefs {rrefs}")
      subset=list(set(rrefs[s%len(rrefs)] for s in subs))
      note(f"subset {subset}")
      try:
        actual=realizeMany(instantiate(
          redefine(stage,new_matcher=match_exact(subset)), S=S))
        note(f"actual {actual}")
        assert set(actual)==set(subset)
      except AssertionError:
        assert len(subset)==0

# @settings(max_examples=30)
# @given(stages=rootstages(max_size=3, partial_matches=False))
# def test_match_all(stages):
#   with setup_storage2('test_match_all') as S:
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


# def mkstageL(draw, r:Registry, name:str, artifact:int, buildstart:str)->DRef:
#   def _r(S, dref:DRef, c:Context, ra:RealizeArg)->Output[Path]:
#     r=setup_test_realize(1, buildstart, lambda i:artifact, mustfail=False)
#     return r(S,dref,c,ra)
#   return mkdrv(r, setup_test_config({'name':name}),
#                   output_matcher(setup_test_match(1)),
#                   output_realizer(_r))

@composite
def stagesL(draw):
  return (lambda r,cfg,t,a:mkdrv(setup_test_config(cfg),
                  match_latest(),
                  output_realizer(setup_test_realize(
                    1, timestring(sec=float(t)), lambda i:a, False)), r))

@given(h=hierarchies(stages=stagesL))
def test_match_latest(h):
  with setup_storage2('test_match_latest') as S:
    for t in range(3):
      note(f"t={t}")
      _,clo=instantiate(h, t=t, a=t, S=S)
      rrefs=realizeMany(clo, force_rebuild=[d.dref for d in clo.derivations])
      for rref in rrefdeps(rrefs,S=S)|set(rrefs):
        bstart=rrefbstart(rref,S=S)
        assert bstart is not None
        note(f"{rref}: bstart {bstart}")
        assert parsetime(bstart)==t

# FIXME: repair this test
# def test_match_latest()->None:
#   def _mknode(r, cfg, matcher, nouts:int, data=0, buildtime=True):
#     def _realize(b:Build)->None:
#       build_setoutpaths(b,nouts)
#       for i,out in enumerate(build_outpaths(b)):
#         assert trywrite(Path(join(out,'artifact')),str(data)+'_'+str(i))
#     return mkdrv(r, Config(cfg), matcher,
#                     build_wrapper(_realize, buildtime=buildtime))
#
#   with setup_storage2('test_match_latest') as S:
#     clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=1, S=S)
#     rref1=realize1(clo)
#     assert len(list(drefrrefs(clo.dref,S)))==1
#     sleep(0.01)
#     clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=2, S=S)
#     rref2=realize1(clo, force_rebuild=[clo.dref])
#     assert len(list(drefrrefs(clo.dref,S)))==2
#     assert tryread(Path(join(rref2path(rref2,S),'artifact')))==str('2_0')
#
#   with setup_storage2('test_match_latest') as S:
#     clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=1, S=S)
#     rref1=realize1(clo)
#     assert len(list(drefrrefs(clo.dref,S)))==1
#     sleep(0.01)
#     clo=instantiate(_mknode, {'a':0}, match_latest(1), nouts=1, data=2, buildtime=False, S=S)
#     rref2=realize1(clo, force_rebuild=[clo.dref])
#     assert len(list(drefrrefs(clo.dref,S)))==2
#     assert tryread(Path(join(rref2path(rref2,S),'artifact')))==str('1_0')
#
#   for i in range(10):
#     with setup_storage2('test_match_latest') as S:
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
  with setup_storage2('test_promise') as S:
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
  with setup_storage2('test_root_rrefs') as S:
    assert len(rootrrefs(S))==0
    results=set()
    for stage in stages:
      rrefs=realizeMany(instantiate(stage,S=S))
      results |= set(rrefs)
    roots=rootrrefs(S)
    for rref in results:
      assert rref in roots


@given(stages=rootstages())
def test_root_drefs(stages):
  """ Check that rootdrefs really enumerates roots """
  with setup_storage2('test_root_drefs') as S:
    assert len(rootdrefs(S))==0
    results=set()
    for stage in stages:
      results |= set([instantiate(stage,S=S)[1].targets[0]])
    roots=rootdrefs(S)
    for dref in results:
      assert dref in roots

