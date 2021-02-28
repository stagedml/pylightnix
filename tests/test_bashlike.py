from pylightnix import ( DRef, RRef, lsref, catref, instantiate, realize,
    unrref, rmref, store_dref2path, store_rref2path, shellref, shell, rref2dref, du,
    repl_realize, repl_cancelBuild, repl_build, build_outpath, find, partial,
    diff, timestring, parsetime )

from tests.setup import ( ShouldHaveFailed, setup_testpath, setup_storage,
    mkstage, mkstage )

from tests.imports import ( isdir, environ, chmod, stat, TemporaryDirectory,
    join, S_IEXEC, sleep )


def test_bashlike():
  with setup_storage('test_bashlike'):
    clo=instantiate(mkstage, {'a':1}, lambda:42)
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
    clo=instantiate(mkstage, {'a':1}, lambda:42)
    drefpath=store_dref2path(clo.dref)
    rref1=realize(clo, force_rebuild=[clo.dref])
    rrefpath=store_rref2path(rref1)
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
      rref=realize(instantiate(mkstage, {'a':1}))
      shellref(rref)
      shellref(rref2dref(rref))
      shellref()
      shell(store_rref2path(rref))
      repl_realize(instantiate(mkstage, {'n':1}), force_interrupt=True)
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
    clo=instantiate(mkstage, {'name':'1'}, lambda:42)
    usage=du()
    assert clo.dref in usage
    assert usage[clo.dref][0]>0
    assert usage[clo.dref][1]=={}
    rref=realize(clo)
    usage=du()
    assert rref in usage[clo.dref][1]
    assert usage[clo.dref][1][rref]>0

def test_find():
  with setup_storage('test_find') as s:
    s1=partial(mkstage, config={'name':'1'}, nondet=lambda:42)
    s2=partial(mkstage, config={'name':'2'}, nondet=lambda:33)
    rref1=realize(instantiate(s1))
    sleep(0.1)
    now=parsetime(timestring())
    rref2=realize(instantiate(s2))
    rrefs=find()
    assert set(rrefs)==set([rref1,rref2])
    rrefs=find(name='1')
    assert rrefs==[rref1]
    rrefs=find(name=s2)
    assert rrefs==[rref2]
    rrefs=find(newer=-10)
    assert len(rrefs)==2
    rrefs=find(newer=now)
    assert rrefs==[rref2]

def test_diff():
  with setup_storage('test_find') as s:
    s1=partial(mkstage, config={'name':'1'}, nondet=lambda:42)
    s2=partial(mkstage, config={'name':'2'}, nondet=lambda:33)
    dref1=instantiate(s1).dref
    rref2=realize(instantiate(s2))
    diff(dref1, rref2)
    diff(dref1, s2)

