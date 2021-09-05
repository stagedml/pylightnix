from pylightnix import (SPath, Context, RealizeArg, Path, instantiate, DRef,
                        RRef, assert_valid_rref, Registry, Build, realize1,
                        mklens, either_realizer, readstr, mkconfig, mkdrv,
                        build_wrapper, either_status,
                        either_isRight, either_isLeft, realizeMany, rref2path,
                        match_only, writestr, match_some, Output,
                        allrrefs, rrefdeps1, realizeE, either_paths,
                        either_loadR, either_status, realizeManyE)

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, List, randint, sleep, rmtree, system,
                           S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen, PIPE,
                           settings, event, reproduce_failure)

from tests.generators import (rrefs, drefs, configs, dicts, rootstages,
                              integers)

from tests.setup import (ShouldHaveFailed, mkstage, setup_test_config,
                         setup_test_match, setup_test_realize, setup_storage2,
                         rrefdepth, DELIBERATE_TEST_FAILURE)

from pylightnix.either import (Either, mkdrvE)

def mkstageE(r:Registry,
            config:dict,
            nondet:Callable[[int],int]=lambda n:0,
            buildstart:Optional[str]='AUTO',
            nrrefs:int=1,
            nmatch:int=1,
            mustfail:bool=False)->DRef:
  def _r(S, dref:DRef, c:Context, ra:RealizeArg)->Output[Path]:
    r=setup_test_realize(nrrefs, buildstart, nondet, mustfail)
    return r(S,dref,c,ra)
  return mkdrvE(setup_test_config(config), setup_test_match(nmatch), _r, r)

@given(stages=rootstages(stagefn=mkstageE, failchances=[50]))
def test_either_invariant(stages):
  with setup_storage2('test_either_invariant') as S:
    for stage in stages:
      e=realizeManyE(instantiate(stage,S=S))
      depth=max([rrefdepth(rref,S) for rref in either_paths(e)])
      assert not (either_isLeft(e) and either_isRight(e))
      assert (either_isLeft(e) or either_isRight(e))
      if either_isRight(e):
        event(f'Right')
        assert either_status(e) is None
      elif either_isLeft(e):
        event(f'Left')
        assert DELIBERATE_TEST_FAILURE in str(either_status(e))
      else:
        assert False
    for rref in allrrefs(S=S):
      assert not (either_isRight(either_loadR([rref],S)) and
                  either_isLeft(either_loadR(list(rrefdeps1([rref],S=S)),S)))


# def mkeither(r, source, should_fail=False):
#   def _mutate(i):
#     if should_fail:
#       raise ValueError('Expected test error')
#     else:
#       return 33
#   return mkstage(r, source, realize_wrapper=either_wrapper, nondet=_mutate)

# def test_either()->None:
#   with setup_storage('test_either'):
#     def _setting(r:Registry)->DRef:
#       n1 = mkeither(r, {'name':'n1', 'foo':'bar'})
#       n2 = mkeither(r, {'name':'n2', 'bar':'baz'}, should_fail=True)
#       n3 = mkeither(r, {'name':'n3', 'maman':n1, 'papa':n2})
#       return n3

#     rref = realize1(instantiate(_setting))
#     assert_valid_rref(rref)
#     assert mklens(rref).name.val=='n3'
#     assert readstr(join(mklens(rref).syspath, 'status_either.txt'))=='LEFT'
#     assert readstr(join(mklens(rref).maman.syspath, 'status_either.txt'))=='RIGHT'
#     assert readstr(join(mklens(rref).papa.syspath, 'status_either.txt'))=='LEFT'
#     assert isfile(join(mklens(rref).papa.syspath, 'exception.txt'))

# def test_either_success()->None:
#   with setup_storage('test_either_success'):
#     def _setting(r:Registry)->DRef:
#       n1 = mkeither(r, {'name':'n1', 'foo':'bar'})
#       def _make(b:Build):
#         build_setoutpaths(b, 1)
#         assert mklens(b).name.val=='n2'
#       return mkdrv(r, mkconfig({'name':'n2', 'maman':n1}),
#                    match_only(), either_wrapper(build_wrapper(_make)))

#     rref = realize1(instantiate(_setting))
#     assert_valid_rref(rref)
#     assert mklens(rref).maman.name.val=='n1'
#     assert mklens(rref).name.val=='n2'
#     assert either_isRight(rref), either_status(rref)
#     assert not either_isLeft(rref), either_status(rref)

# def test_either_builderror()->None:
#   with setup_storage2('test_either_builderror') as T,S:
#     def _setting(r:Registry)->DRef:
#       def _make(b:Build):
#         # Make both paths differ from each other
#         for p in build_setoutpaths(b, 2):
#           writestr(join(p,'artifact.txt'), p)
#         raise ValueError('Ooops (an intended test failure)')
#       return mkdrvE(r, mkconfig({'name':'pigfood'}),
#                    match_some(2), either_wrapper(build_wrapper(_make)))

#     rrefs = realizeMany(instantiate(_setting))
#     assert len(rrefs)==2
#     for rref in rrefs:
#       assert_valid_rref(rref)
#       assert either_isLeft(rref), either_status(rref)
#       assert isfile(join(rref2path(rref),'exception.txt'))

