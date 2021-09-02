from pylightnix import ( Manager, DRef, RRef, Path, List, mklogdir, dirhash,
                        rref2path, Manager, mkcontext, instantiate,
                        realize, instantiate_inplace, realize_inplace,
                        assert_valid_rref, alldrefs, assert_valid_dref,
                        repl_realize, repl_cancel, repl_continue, repl_rref,
                        repl_build, ReplHelper, build_outpath, tryread,
                        repl_continueBuild, isrref, context_deref, rrefctx,
                        output_validate )

from tests.imports import (
    given, assume, example, note, settings, text, decimals, integers, rmtree,
    characters, gettempdir, isdir, join, makedirs, from_regex, islink, listdir,
    get_executable, run, dictionaries, one_of, lists, recursive, printable,
    none, booleans, floats, re_compile, composite, event, isfile )

from tests.generators import (
    configs, dicts, artifacts )

from tests.setup import ( setup_storage2, setup_inplace_reset, mkstage, mkstage,
                         ShouldHaveFailed )

# def test_repl_null():
#   with setup_storage('test_repl_null'):

#   def _setting(m:Manager)->DRef:
#     nonlocal n1,n2
#     n1 = mkstage(m, {'a':'1'})
#     n2 = mkstage(m, {'maman':n1})
#     return n2

def test_repl_basic():
  with setup_storage2('test_repl_default') as S:

    n1:DRef; n2:DRef
    def _setting(m:Manager)->DRef:
      nonlocal n1,n2
      n1 = mkstage(m, {'a':'1'})
      n2 = mkstage(m, {'maman':n1})
      return n2

    clo=instantiate(_setting,S=S)
    rh=repl_realize(clo, force_interrupt=False)
    assert repl_rref(rh) is not None

    rh=repl_realize(clo, force_interrupt=[n1,n2])
    assert repl_rref(rh) is None
    assert rh.result is not None
    assert n1 in rh.result
    repl_continue(rh=rh)
    assert repl_rref(rh) is None
    assert rh.result is not None
    assert n2 in rh.result
    repl_continue(rh=rh)
    assert repl_rref(rh) is not None


def test_repl_race():
  with setup_storage2('test_repl_recursion'):

    def _setting(m:Manager)->DRef:
      n1 = mkstage(m, {'a':'1'})
      n2 = mkstage(m, {'maman':n1})
      return n2

    clo=instantiate(_setting)
    rh=repl_realize(clo, force_interrupt=True)
    assert repl_rref(rh) is None
    assert rh.result is not None
    assert clo.targets[0] in rh.result

    clo2=instantiate(_setting)
    rref2=realize(clo2) # Realize dref while repl_realizing same dref

    repl_cancel(rh)
    assert_valid_rref(rref2)


def test_repl_override():
  with setup_storage2('test_repl_override') as S:

    n1:DRef; n2:DRef
    def _setting(m:Manager)->DRef:
      nonlocal n1,n2
      n1 = mkstage(m, {'a':'1'}, lambda i: 33)
      n2 = mkstage(m, {'maman':n1}, lambda i: 42)
      return n2

    clo=instantiate(_setting, S=S)
    rh=repl_realize(clo, force_interrupt=[n1])
    assert rh.result is not None
    assert n1 in rh.result
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
    def _setting(m:Manager)->DRef:
      nonlocal n1,n2
      n1 = mkstage(m, {'a':'1'})
      n2 = mkstage(m, {'maman':n1})
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
    def _setting(m:Manager)->DRef:
      nonlocal n1,n2
      n1 = mkstage(m, {'a':'1'})
      n2 = mkstage(m, {'maman':n1})
      return n2

    rh=repl_realize(instantiate(_setting,S=S), force_interrupt=True)
    assert repl_rref(rh) is None
    repl_cancel()
    assert rh.gen is None
    rref=realize(instantiate(_setting, S=S))
    assert isrref(rref)


def test_repl_realizeInval():
  with setup_storage2('test_repl_realizeInval') as S:
    try:
      repl_realize(instantiate(mkstage, {'a':1}, S=S),
                   force_interrupt=33) #type:ignore
      raise ShouldHaveFailed('wrong force_interrupt value')
    except AssertionError:
      pass
