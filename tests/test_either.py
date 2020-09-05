from pylightnix import (instantiate, DRef, RRef, assert_valid_rref, Manager,
                        realize, mklens, either_wrapper, claim, readstr)

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, List, randint, sleep, rmtree, system,
                           S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen, PIPE)

from tests.generators import (rrefs, drefs, configs, dicts)

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


