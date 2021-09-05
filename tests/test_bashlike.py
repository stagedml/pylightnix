from pylightnix import (DRef, RRef, lsref, catref, instantiate, realize1,
                        unrref, rmref, dref2path, rref2path, shellref, shell,
                        rref2dref, du, repl_realize, repl_cancelBuild,
                        repl_build, build_outpath, find, diff, timestring,
                        parsetime, linkdref, linkrref, linkrrefs, readlink,
                        undref, islink, rrefbstart, fstmpdir, Stage, Optional,
                        Registry)

from tests.setup import (ShouldHaveFailed, mkstage, mkstage,
                         setup_storage2 )

from tests.imports import (isdir, environ, chmod, stat, TemporaryDirectory,
                           join, S_IEXEC, sleep)


def wrapstage(config,**kwargs):
  def _stage(r:Optional[Registry])->DRef:
    return mkstage(config,r=r,**kwargs)
  return _stage

def test_bashlike():
  with setup_storage2('test_bashlike') as S:
    _,clo=instantiate(wrapstage({'a':1},nondet=lambda i:42), S=S)
    rref1=realize1(clo, force_rebuild=clo.targets)
    rref2=realize1(clo, force_rebuild=clo.targets)
    assert 'artifact' in lsref(rref1,S=S)
    assert 'context.json' in lsref(rref1,S=S)
    assert '__buildstart__.txt' in lsref(rref1,S=S)
    assert '__buildstop__.txt' in lsref(rref1,S=S)
    h1,_,_=unrref(rref1)
    h2,_,_=unrref(rref2)
    assert len(lsref(clo.targets[0],S=S))==2
    assert h1 in lsref(clo.targets[0],S=S)
    assert h2 in lsref(clo.targets[0],S=S)
    assert '42' in catref(rref1,['artifact'],S=S)
    try:
      lsref('foobar',S=S) # type:ignore
      raise ShouldHaveFailed('should reject garbage')
    except AssertionError:
      pass
    try:
      catref(clo.targets[0],['artifact'],S=S) # type:ignore
      raise ShouldHaveFailed('notimpl')
    except AssertionError:
      pass

def test_rmdref():
  with setup_storage2('test_rmdref') as S:
    stage=wrapstage(config={'a':1}, nondet=lambda i:42)
    _,clo=instantiate(stage, S=S)
    drefpath=dref2path(clo.targets[0],S=S)
    rref1=realize1(clo, force_rebuild=[clo.targets[0]])
    rrefpath=rref2path(rref1, S=S)
    assert isdir(rrefpath)
    rmref(rref1,S=S)
    assert not isdir(rrefpath)
    assert isdir(drefpath)
    rmref(clo.targets[0],S=S)
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
      rref=realize1(instantiate(mkstage,{'a':1}, S=S))
      shellref(rref,S=S)
      shellref(rref2dref(rref),S=S)
      shellref(S=S)
      shell(rref2path(rref,S=S),S=S)
      repl_realize(instantiate(mkstage,{'n':1},S=S), force_interrupt=True)
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
    s=wrapstage({'name':'1'}, nondet=lambda i:42)
    _,clo=instantiate(s, S=S)
    usage=du(S=S)
    assert clo.targets[0] in usage
    assert usage[clo.targets[0]][0]>0
    assert usage[clo.targets[0]][1]=={}
    rref=realize1(clo)
    usage=du(S=S)
    assert rref in usage[clo.targets[0]][1]
    assert usage[clo.targets[0]][1][rref]>0

def test_find():
  with setup_storage2('test_find') as S:
    s1=wrapstage(config={'name':'1'}, nondet=lambda i:42)
    s2=wrapstage(config={'name':'2'}, nondet=lambda i:33)
    rref1=realize1(instantiate(s1,S=S))
    sleep(0.1)
    now=parsetime(timestring())
    rref2=realize1(instantiate(s2,S=S))
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
    s1=wrapstage(config={'name':'1'},nondet=lambda i:42)
    s2=wrapstage(config={'name':'2'},nondet=lambda i:33)
    dref1:DRef=instantiate(s1,S=S)[0]
    rref2:RRef=realize1(instantiate(s2,S=S))
    diff(dref1,rref2,S=S)
    diff(dref1,s2,S=S)

def test_linkrrefs()->None:
  with setup_storage2('test_linkrrefs') as S:
    s1=wrapstage(config={'name':'NaMe'})
    rref1=realize1(instantiate(s1,S=S))
    l=linkrrefs([rref1], destdir=fstmpdir(S), format='result-%(N)s', S=S)
    assert len(l)==1
    assert str(l[0])==join(fstmpdir(S),'result-NaMe')
    assert islink(join(fstmpdir(S),'result-NaMe'))
    assert fstmpdir(S) in l[0]
    assert unrref(rref1)[0] in readlink(l[0])
    assert unrref(rref1)[1] in readlink(l[0])
    assert undref(rref2dref(rref1))[0] in readlink(l[0])
    l=linkrrefs([rref1], destdir=fstmpdir(S), format='result-%(T)s', S=S)
    t=rrefbstart(rref1,S)
    assert t is not None
    assert t in l[0]
    assert fstmpdir(S) in l[0]

