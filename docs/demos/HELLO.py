
from os.path import join
from os import system, chdir, getcwd
from shutil import copytree
from tempfile import TemporaryDirectory
from typing import Any
from subprocess import Popen, PIPE


from os import environ
from pylightnix import fsinit

environ['PYLIGHTNIX_ROOT']='/tmp/pylightnix_hello_demo'
fsinit(remove_existing=True)


from pylightnix import (fetchurl2, unpack, DRef, RRef, instantiate_inplace,
                        realize_inplace, mklens, selfref)


hello_version = '2.10'

tarball:DRef = \
  instantiate_inplace(
    fetchurl2,
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b',
    out=[selfref, f'hello-{hello_version}.tar.gz'])


hello_src:DRef = \
  instantiate_inplace(
    unpack,
    name='unpack-hello',
    refpath=mklens(tarball).out.refpath,
    aunpack_args=['-q'],
    src=[selfref, f'hello-{hello_version}'])


hello_rref:RRef = realize_inplace(hello_src)
print(hello_rref)


from pylightnix import rref2path

print(rref2path(hello_rref))
print(mklens(hello_rref).val)
print(mklens(hello_rref).syspath)
print(mklens(hello_rref).src.syspath)


from pylightnix import lsref, catref

print(lsref(hello_rref))


from pylightnix import Config, mkconfig, mklens, selfref

def hello_config()->Config:
  name = 'hello-bin'
  src = mklens(hello_src).src.refpath
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

hello:DRef = \
  instantiate_inplace(mkdrv, hello_config(), match_only(), build_wrapper(hello_realize))

print(hello)


rref:RRef=realize_inplace(hello)
print(rref)


for line in open(mklens(rref).out_log.syspath).readlines()[-10:]:
  print(line.strip())


print(Popen([mklens(rref).out_hello.syspath],
            stdout=PIPE, shell=True).stdout.read()) # type:ignore

