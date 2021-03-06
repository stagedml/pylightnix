from pylightnix import (instantiate, DRef, RRef, assert_valid_rref, Manager,
                        Build, realize, mklens, either_wrapper, claim, readstr,
                        mkconfig, mkdrv, match_only, build_wrapper,
                        build_setoutpaths, either_status, either_isRight,
                        either_isLeft, realizeMany, rref2path, match_some)

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, List, randint, sleep, rmtree, system,
                           S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen, PIPE)

from tests.generators import (drefs, configs, dicts)

from tests.setup import (ShouldHaveFailed, setup_testpath, setup_storage,
                         mktestnode_nondetermenistic, mktestnode)


def mkeither(m, source, should_fail=False):
  def _mutate():
    if should_fail:
      raise ValueError('Expected test error')
    else:
      return 33
  return mktestnode_nondetermenistic(m, source,
                                     realize_wrapper=either_wrapper,
                                     nondet=_mutate,
                                     promise_strength=claim)

def test_either()->None:
  with setup_storage('test_either'):
    def _setting(m:Manager)->DRef:
      n1 = mkeither(m, {'name':'n1', 'foo':'bar'})
      n2 = mkeither(m, {'name':'n2', 'bar':'baz'}, should_fail=True)
      n3 = mkeither(m, {'name':'n3', 'maman':n1, 'papa':n2})
      return n3

    rref = realize(instantiate(_setting))
    assert_valid_rref(rref)
    assert mklens(rref).name.val=='n3'
    assert readstr(join(mklens(rref).syspath, 'status_either.txt'))=='LEFT'
    assert readstr(join(mklens(rref).maman.syspath, 'status_either.txt'))=='RIGHT'
    assert readstr(join(mklens(rref).papa.syspath, 'status_either.txt'))=='LEFT'
    assert isfile(join(mklens(rref).papa.syspath, 'exception.txt'))

def test_either_success()->None:
  with setup_storage('test_either_success'):
    def _setting(m:Manager)->DRef:
      n1 = mkeither(m, {'name':'n1', 'foo':'bar'})
      def _make(b:Build):
        build_setoutpaths(b, 1)
        assert mklens(b).name.val=='n2'
      return mkdrv(m, mkconfig({'name':'n2', 'maman':n1}),
                   match_only(), either_wrapper(build_wrapper(_make)))

    rref = realize(instantiate(_setting))
    assert_valid_rref(rref)
    assert mklens(rref).maman.name.val=='n1'
    assert mklens(rref).name.val=='n2'
    assert either_isRight(rref), either_status(rref)
    assert not either_isLeft(rref), either_status(rref)

def test_either_builderror()->None:
  with setup_storage('test_either_builderror'):
    def _setting(m:Manager)->DRef:
      def _make(b:Build):
        build_setoutpaths(b, 2)
        raise ValueError('Ooops')
      return mkdrv(m, mkconfig({'name':'pigfood'}),
                   match_some(n=2), either_wrapper(build_wrapper(_make)))

    rrefs = realizeMany(instantiate(_setting))
    assert len(rrefs)==2
    for rref in rrefs:
      assert_valid_rref(rref)
      assert either_isLeft(rref), either_status(rref)
      assert isfile(join(rref2path(rref),'exception.txt'))

