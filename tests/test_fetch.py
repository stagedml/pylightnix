from pylightnix import ( DRef, RRef, lsref, catref, instantiate, realize,
    unrref, fetchurl )

from tests.imports import ( TemporaryDirectory, join, stat, chmod, S_IEXEC,
    system, Popen, PIPE, get_executable )
from tests.setup import (
    ShouldHaveFailed, setup_testpath, setup_storage,
    mktestnode_nondetermenistic )


SHA256SUM=get_executable('sha256sum', 'Please install `sha256sum` tool from `coreutils` package')

def test_fetchurl():
  with setup_storage('test_fetchurl'):
    with TemporaryDirectory() as tmp:
      mockwget=join(tmp,'mockwget')
      mockdata=join(tmp,'mockdata')
      with open(mockdata,'w') as f:
        f.write('blala')
      system(f'tar -zcvf {mockdata}.tar.gz {mockdata}')
      with open(mockwget,'w') as f:
        f.write(f"#!/bin/sh\n")
        f.write(f"mv {mockdata}.tar.gz $3\n")
      chmod(mockwget, stat(mockwget).st_mode | S_IEXEC)

      wanted_sha256=Popen([SHA256SUM, f"{mockdata}.tar.gz"], stdout=PIPE).stdout.read().split()[0]

      import pylightnix.stages.fetch
      oldwget=pylightnix.stages.fetch.WGET
      try:
        pylightnix.stages.fetch.WGET=mockwget

        clo=instantiate(fetchurl,
              url='mockwget://result.tar.gz',
              filename='validname.tar.gz',
              sha256=wanted_sha256.decode())
        rref=realize(clo)
      finally:
        pylightnix.stages.fetch.WGET=oldwget


