
from os.path import join
from os import system, chdir, getcwd
from shutil import copytree
from tempfile import TemporaryDirectory
from typing import Any
from subprocess import Popen, PIPE

from pylightnix import Path, store_initialize, dirrm
dirrm(Path('/tmp/pylightnix_hello_demo'))
store_initialize(custom_store='/tmp/pylightnix_hello_demo', custom_tmp='/tmp')

from pylightnix import DRef, instantiate_inplace, fetchurl, promise

hello_version = '2.10'

hello_src:DRef = \
  instantiate_inplace(
    fetchurl,
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b',
    src=[promise, f'hello-{hello_version}'])

from pylightnix import RRef, realize_inplace

hello_rref:RRef = realize_inplace(hello_src)
print(hello_rref)

from pylightnix import rref2path

print(rref2path(hello_rref))

from pylightnix import lsref

print(lsref(hello_rref))

from pylightnix import Config, mkconfig, store_cattrs

def hello_config()->Config:
  name = 'hello-bin'
  src = store_cattrs(hello_src).src
  return mkconfig(locals())

from pylightnix import ( Path, Build, build_cattrs, build_outpath, build_path, dirrw )

def hello_realize(b:Build)->None:
  c:Any = build_cattrs(b)
  o:Path = build_outpath(b)
  with TemporaryDirectory() as tmp:
    copytree(build_path(b,c.src),join(tmp,'src'))
    dirrw(Path(join(tmp,'src')))
    cwd = getcwd()
    try:
      chdir(join(tmp,'src'))
      system(f'./configure --prefix=/usr')
      system(f'make')
      system(f'make install DESTDIR={o}')
    finally:
      chdir(cwd)

from pylightnix import mkdrv, build_wrapper, match_only

hello:DRef = \
  instantiate_inplace(mkdrv, hello_config(), match_only(), build_wrapper(hello_realize))

print(hello)

rref:RRef=realize_inplace(hello)
print(rref)


hello_bin=join(rref2path(rref),'usr/bin/hello')
print(Popen([hello_bin], stdout=PIPE, shell=True).stdout.read())
