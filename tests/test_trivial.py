from pylightnix import (
    Manager, DRef, RRef, Path, mklogdir, dirhash, mknode, store_deps,
    store_deepdeps, store_rref2path, Manager, mkclosure, instantiate, realize )

from tests.imports import (
    given, assume, example, note, settings, text, decimals, integers, rmtree,
    characters, gettempdir, isdir, join, makedirs, from_regex, islink, listdir,
    get_executable, run, dictionaries, one_of, lists, recursive, printable,
    none, booleans, floats, re_compile, composite, event, isfile )

from tests.generators import (
    configs, dicts, artifacts )

from tests.setup import (
    setup_testpath, setup_storage )



@given(d=dicts())
def test_mknode(d)->None:
  setup_storage('test_mknode')

  def _setting(m:Manager)->DRef:
    return mknode(m, d)

  ds1 = instantiate(_setting)
  ds2 = instantiate(_setting)
  assert len(ds1)==1
  assert len(ds2)==1
  assert ds1[0].dref == ds2[0].dref


@given(d=dicts(), a=artifacts())
def test_mknode_with_artifacts(d,a)->None:
  setup_storage('test_mknode_with_artifacts')

  def _setting(m:Manager)->DRef:
    return mknode(m, sources=d, artifacts=a)

  derivs = instantiate(_setting)
  assert len(derivs)==1

  rref = realize(_setting)
  for nm,val in a.items():
    assert isfile(join(store_rref2path(rref),nm)), \
        f"RRef {rref} doesn't contain artifact {nm}"



