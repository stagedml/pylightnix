from pylightnix import ( Manager, DRef, RRef, Path, mklogdir, dirhash,
                        drefdeps1, rref2path, Manager, mkcontext,
                        instantiate, realize, instantiate_inplace,
                        realize_inplace, assert_valid_rref, drefrrefs, alldrefs,
                        assert_valid_dref )

from tests.imports import (
    given, assume, example, note, settings, text, decimals, integers, rmtree,
    characters, gettempdir, isdir, join, makedirs, from_regex, islink, listdir,
    get_executable, run, dictionaries, one_of, lists, recursive, printable,
    none, booleans, floats, re_compile, composite, event, isfile )

from tests.generators import (configs, dicts, artifacts)

from tests.setup import (setup_storage2, setup_inplace_reset,
                         mkstage)



def test_inplace():
  with setup_storage2('test_inplace') as S:
    setup_inplace_reset(S)

    n1 = instantiate_inplace(mkstage, {'a':'1'})
    n2 = instantiate_inplace(mkstage, {'b':'2'})
    n3 = instantiate_inplace(mkstage, {'c':'3', 'maman':n1})
    n4 = instantiate_inplace(mkstage, {'c':'4', 'papa':n3})
    assert_valid_dref(n3)
    assert_valid_dref(n4)

    rref_n3 = realize_inplace(n3)
    assert_valid_rref(rref_n3)

    all_drefs = list(alldrefs())
    assert len(all_drefs)==4
    assert len(list(drefrrefs(n1)))==1
    assert len(list(drefrrefs(n2)))==0
    assert len(list(drefrrefs(n3)))==1
    assert len(list(drefrrefs(n4)))==0

