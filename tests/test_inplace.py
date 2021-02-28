from pylightnix import (
    Manager, DRef, RRef, Path, mklogdir, dirhash, mknode, store_deps,
    store_deepdeps, store_rref2path, Manager, mkcontext, instantiate, realize,
    instantiate_inplace, realize_inplace, assert_valid_rref, store_rrefs_,
    alldrefs, assert_valid_dref )

from tests.imports import (
    given, assume, example, note, settings, text, decimals, integers, rmtree,
    characters, gettempdir, isdir, join, makedirs, from_regex, islink, listdir,
    get_executable, run, dictionaries, one_of, lists, recursive, printable,
    none, booleans, floats, re_compile, composite, event, isfile )

from tests.generators import (
    configs, dicts, artifacts )

from tests.setup import (
    setup_testpath, setup_storage, setup_inplace_reset,
    mktestnode )



def test_inplace():
  with setup_storage('test_inplace'):
    setup_inplace_reset()

    n1 = instantiate_inplace(mktestnode, {'a':'1'})
    n2 = instantiate_inplace(mktestnode, {'b':'2'})
    n3 = instantiate_inplace(mktestnode, {'c':'3', 'maman':n1})
    n4 = instantiate_inplace(mktestnode, {'c':'4', 'papa':n3})
    assert_valid_dref(n3)
    assert_valid_dref(n4)

    rref_n3 = realize_inplace(n3)
    assert_valid_rref(rref_n3)

    all_drefs = list(alldrefs())
    assert len(all_drefs)==4
    assert len(list(store_rrefs_(n1)))==1
    assert len(list(store_rrefs_(n2)))==0
    assert len(list(store_rrefs_(n3)))==1
    assert len(list(store_rrefs_(n4)))==0
