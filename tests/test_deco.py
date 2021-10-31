from pylightnix import (RRef, DRef, Registry, Build, Placeholder, autodrv,
                        autostage, mklens, realize1, instantiate, isrref)

from tests.setup import (setup_storage2)

def stage3(r:Registry,a=3,b=True)->DRef:
  @autodrv(locals())
  def drv(a,b,build:Build):
    print(f"a={a} b={b}.")
  return drv


def stage4(ref:DRef,r:Registry,c=3,d=True)->DRef:
  @autodrv(locals())
  def drv(c,d,ref:RRef,build:Build):
    print(f"c={c} d={d} ref:{ref}")
    print(f"a={mklens(ref).a.val} b={mklens(ref).b.val}")
  return drv


def stage_all2(r:Registry):
  r1=stage3(r)
  r2=stage4(r1,r=r)
  return r2

def test_autodrv():
  with setup_storage2('test_autodrv') as S:
    r1=realize1(instantiate(stage_all2,S=S))
    assert isrref(r1)


@autostage(a=2,b=4)
def stage1(a,b,build:Build):
  print('Building stage1')
  print(f'a {a} b {b}. 2.ddxx')

@autostage(d=4,e=1,ref1=Placeholder())
def stage2(d,e,ref1:RRef,build:Build):
  print('Building stage2')
  print(f'd {d} e {e}')
  print(f'ref1 {ref1}')


def stage_all(r:Registry):
  r1=stage1(r)
  r2=stage2(r=r,ref1=r1)
  return r2

def test_autostage():
  with setup_storage2('test_autostage') as S:
    r1=realize1(instantiate(stage_all,S=S))
    assert isrref(r1)
