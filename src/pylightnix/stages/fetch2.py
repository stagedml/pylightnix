# Copyright 2020, Sergey Mironov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Builtin stages for fetching things from the Internet """

from pylightnix.imports import (sha256 as sha256sum, sha1 as sha1sum, urlparse,
                                Popen, remove, basename, join, rename, isfile,
                                copyfile, environ, getLogger, isabs )
from pylightnix.types import ( DRef, Manager, Build, Context, Name,
    Path, Optional, List, Config )
from pylightnix.core import ( mkconfig, mkdrv, match_only, promise )
from pylightnix.build import ( mkbuild, build_outpath, build_setoutpaths,
    build_paths, build_deref_, build_cattrs, build_wrapper, build_wrapper )
from pylightnix.utils import ( try_executable, makedirs, filehash )
from pylightnix.lens import ( mklens )

logger=getLogger(__name__)
info=logger.info
error=logger.error

CURL=try_executable('curl', 'Please install `curl` pacakge.')


def fetchurl2(m:Manager,
              url:str,
              sha256:Optional[str]=None,
              sha1:Optional[str]=None,
              name:Optional[str]=None,
              filename:Optional[str]=None,
              force_download:bool=False,
              **kwargs)->DRef:
  """ Download file given it's URL addess.

  Downloading is done by calling `wget` application. Optional unpacking is
  performed with the `aunpack` script from `atool` package. `sha256` defines the
  expected SHA-256 hashsum of the stored data. `mode` allows to tweak the
  stage's behavior: adding word 'unpack' instructs fetchurl to unpack the
  package, adding 'remove' instructs it to remove the archive after unpacking.

  If 'unpack' is not expected, then the promise named 'out_path' is created.

  Agruments:
  - `m:Manager` the dependency resolution [Manager](#pylightnix.types.Manager).
  - `url:str` URL to download from. Should point to a single file.
  - `sha256:str` SHA-256 hash sum of the file.
  - `model:str='unpack,remove'` Additional options. Format: `[unpack[,remove]]`.
  - `name:Optional[str]`: Name of the Derivation. The stage will attempt to
    deduce the name if not specified.
  - `filename:Optional[str]=None` Name of the filename on disk after downloading.
    Stage will attempt to deduced it if not specified.
  - `force_download:bool=False` If False, resume the last download if
    possible.
  - `check_promises:bool=True` Passed to `mkdrv` as-is.

  Example:
  ```python
  def hello_src(m:Manager)->DRef:
    hello_version = '2.10'
    return fetchurl2(
      m,
      name='hello-src',
      url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
      sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b')

  rref:RRef=realize(instantiate(hello_src))
  print(rref2path(rref))
  ```
  """

  import pylightnix.core
  tmpfetchdir=join(pylightnix.core.PYLIGHTNIX_TMP,'fetchurl2')
  assert isabs(tmpfetchdir), (f"Expect absolute PYLIGHTNIX_TMP path, "
                              f"got {tmpfetchdir}")

  fname=filename or basename(urlparse(url).path)
  assert len(fname)>0, ("Downloadable filename shouldn't be empty. "
                        "Try specifying a valid `filename` argument")
  assert CURL() is not None
  makedirs(tmpfetchdir, exist_ok=True)

  if sha256 is None and sha1 is None:
    if url.startswith('file://'):
      sha256=filehash(url)
    else:
      assert False, ("Either sha256 or sha1 arguments should be set for non "
                     "`file://' URLs")

  def _config()->dict:
    args={'name':name}
    if sha1 is not None:
      args.update({'sha1':sha1})
    if sha256 is not None:
      args.update({'sha256':sha256})
    args.update(**kwargs)
    return args

  def _make(b:Build)->None:
    c=build_cattrs(b)
    o=build_outpath(b)

    download_dir=o if force_download else tmpfetchdir
    partpath=join(download_dir,fname+'.tmp')

    try:
      p=Popen([CURL(), "--continue-at", "-", "--output", partpath, url],
              cwd=download_dir)
      p.wait()
      assert p.returncode == 0, f"Download failed, errcode '{p.returncode}'"
      assert isfile(partpath), f"Can't find output file '{partpath}'"

      with open(partpath,"rb") as f:
        if sha256 is not None:
          realhash=sha256sum(f.read()).hexdigest()
          assert realhash==c.sha256, (f"Expected sha256 checksum '{c.sha256}', "
                                      f"but got '{realhash}'")
        if sha1 is not None:
          realhash=sha1sum(f.read()).hexdigest()
          assert realhash==c.sha1, (f"Expected sha1 checksum '{c.sha1}', "
                                    f"but got '{realhash}'")
      fullpath=join(o,fname)
      rename(partpath, fullpath)

    except Exception as e:
      error(f"Download failed: {e}")
      error(f"Keeping temporary directory {o}")
      raise

  return mkdrv(m,
               mkconfig(_config()),
               match_only(),
               build_wrapper(_make))




