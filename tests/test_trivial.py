from pylightnix import (Registry, DRef, RRef, Path, mklogdir, dirhash, mknode,
                        drefdeps1, rref2path, Registry, mkcontext, instantiate,
                        realize1, Name, realized, build_wrapper, Build,
                        mkconfig, match_some, mkdrv, build_outpath, redefine,
                        tryread, mklens, selfref, match_only )

from tests.imports import (
    given, assume, example, note, settings, text, decimals, integers, rmtree,
    characters, gettempdir, isdir, join, makedirs, from_regex, islink, listdir,
    get_executable, run, dictionaries, one_of, lists, recursive, printable,
    none, booleans, floats, re_compile, composite, event, isfile, Verbosity )

from tests.generators import (
    configs, dicts, artifacts )

from tests.setup import ( setup_storage2, ShouldHaveFailed )



@given(d=dicts())
def test_mknode(d)->None:
  with setup_storage2('test_mknode') as S:

    def _setting(r:Registry)->DRef:
      return mknode(r, d)

    _,cl1=instantiate(_setting,S=S)
    _,cl2=instantiate(_setting,S=S)
    assert len(cl1.derivations)==1
    assert len(cl2.derivations)==1
    assert cl1.derivations[0].dref == cl2.derivations[0].dref
    assert cl1.targets == cl2.targets


@given(d=dicts(), a=artifacts())
def test_mknode_with_artifacts(d,a)->None:
  with setup_storage2('test_mknode_with_artifacts') as S:

    def _setting(r:Registry)->DRef:
      return mknode(r, cfgdict=d, artifacts=a)

    _,cl=instantiate(_setting,S=S)
    assert len(cl.derivations)==1

    rref = realize1(instantiate(_setting,S=S))
    for nm,val in a.items():
      assert isfile(join(rref2path(rref,S=S),nm)), \
          f"RRef {rref} doesn't contain artifact {nm}"


def test_realized()->None:
  with setup_storage2('test_realized') as S:

    def _setting(r:Registry, assume_realized:bool)->DRef:
      def _realize(b:Build):
        if assume_realized:
          raise ShouldHaveFailed('Should not call the real realizer')
        return build_outpath(b)
      return mkdrv(mkconfig({'name':'1'}), match_only(),
                   build_wrapper(_realize), r)

    dref:DRef
    dref,clo=instantiate(realized(_setting), assume_realized=True, S=S)
    try:
      rref=realize1(clo)
      raise ShouldHaveFailed('Should not be realized')
    except AssertionError:
      pass

    rref=realize1(instantiate(_setting, assume_realized=False,S=S))
    rref2=realize1(instantiate(realized(_setting), assume_realized=True,S=S))
    assert rref==rref2

def test_redefine()->None:
  with setup_storage2('test_redefine') as S:

    def _setting(r:Registry)->DRef:
      return mknode(r, {'name':'foo','bar':'baz','output':[selfref,'f']},
                       {Name('f'):bytes(('umgh').encode('utf-8'))})
    def _nc(c):
      mklens(c,S=S).bar.val=42
    _setting2=redefine(_setting, new_config=_nc)

    rref=realize1(instantiate(_setting2,S=S))
    assert mklens(rref,S=S).bar.val==42
    assert tryread(mklens(rref,S=S).output.syspath)=='umgh'




