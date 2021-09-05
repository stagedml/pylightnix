from pylightnix import (Registry, DRef, RRef, Path, List, mklogdir, dirhash,
                        rref2path, mkcontext, instantiate, realize1,
                        assert_valid_rref, alldrefs, assert_valid_dref,
                        repl_realize, repl_cancel, repl_continue, repl_rref,
                        repl_build, ReplHelper, build_outpath, tryread,
                        repl_continueBuild, isrref, context_deref, rrefctx,
                        output_validate, repl_result, repl_continueAll,
                        repl_realize, Tuple, Closure)

from tests.imports import (
    given, assume, example, note, settings, text, decimals, integers, rmtree,
    characters, gettempdir, isdir, join, makedirs, from_regex, islink, listdir,
    get_executable, run, dictionaries, one_of, lists, recursive, printable,
    none, booleans, floats, re_compile, composite, event, isfile )

from tests.generators import (
    configs, dicts, artifacts )

from tests.setup import ( setup_storage2, mkstage, mkstage, ShouldHaveFailed )


def test_repl_basic():
  with setup_storage2('test_repl_default') as S:

    n1:DRef; n2:DRef
    def _setting(r:Registry)->List[DRef]:
      nonlocal n1,n2
      n1 = mkstage({'a':'1'},r)
      n2 = mkstage({'maman':n1},r)
      return [n1,n2]

    x:Tuple[List[DRef],Closure]=instantiate(_setting,S=S)
    rh=repl_realize(x, force_interrupt=False)
    assert repl_result(rh) is not None
    rh=repl_realize(x, force_interrupt=[n1,n2])
    assert repl_result(rh) is None
    repl_continueAll(rh=rh)
    assert repl_result(rh) is None
    repl_continueAll(rh=rh)
    res=repl_result(rh)
    assert res is not None
    assert n1 in res
    assert n2 in res


def test_repl_race():
  with setup_storage2('test_repl_recursion') as S:

    def _setting(r:Registry)->DRef:
      n1 = mkstage({'a':'1'},r)
      n2 = mkstage({'maman':n1},r)
      return n2

    x:Tuple[DRef,Closure]=instantiate(_setting,S=S)
    rh=repl_realize(x, force_interrupt=True)
    assert repl_rref(rh) is None
    assert rh.result is None

    x2:Tuple[DRef,Closure]=instantiate(_setting,S=S)
    rref2=realize1(x2) # Realize dref while repl_realizing the same dref

    repl_cancel(rh)
    assert_valid_rref(rref2)


def test_repl_override():
  with setup_storage2('test_repl_override') as S:

    n1:DRef; n2:DRef
    def _setting(r:Registry)->DRef:
      nonlocal n1,n2
      n1 = mkstage({'a':'1'}, r, lambda i: 33)
      n2 = mkstage({'maman':n1}, r, lambda i: 42)
      return n2

    x:Tuple[DRef,Closure]=instantiate(_setting, S=S)
    rh=repl_realize(x, force_interrupt=[n1])
    assert rh.result is None
    b=repl_build(rh)
    with open(join(build_outpath(b),'artifact'),'w') as f:
      f.write('777')
    assert b.outpaths is not None
    repl_continue(output_validate(b.dref, b.outpaths, S=b.S), rh=rh)
    rref=repl_rref(rh)
    assert rref is not None

    rrefn1=context_deref(rrefctx(rref,S=S),n1)[0]
    assert tryread(Path(join(rref2path(rrefn1,S=S),'artifact'))) == '777'



def test_repl_globalHelper():
  with setup_storage2('test_repl_globalHelper') as S:

    n1:DRef; n2:DRef
    def _setting(r:Registry)->DRef:
      nonlocal n1,n2
      n1 = mkstage({'a':'1'},r)
      n2 = mkstage({'maman':n1},r)
      return n2

    rh=repl_realize(instantiate(_setting, S=S), force_interrupt=True)
    assert repl_rref(rh) is None
    b=repl_build()
    with open(join(build_outpath(b),'artifact.txt'), 'w') as f:
      f.write("Fooo")
    repl_continueBuild(b)
    rref=repl_rref(rh)
    assert rref is not None
    assert isfile(join(rref2path(rref,S=S),'artifact.txt'))


def test_repl_globalCancel():
  with setup_storage2('test_repl_globalCancel') as S:

    n1:DRef; n2:DRef
    def _setting(r:Registry)->DRef:
      nonlocal n1,n2
      n1 = mkstage({'a':'1'},r)
      n2 = mkstage({'maman':n1},r)
      return n2

    rh=repl_realize(instantiate(_setting,S=S), force_interrupt=True)
    assert repl_rref(rh) is None
    repl_cancel()
    assert rh.gen is None
    rref=realize1(instantiate(_setting, S=S))
    assert isrref(rref)


def test_repl_realizeInval():
  with setup_storage2('test_repl_realizeInval') as S:
    try:
      repl_realize(instantiate(mkstage, {'a':1}, S=S),
                   force_interrupt=33) #type:ignore
      raise ShouldHaveFailed('wrong force_interrupt value')
    except AssertionError:
      pass
