from pylightnix import (Manager, DRef, RRef, Path, mklogdir, dirhash, mknode,
                        drefdeps1, rref2path, Manager, mkcontext, instantiate,
                        realize, Name, realized, build_wrapper, Build,
                        mkconfig, match_some, mkdrv, build_outpath, redefine,
                        tryread, mklens, selfref, match_only )

from tests.imports import (
    given, assume, example, note, settings, text, decimals, integers, rmtree,
    characters, gettempdir, isdir, join, makedirs, from_regex, islink, listdir,
    get_executable, run, dictionaries, one_of, lists, recursive, printable,
    none, booleans, floats, re_compile, composite, event, isfile )

from tests.generators import (
    configs, dicts, artifacts )

from tests.setup import ( setup_storage2, ShouldHaveFailed )



@given(d=dicts())
def test_mknode(d)->None:
  with setup_storage2('test_mknode') as S:

    def _setting(m:Manager)->DRef:
      return mknode(m, d)

    cl1 = instantiate(_setting,S=S)
    cl2 = instantiate(_setting,S=S)
    assert len(cl1.derivations)==1
    assert len(cl2.derivations)==1
    assert cl1.derivations[0].dref == cl2.derivations[0].dref
    assert cl1.targets == cl2.targets


@given(d=dicts(), a=artifacts())
def test_mknode_with_artifacts(d,a)->None:
  with setup_storage2('test_mknode_with_artifacts') as S:

    def _setting(m:Manager)->DRef:
      return mknode(m, cfgdict=d, artifacts=a)

    cl = instantiate(_setting,S=S)
    assert len(cl.derivations)==1

    rref = realize(instantiate(_setting,S=S))
    for nm,val in a.items():
      assert isfile(join(rref2path(rref,S=S),nm)), \
          f"RRef {rref} doesn't contain artifact {nm}"



# def test_mkfile()->None:
#   with setup_storage('test_mkfile'):

#     def _setting(m:Manager, nm)->DRef:
#       return mkfile(m, Name('foo'), bytes((nm or 'bar').encode('utf-8')), nm)

#     rref1=realize(instantiate(_setting, None))
#     with open(join(rref2path(rref1),'foo'),'r') as f:
#       bar=f.read()
#     assert bar=='bar'

#     rref2=realize(instantiate(_setting, 'baz'))
#     with open(join(rref2path(rref2),'baz'),'r') as f:
#       baz=f.read()
#     assert baz=='baz'
#     assert rref1!=rref2


def test_realized()->None:
  with setup_storage2('test_realized') as S:

    def _setting(m:Manager, assume_realized:bool)->DRef:
      def _realize(b:Build):
        if assume_realized:
          raise ShouldHaveFailed('Should not call the real realizer')
        return build_outpath(b)
      return mkdrv(m,
                   mkconfig({'name':'1'}), match_only(),
                   build_wrapper(_realize))

    dref=instantiate(realized(_setting), assume_realized=True, S=S)
    try:
      rref=realize(dref)
      raise ShouldHaveFailed('Should not be realized')
    except AssertionError:
      pass

    rref=realize(instantiate(_setting, assume_realized=False,S=S))
    rref2=realize(instantiate(realized(_setting), assume_realized=True,S=S))
    assert rref==rref2

def test_redefine()->None:
  with setup_storage2('test_redefine') as S:

    def _setting(m:Manager)->DRef:
      return mknode(m, {'name':'foo','bar':'baz','output':[selfref,'f']},
                       {Name('f'):bytes(('umgh').encode('utf-8'))})
    def _nc(c):
      mklens(c,S=S).bar.val=42
    _setting2=redefine(_setting, new_config=_nc)

    rref=realize(instantiate(_setting2,S=S))
    assert mklens(rref,S=S).bar.val==42
    assert tryread(mklens(rref,S=S).output.syspath)=='umgh'




