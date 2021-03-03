from pylightnix import ( DRef, RRef, lsref, catref, instantiate, realize,
    unrref, fetchurl, fetchlocal, isrref, store_rref2path, isfile, mklens )

from tests.imports import ( TemporaryDirectory, join, stat, chmod, S_IEXEC,
    system, Popen, PIPE, get_executable )
from tests.setup import (ShouldHaveFailed, setup_storage, pipe_stdout)


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

      wanted_sha256=pipe_stdout([SHA256SUM, f"{mockdata}.tar.gz"]).split()[0]

      import pylightnix.stages.fetch
      oldwget=pylightnix.stages.fetch.WGET
      try:
        pylightnix.stages.fetch.WGET=lambda: mockwget

        clo=instantiate(fetchurl,
              url='mockwget://result.tar.gz',
              filename='validname.tar.gz',
              sha256=wanted_sha256)
        rref=realize(clo)
      finally:
        pylightnix.stages.fetch.WGET=oldwget


def test_fetchlocal():
  with setup_storage('test_fetclocal') as tmp:
    mockdata=join(tmp,'mockdata')
    with open(mockdata,'w') as f:
      f.write('dogfood')
    system(f"tar -C '{tmp}' -zcvf {tmp}/mockdata.tar.gz mockdata")

    wanted_sha256=pipe_stdout([SHA256SUM, "mockdata.tar.gz"], cwd=tmp).split()[0]

    rref=realize(instantiate(fetchlocal,
          path=mockdata+'.tar.gz',
          filename='validname.tar.gz',
          sha256=wanted_sha256))
    assert isrref(rref)
    assert isfile(join(store_rref2path(rref),'mockdata'))


def test_fetchlocal2():
  with setup_storage('test_fetclocal') as tmp:
    mockdata=join(tmp,'mockdata')
    with open(mockdata,'w') as f:
      f.write('dogfood')

    wanted_sha256=pipe_stdout([SHA256SUM, "mockdata"], cwd=tmp).split()[0]

    rref=realize(instantiate(fetchlocal, path=mockdata, sha256=wanted_sha256,
                             mode='as-is'))
    assert isrref(rref)
    assert isfile(join(store_rref2path(rref),'mockdata'))
    assert isfile(mklens(rref).out_path.syspath)

