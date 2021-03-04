from pylightnix import (instantiate, DRef, RRef, Path, SPath, mklogdir,
                        dirhash, assert_valid_dref, assert_valid_rref,
                        store_deps, store_deepdeps, store_gc,
                        assert_valid_hash, assert_valid_config, Manager,
                        mkcontext, mkrgroup, store_rrefs, mkdref, mkrref,
                        unrref, undref, realize, rref2dref, store_config,
                        mkconfig, Build, Context, build_outpath, match_only,
                        mkdrv, store_deref, store_rref2path, store_rrefs_,
                        config_cattrs, mksymlink, store_cattrs, build_deref,
                        build_path, mkrefpath, build_config, alldrefs,
                        store_rrefs, build_wrapper, build_cattrs, build_name,
                        match_best, tryread, trywrite, match, latest, best,
                        exact, Key, match_latest, match_all, match_some,
                        match_n, realizeMany, build_outpaths, scanref_dict,
                        config_dict, promise, mklens, isrref, Config, RConfig,
                        build_setoutpaths, partial, path2rref, Tag, Group,
                        RRefGroup, concat, linkrrefs, instantiate_,
                        store_dref2path, path2dref, linkdref, storage,
                        store_deepdepRrefs, drefrrefs, allrrefs, realizeGroups,
                        tag_out, groups2rrefs)

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, islink, List, randint, sleep, rmtree,
                           system, S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen,
                           PIPE, data, event, settings, reproduce_failure)

from tests.generators import (rrefs, drefs, configs, dicts, rootstages)

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
      deps |= store_deepdeps([clo.dref],S) | set([clo.dref])
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
      deps|=store_deepdepRrefs(rrefs,S) | set(rrefs)
    assert deps<=set(allrrefs(S))


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


