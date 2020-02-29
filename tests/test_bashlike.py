from pylightnix import ( DRef, RRef, lsref, catref, instantiate, realize,
    unrref, rmref, store_dref2path, rref2path, shellref, shell, rref2dref, du,
    repl_realize, repl_cancelBuild, repl_build, build_outpath )

from tests.setup import ( ShouldHaveFailed, setup_testpath, setup_storage,
    mktestnode, mktestnode_nondetermenistic )

from tests.imports import ( isdir, environ, chmod, stat, TemporaryDirectory,
    join, S_IEXEC )


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
    except AssertionError:
      pass
    try:
      catref(clo.dref, ['artifact']) # type:ignore
      raise ShouldHaveFailed('notimpl')
    except AssertionError:
      pass

def test_rmdref():
  with setup_storage('test_rmdref') as s:
    clo=instantiate(mktestnode_nondetermenistic, {'a':1}, lambda:42)
    drefpath=store_dref2path(clo.dref)
    rref1=realize(clo, force_rebuild=[clo.dref])
    rrefpath=rref2path(rref1)
    assert isdir(rrefpath)
    rmref(rref1)
    assert not isdir(rrefpath)
    assert isdir(drefpath)
    rmref(clo.dref)
    assert not isdir(drefpath)
    try:
      rmref('asdasd') # type:ignore
      raise ShouldHaveFailed('shoud reject garbage')
    except AssertionError:
      pass

def test_shellref():
  with setup_storage('test_shellref') as s:
    with TemporaryDirectory() as tmp:
      mockshell=join(tmp,'mockshell')
      with open(mockshell,'w') as f:
        f.write(f"#!/bin/sh\n")
        f.write(f"pwd\n")
      chmod(mockshell, stat(mockshell).st_mode | S_IEXEC)
      environ['SHELL']=mockshell
      rref=realize(instantiate(mktestnode, {'a':1}))
      shellref(rref)
      shellref(rref2dref(rref))
      shellref()
      shell(rref2path(rref))
      repl_realize(instantiate(mktestnode, {'n':1}), force_interrupt=True)
      b=repl_build()
      o=build_outpath(b)
      shell(b)
      repl_cancelBuild(b)
      try:
        shellref('foo') # type:ignore
        raise ShouldHaveFailed('shellref should reject garbage')
      except AssertionError:
        pass


def test_du():
  with setup_storage('test_du') as s:
    usage=du()
    assert usage=={}
    clo=instantiate(mktestnode_nondetermenistic, {'name':'1'}, lambda:42)
    usage=du()
    assert clo.dref in usage
    assert usage[clo.dref][0]>0
    assert usage[clo.dref][1]=={}
    rref=realize(clo)
    usage=du()
    assert rref in usage[clo.dref][1]
    assert usage[clo.dref][1][rref]>0


