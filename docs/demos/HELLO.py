
from os.path import join
from os import system, chdir, getcwd
from shutil import copytree
from tempfile import TemporaryDirectory
from typing import Any
from subprocess import Popen, PIPE

from shutil import rmtree
from pylightnix import store_initialize
rmtree('/tmp/pylightnix_hello_demo', ignore_errors=True)
store_initialize(custom_store='/tmp/pylightnix_hello_demo', custom_tmp='/tmp')

from pylightnix import DRef, instantiate_inplace, fetchurl

hello_version = '2.10'

hello_src:DRef = \
  instantiate_inplace(
    fetchurl,
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b')

from pylightnix import RRef, realize_inplace

hello_rref:RRef = realize_inplace(hello_src)
print(hello_rref)

from pylightnix import Config, mkconfig

def hello_config()->Config:
  name = 'hello-bin'
  src = [hello_src, f'hello-{hello_version}']
  return mkconfig(locals())

from pylightnix import Path, Build, build_cattrs, build_outpath, build_path

def hello_realize(b:Build)->None:
  c:Any = build_cattrs(b)
  o:Path = build_outpath(b)
  with TemporaryDirectory() as tmp:
    copytree(build_path(b,c.src),join(tmp,'src'))
    cwd = getcwd()
    try:
      chdir(join(tmp,'src'))
      system(f'./configure --prefix=/usr')
      system(f'make')
      system(f'make install DESTDIR={o}')
    finally:
      chdir(cwd)

from pylightnix import mkdrv, build_wrapper, only

hello:DRef = \
  instantiate_inplace(mkdrv, hello_config, only(), build_wrapper(hello_realize))

print(hello)

rref:RRef=realize_inplace(hello)
print(rref)

from pylightnix import rref2path

hello_bin=join(rref2path(rref),'usr/bin/hello')
print(Popen([hello_bin], stdout=PIPE, shell=True).stdout.read())
