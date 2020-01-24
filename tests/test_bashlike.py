from pylightnix import ( DRef, RRef, lsref, catref, instantiate, realize,
    unrref )

from tests.setup import (
    ShouldHaveFailed, setup_testpath, setup_storage, mktestnode_nondetermenistic )


def test_bashlike():
  with setup_storage('test_bashlike'):
    clo=instantiate(mktestnode_nondetermenistic, {'a':1}, lambda:42)
    rref1=realize(clo, force_rebuild=[clo.dref])
    rref2=realize(clo, force_rebuild=[clo.dref])
    assert 'artifact' in lsref(rref1)
    assert 'context.json' in lsref(rref1)
    assert '__buildtime__.txt' in lsref(rref1)
    h1,_,_=unrref(rref1)
    h2,_,_=unrref(rref2)
    assert len(lsref(clo.dref))==2
    assert h1 in lsref(clo.dref)
    assert h2 in lsref(clo.dref)
    assert '42' in catref(rref1,['artifact'])
    try:
      lsref('foobar') # type:ignore
      raise ShouldHaveFailed('should reject garbage')
    except:
      pass
    try:
      catref(clo.dref, ['artifact'])
      raise ShouldHaveFailed('notimpl')
    except:
      pass

