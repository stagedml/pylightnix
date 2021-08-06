from pylightnix import (DRef, RRef, lsref, catref, instantiate, realize, unrref,
                        rmref, dref2path, rref2path, shellref, shell, rref2dref,
                        du, repl_realize, repl_cancelBuild, repl_build,
                        build_outpath, find, partial, diff, timestring,
                        parsetime, linkdref, linkrref, linkrrefs, readlink,
                        undref, islink, rrefbstart)

from tests.setup import (ShouldHaveFailed, mkstage, mkstage,
                         setup_storage2 )

from tests.imports import (isdir, environ, chmod, stat, TemporaryDirectory,
                           join, S_IEXEC, sleep)


def test_bashlike():
  with setup_storage2('test_bashlike') as S:
    clo=instantiate(mkstage, {'a':1}, lambda i:42, S=S)
    rref1=realize(clo, force_rebuild=[clo.dref])
    rref2=realize(clo, force_rebuild=[clo.dref])
    assert 'artifact' in lsref(rref1,S=S)
    assert 'context.json' in lsref(rref1,S=S)
    assert '__buildstart__.txt' in lsref(rref1,S=S)
    assert '__buildstop__.txt' in lsref(rref1,S=S)
    h1,_,_=unrref(rref1)
    h2,_,_=unrref(rref2)
    assert len(lsref(clo.dref,S=S))==2
    assert h1 in lsref(clo.dref,S=S)
    assert h2 in lsref(clo.dref,S=S)
    assert '42' in catref(rref1,['artifact'],S=S)
    try:
      lsref('foobar',S=S) # type:ignore
      raise ShouldHaveFailed('should reject garbage')
    except AssertionError:
      pass
    try:
      catref(clo.dref,['artifact'],S=S) # type:ignore
      raise ShouldHaveFailed('notimpl')
    except AssertionError:
      pass

def test_rmdref():
  with setup_storage2('test_rmdref') as S:
    clo=instantiate(mkstage, {'a':1}, lambda i:42, S=S)
    drefpath=dref2path(clo.dref,S=S)
    rref1=realize(clo, force_rebuild=[clo.dref])
    rrefpath=rref2path(rref1, S=S)
    assert isdir(rrefpath)
    rmref(rref1,S=S)
    assert not isdir(rrefpath)
    assert isdir(drefpath)
    rmref(clo.dref,S=S)
    assert not isdir(drefpath)
    try:
      rmref('asdasd',S=S) # type:ignore
      raise ShouldHaveFailed('shoud reject garbage')
    except AssertionError:
      pass

def test_shellref():
  with setup_storage2('test_shellref') as S:
    with TemporaryDirectory() as tmp:
      mockshell=join(tmp,'mockshell')
      with open(mockshell,'w') as f:
        f.write(f"#!/bin/sh\n")
        f.write(f"pwd\n")
      chmod(mockshell, stat(mockshell).st_mode | S_IEXEC)
      environ['SHELL']=mockshell
      rref=realize(instantiate(mkstage, {'a':1}, S=S))
      shellref(rref,S=S)
      shellref(rref2dref(rref),S=S)
      shellref(S=S)
      shell(rref2path(rref,S=S),S=S)
      repl_realize(instantiate(mkstage, {'n':1},S=S), force_interrupt=True)
      b=repl_build()
      o=build_outpath(b)
      shell(b)
      repl_cancelBuild(b)
      try:
        shellref('foo',S=S) # type:ignore
        raise ShouldHaveFailed('shellref should reject garbage')
      except AssertionError:
        pass


def test_du():
  with setup_storage2('test_du') as S:
    usage=du(S=S)
    assert usage=={}
    clo=instantiate(mkstage, {'name':'1'}, lambda i:42, S=S)
    usage=du(S=S)
    assert clo.dref in usage
    assert usage[clo.dref][0]>0
    assert usage[clo.dref][1]=={}
    rref=realize(clo)
    usage=du(S=S)
    assert rref in usage[clo.dref][1]
    assert usage[clo.dref][1][rref]>0

def test_find():
  with setup_storage2('test_find') as S:
    s1=partial(mkstage, config={'name':'1'}, nondet=lambda i:42)
    s2=partial(mkstage, config={'name':'2'}, nondet=lambda i:33)
    rref1=realize(instantiate(s1,S=S))
    sleep(0.1)
    now=parsetime(timestring())
    rref2=realize(instantiate(s2,S=S))
    rrefs=find(S=S)
    assert set(rrefs)==set([rref1,rref2])
    rrefs=find(name='1',S=S)
    assert rrefs==[rref1]
    rrefs=find(name=s2,S=S)
    assert rrefs==[rref2]
    rrefs=find(newer=-10,S=S)
    assert len(rrefs)==2
    # FIXME: repair now-based search
    # rrefs=find(newer=now)
    # assert rrefs==[rref2]

def test_diff():
  with setup_storage2('test_find') as S:
    s1=partial(mkstage, config={'name':'1'}, nondet=lambda i:42)
    s2=partial(mkstage, config={'name':'2'}, nondet=lambda i:33)
    dref1=instantiate(s1,S=S).dref
    rref2=realize(instantiate(s2,S=S))
    diff(dref1,rref2,S=S)
    diff(dref1,s2,S=S)

def test_linkrrefs()->None:
  with setup_storage2('test_linkrrefs') as S:
    s1=partial(mkstage, config={'name':'NaMe'})
    rref1=realize(instantiate(s1,S=S))
    l=linkrrefs([rref1], destdir=S.tmpdir, format='result-%(N)s', S=S)
    assert len(l)==1
    assert str(l[0])==join(S.tmpdir,'result-NaMe')
    assert islink(join(S.tmpdir,'result-NaMe'))
    assert S.tmpdir in l[0]
    assert unrref(rref1)[0] in readlink(l[0])
    assert unrref(rref1)[1] in readlink(l[0])
    assert undref(rref2dref(rref1))[0] in readlink(l[0])
    l=linkrrefs([rref1], destdir=S.tmpdir, format='result-%(T)s', S=S)
    t=rrefbstart(rref1,S)
    assert t is not None
    assert t in l[0]
    assert S.tmpdir in l[0]

