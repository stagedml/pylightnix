from pylightnix import ( Manager, DRef, RRef, Path, mklogdir, dirhash, mknode,
    store_deps, store_deepdeps, rref2path, Manager, mkcontext, instantiate,
    realize, instantiate_inplace, realize_inplace, assert_valid_rref,
    store_rrefs_, store_drefs, assert_valid_dref, repl_realize, repl_cancel,
    repl_continue, repl_rref, repl_build, ReplHelper, build_outpath,
    store_deref, tryread, repl_continueBuild )

from tests.imports import (
    given, assume, example, note, settings, text, decimals, integers, rmtree,
    characters, gettempdir, isdir, join, makedirs, from_regex, islink, listdir,
    get_executable, run, dictionaries, one_of, lists, recursive, printable,
    none, booleans, floats, re_compile, composite, event, isfile )

from tests.generators import (
    configs, dicts, artifacts )

from tests.setup import (
    setup_testpath, setup_storage, setup_inplace_reset,
    mktestnode_nondetermenistic, mktestnode, ShouldHaveFailed )

# def test_repl_null():
#   with setup_storage('test_repl_null'):

#   def _setting(m:Manager)->DRef:
#     nonlocal n1,n2
#     n1 = mktestnode(m, {'a':'1'})
#     n2 = mktestnode(m, {'maman':n1})
#     return n2

def test_repl_basic():
  with setup_storage('test_repl_default'):

    n1:DRef; n2:DRef
    def _setting(m:Manager)->DRef:
      nonlocal n1,n2
      n1 = mktestnode(m, {'a':'1'})
      n2 = mktestnode(m, {'maman':n1})
      return n2

    clo=instantiate(_setting)
    rh=repl_realize(clo, force_interrupt=False)
    assert repl_rref(rh) is not None

    rh=repl_realize(clo, force_interrupt=[n1,n2])
    assert repl_rref(rh) is None
    assert rh.dref==n1
    repl_continue(rh=rh)
    assert repl_rref(rh) is None
    assert rh.dref==n2
    repl_continue(rh=rh)
    assert repl_rref(rh) is not None


def test_repl_recursion():
  with setup_storage('test_repl_recursion'):

    def _setting(m:Manager)->DRef:
      n1 = mktestnode(m, {'a':'1'})
      n2 = mktestnode(m, {'maman':n1})
      return n2

    clo=instantiate(_setting)
    rh=repl_realize(clo, force_interrupt=True)
    assert repl_rref(rh) is None
    assert rh.dref==clo.dref

    clo2=instantiate(_setting)
    try:
      rref2=realize(clo2)
      raise ShouldHaveFailed("Recursion manager should have alerted")
    except AssertionError:
      pass

    repl_cancel(rh)
    rref2=realize(clo2)
    assert_valid_rref(rref2)


def test_repl_override():
  with setup_storage('test_repl_override'):

    n1:DRef; n2:DRef
    def _setting(m:Manager)->DRef:
      nonlocal n1,n2
      n1 = mktestnode_nondetermenistic(m, {'a':'1'}, lambda: 33)
      n2 = mktestnode_nondetermenistic(m, {'maman':n1}, lambda: 42)
      return n2

    clo=instantiate(_setting)
    rh=repl_realize(clo, force_interrupt=[n1])
    assert rh.dref==n1
    b=repl_build(rh)
    with open(join(build_outpath(b),'artifact'),'w') as f:
      f.write('777')
    repl_continue(rh=rh)
    rref=repl_rref(rh)
    assert rref is not None

    rrefn1=store_deref(rref, n1)
    assert tryread(Path(join(rref2path(rrefn1),'artifact'))) == '777'



def test_repl_globalHelper():
  with setup_storage('test_repl_globalHelper'):

    n1:DRef; n2:DRef
    def _setting(m:Manager)->DRef:
      nonlocal n1,n2
      n1 = mktestnode(m, {'a':'1'})
      n2 = mktestnode(m, {'maman':n1})
      return n2

    rh=repl_realize(instantiate(_setting), force_interrupt=True)
    assert repl_rref(rh) is None
    with open(join(build_outpath(repl_build()),'artifact.txt'), 'w') as f:
      f.write("Fooo")
    repl_continueBuild()
    rref=repl_rref(rh)
    assert rref is not None
    assert isfile(join(rref2path(rref),'artifact.txt'))


def test_repl_globalCancel():
  with setup_storage('test_repl_globalCancel'):

    n1:DRef; n2:DRef
    def _setting(m:Manager)->DRef:
      nonlocal n1,n2
      n1 = mktestnode(m, {'a':'1'})
      n2 = mktestnode(m, {'maman':n1})
      return n2

    rh=repl_realize(instantiate(_setting), force_interrupt=True)
    assert repl_rref(rh) is None
    repl_cancel()
    assert rh.gen is None


def test_repl_realizeInval():
  with setup_storage('test_repl_realizeInval'):
    try:
      repl_realize(instantiate(mktestnode, {'a':1}), force_interrupt=33) #type:ignore
      raise ShouldHaveFailed('wrong force_interrupt value')
    except AssertionError:
      pass
