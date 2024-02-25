from typing import List, Dict, Optional, Any

from pylightnix import (RRef, DRef, Registry, Build, autodrv, autostage, mklens,
                        realize1, instantiate, isrref, writejson, selfref,
                        isrref, isfile, readjson, realizeMany,match_latest,
                        current_registry, writestr, mkregistry, current_storage,
                        isrefpath, isdref)

from tests.setup import (setup_storage2, callername)

def test_autodrv_semnatics():
  with setup_storage2(callername()) as S:
    def _stage1(r:Registry,
                name='stage1',
                i:int=3,
                b=True,
                l:List[int]=[1,2,3],
                d:Dict[str,int]={"a":1,"b":2},
                f:float=3.14,
                out=[selfref,"file.json"])->DRef:
      @autodrv(nouts=3,**locals())
      def drv(name,i,b,l,d,f,out,build:Build,rindex):
        writejson(out,rindex)
      return drv
    def _stage2(r:Registry,ref:DRef,
                name='stage2', p=33, out=[selfref,'out.json'])->DRef:
      @autodrv(always_multiref=True,**locals())
      def drv(name,p,out,ref,build,rindex):
        writejson(out,rindex)
      return drv
    def _stage3(r:Registry,ref:DRef,name='stage3',
                out=[selfref,"out.json"])->DRef:
      @autodrv(nouts=2,**locals())
      def drv(name,ref,out,build,rindex):
        assert isrref(ref._rref)
        for n1 in range(3):
          assert isrref(ref.ref[n1]._rref)
          assert ref.ref[n1].i==3
          assert ref.ref[n1].b
          assert ref.ref[n1].l==[1,2,3]
          assert ref.ref[n1].d=={"a":1,"b":2}
        writejson(out,rindex)
      return drv
    r=Registry(S=S)
    r1=_stage1(r)
    r2=_stage2(r,r1)
    r3=_stage3(r,r2)
    rrefs=realizeMany(instantiate(r3,r=r,S=S))
    assert len(rrefs)==2
    acc=set()
    for i,rref in enumerate(rrefs):
      assert isrref(rref)
      acc.add(readjson(mklens(rref,S=S).out.syspath))
    assert acc==set(range(2))

def test_autostage_minimal():
  with setup_storage2(callername()) as S, current_storage(S):
    @autostage
    def stage1(build):
      pass
    rref=realize1(instantiate(stage1))
    assert isrref(rref)

def test_autostage_name():
  with setup_storage2(callername()) as S, current_storage(S):
    @autostage(name='foo')
    def stage1(build,name):
      pass
    rref=realize1(instantiate(stage1))
    assert mklens(rref).name.val == 'foo'

def test_autostage_semantics():
  with setup_storage2(callername()) as S:
    @autostage(a=2,b="aa",out_file=[selfref,"result.json"])
    def stage1(a,b,out_file,build:Build):
      writejson(out_file,{'field':'Haha'})
    @autostage(d=4,e={'a':1,'b':True})
    def stage2(d,e,ref1,refs,build:Build):
      assert mklens(build).ref1.out_file.field.val=='Haha'
      assert d==4 and e['a']==1 and e['b']is True
      assert isrref(ref1._rref)
      assert isfile(ref1.out_file)
      assert all([isrref(r._rref) for r in refs])
    r=Registry(S)
    r1=stage1(r)
    r2=stage2(r=r,ref1=r1,refs=[r1,r1])
    rref2=realize1(instantiate(r2,r=r,S=S))
    assert isrref(rref2)


def test_autostage_overload():
  @autostage(a=42)
  def stage(a,build):
    pass
  with setup_storage2(callername()) as S:
    r1=realize1(instantiate(stage,S=S))
    assert mklens(r1,S=S).a.val==42
    r1=realize1(instantiate(stage,a=33,S=S))
    assert mklens(r1,S=S).a.val==33

def test_autostage_directref1():
  with setup_storage2(callername()) as S:
    with current_registry(mkregistry(S)) as r:
      @autostage(a=42)
      def stage1(a,build):
        assert a==111
      @autostage(b=33,ref_stage1=stage1(a=111))
      def stage2(b,build,ref_stage1):
        assert b==33
        assert ref_stage1.a==111
      r1=realize1(instantiate(stage2))
      assert mklens(r1,S=S).b.val==33

def test_autostage_directref2():
  with setup_storage2(callername()) as S:
    r=mkregistry(S)
    @autostage(a=42,out=[selfref,"out.txt"],r=r,nouts=3)
    def stage1(a,out,rindex,build):
      assert a==111
      writestr(out,str(rindex))
    @autostage(b=33,ref_stage1=stage1(a=111),r=r)
    def stage2(b,build,ref_stage1):
      assert b==33
      assert all(r.a==111 for r in ref_stage1)
    r1=realize1(instantiate(stage2,r=r))
    assert mklens(r1,S=S).b.val==33

def test_autostage_argument():
  with setup_storage2(callername()) as S, current_storage(S):
    @autostage
    def stage1(a=42):
      assert a==42
    dref:DRef
    dref,clo=instantiate(stage1)
    assert isdref(dref)
    assert mklens(dref).a.val==42
    rref=realize1((dref,clo))
    assert isrref(rref)
    assert mklens(rref).a.val==42

def test_autostage_parse_signature_nouts():
  with setup_storage2(callername()) as S, current_storage(S):
    @autostage(nouts=2)
    def stage1(rindex,a=42,b=3,out=[selfref,"out.txt"]):
      assert b==3
      assert a==111
      assert isinstance(out,str) and out.endswith('out.txt')
      writestr(out,str(rindex))
    rrefs=realizeMany(instantiate(stage1,a=111))
    assert len(rrefs)==2
    assert all(isrref(r) for r in rrefs)

def test_autostage_parse_signature_drefs():
  with setup_storage2(callername()) as S, current_storage(S):
    @autostage
    def stage1(a=42):
      pass
    @autostage
    def stage2(b=33, s1=lambda r:stage1(a=141,r=r)):
      pass
    rref=realize1(instantiate(stage2,b=111))
    assert isrref(rref)
    assert mklens(rref).b.val==111
    assert mklens(rref).s1.a.val==141

