from pylightnix import ( DRef, RRef, lsref, catref, instantiate, realize,
                        unrref, fetchurl, fetchurl2, isrref, rref2path, isfile,
                        mklens, promise, basename )

from tests.imports import ( TemporaryDirectory, join, stat, chmod, S_IEXEC,
    system, Popen, PIPE, get_executable )
from tests.setup import (
    ShouldHaveFailed, setup_testpath, setup_storage,
    mktestnode_nondetermenistic, pipe_stdout )


SHA256SUM=get_executable('sha256sum', 'Please install `sha256sum` tool from `coreutils` package')

def test_fetchurl2():
  with setup_storage('test_fetchurl'):
    with TemporaryDirectory() as tmp:
      mockcurl=join(tmp,'mockcurl')
      print(mockcurl)
      mockdata=join(tmp,'mockdata')
      with open(mockdata,'w') as f:
        f.write('blala')
      system(f'tar -zcvf {mockdata}.tar.gz {mockdata}')
      with open(mockcurl,'w') as f:
        f.write("#!/bin/sh\n")
        f.write(f"mv --verbose {mockdata}.tar.gz $4\n")
      chmod(mockcurl, stat(mockcurl).st_mode | S_IEXEC)

      wanted_sha256=pipe_stdout([SHA256SUM, f"{mockdata}.tar.gz"]).split()[0]

      import pylightnix.stages.fetch2
      oldcurl=pylightnix.stages.fetch2.CURL
      try:
        pylightnix.stages.fetch2.CURL=lambda: mockcurl

        rref=realize(instantiate(fetchurl2,
              url='mockcurl://result.tar.gz',
              filename='validname.tar.gz',
              sha256=wanted_sha256,
              out=[promise,'validname.tar.gz']))

      finally:
        pylightnix.stages.fetch2.CURL=oldcurl

      assert isrref(rref)
      assert isfile(mklens(rref).out.syspath)


def test_fetchurl2_file():
  with setup_storage('test_fetclocal') as tmp:
    mockdata=join(tmp,'mockdata.foo')
    with open(mockdata,'w') as f:
      f.write('dogfood')

    wanted_sha256=pipe_stdout([SHA256SUM, "mockdata.foo"], cwd=tmp).split()[0]
    rref=realize(instantiate(fetchurl2,
                             url=f"file://{mockdata}",
                             sha256=wanted_sha256))
    assert isrref(rref)
    assert isfile(mklens(rref).out.syspath)
    assert basename(mklens(rref).out.syspath)=="mockdata.foo"

