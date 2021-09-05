
from os.path import join
from os import system, chdir, getcwd
from shutil import copytree
from tempfile import TemporaryDirectory
from typing import Any
from subprocess import Popen, PIPE


from os import environ
from pylightnix import Registry, StorageSettings, mkSS, fsinit

S:StorageSettings=mkSS('/tmp/pylightnix_hello_demo')
fsinit(S,remove_existing=True)
R=Registry(S)

hello_version = '2.10'


from pylightnix import (Registry, DRef, RRef, fetchurl2, unpack, mklens, selfref)


tarball:DRef = fetchurl2(
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b',
    out=[selfref, f'hello-{hello_version}.tar.gz'], r=R)


hello_src:DRef = unpack(
    name='unpack-hello',
    refpath=mklens(tarball,r=R).out.refpath,
    aunpack_args=['-q'],
    src=[selfref, f'hello-{hello_version}'],r=R)


from pylightnix import instantiate, realize1
hello_rref:RRef = realize1(instantiate(hello_src, r=R))
print(hello_rref)


from pylightnix import current_storage

with current_storage(S):
  print(mklens(hello_rref).val)
  print(mklens(hello_rref).syspath)
  print(mklens(hello_rref).src.syspath)


from pylightnix import lsref, catref

print(lsref(hello_rref, S))


from pylightnix import Config, mkconfig, mklens, selfref

def hello_config()->Config:
  name = 'hello-bin'
  src = mklens(hello_src,r=R).src.refpath
  out_hello = [selfref, 'usr', 'bin', 'hello']
  out_log = [selfref, 'build.log']
  return mkconfig(locals())


from pylightnix import (Path, Build, build_cattrs, build_outpath, build_path,
                        dirrw )

def hello_realize(b:Build)->None:
  with TemporaryDirectory() as tmp:
    copytree(mklens(b).src.syspath,join(tmp,'src'))
    dirrw(Path(join(tmp,'src')))
    cwd = getcwd()
    try:
      chdir(join(tmp,'src'))
      system(f'( ./configure --prefix=/usr && '
             f'  make &&'
             f'  make install DESTDIR={mklens(b).syspath}'
             f')>{mklens(b).out_log.syspath} 2>&1')
    finally:
      chdir(cwd)


from pylightnix import mkdrv, build_wrapper, match_only

hello:DRef = mkdrv(hello_config(),match_only(),build_wrapper(hello_realize),R)

print(hello)


rref:RRef=realize1(instantiate(hello,r=R))
print(rref)


for line in open(mklens(rref,r=R).out_log.syspath).readlines()[-10:]:
  print(line.strip())


print(Popen([mklens(rref,r=R).out_hello.syspath],
            stdout=PIPE, shell=True).stdout.read()) # type:ignore

