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
    Popen, remove, basename, join, rename, isfile, copyfile, environ, getLogger )
from pylightnix.types import ( DRef, Registry, Build, Context, Name,
    Path, Optional, List, Config )
from pylightnix.core import ( mkconfig, mkdrv, match_only, cfgcattrs,
                             selfref, fstmpdir, tlregistry )
from pylightnix.build import ( build_outpath, build_paths, build_deref_,
                              build_wrapper, build_wrapper,
                              build_config )
from pylightnix.utils import ( try_executable, makedirs )
from pylightnix.lens import ( mklens )

logger=getLogger(__name__)
info=logger.info
error=logger.error

WGET=try_executable('wget',
                    'PYLIGHTNIX_WGET',
                    'Executable `wget` not found. Please install `wget` system '
                    'pacakge or set PYLIGHTNIX_WGET env var.',
                    '`fetchurl` stage will fail.')
AUNPACK=try_executable('aunpack',
                       'PYLIGHTNIX_AUNPACK',
                       '`aunpack` executable not found. Please install `atool` '
                       'system package or set PYLIGHTNIX_AUNPACK env var.',
                       '`fetchurl` and `fetchlocal` stages will fail in its '
                       '`unpack` mode')

def _unpack_inplace(o:str, fullpath:str, remove_file:bool):
  info(f"Unpacking {fullpath}..")
  p=Popen([AUNPACK(), fullpath], cwd=o)
  p.wait()
  assert p.returncode == 0, f"Unpack failed, errcode '{p.returncode}'"
  if remove_file:
    info(f"Removing {fullpath}..")
    remove(fullpath)


def fetchurl(url:str,
             sha256:Optional[str]=None,
             sha1:Optional[str]=None,
             mode:str='unpack,remove',
             name:Optional[str]=None,
             filename:Optional[str]=None,
             force_download:bool=False,
             check_promises:bool=True,
             r:Optional[Registry]=None,
             **kwargs)->DRef:
  """ Download and unpack an URL addess.

  Downloading is done by calling `wget` application. Optional unpacking is
  performed with the `aunpack` script from `atool` package. `sha256` defines the
  expected SHA-256 hashsum of the stored data. `mode` allows to tweak the
  stage's behavior: adding word 'unpack' instructs fetchurl to unpack the
  package, adding 'remove' instructs it to remove the archive after unpacking.

  If 'unpack' is not expected, then the promise named 'out_path' is created.

  Agruments:
  - `r:Registry` the dependency resolution [Registry](#pylightnix.types.Registry).
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
  def hello_src(r:Registry)->DRef:
    hello_version = '2.10'
    return fetchurl(
      r,
      name='hello-src',
      url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
      sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b')

  rref:RRef=realize1(instantiate(hello_src))
  print(rref2path(rref))
  ```
  """

  r=tlregistry(r)
  assert r is not None, f"The registry is required"
  tmpfetchdir=join(fstmpdir(r.S),'fetchurl')

  fname=filename or basename(urlparse(url).path)
  assert len(fname)>0, ("Downloadable filename shouldn't be empty. "
                        "Try specifying a valid `filename` argument")

  def _instantiate()->Config:
    assert WGET() is not None
    if 'unpack' in mode:
      assert AUNPACK() is not None
    assert (sha256 is None) or (sha1 is None)
    makedirs(tmpfetchdir, exist_ok=True)
    if sha256 is not None:
      kwargs.update({'name':name or 'fetchurl',
                     'url':url,
                     'sha256':sha256,
                     'mode':mode})
    elif sha1 is not None:
      kwargs.update({'name':name or 'fetchurl',
                     'url':url,
                     'sha1':sha1,
                     'mode':mode})
    else:
      assert False, 'Either sha256 or sha1 arguments should be set'
    if 'unpack' not in mode:
      kwargs.update({'out_path': [selfref, fname]})
    return mkconfig(kwargs)

  def _realize(b:Build)->None:
    c=cfgcattrs(build_config(b))
    o=build_outpath(b)

    download_dir=o if force_download else tmpfetchdir

    try:
      partpath=join(download_dir,fname+'.tmp')
      p=Popen([WGET(), "--continue", '--output-document', partpath, c.url],
              cwd=download_dir)
      p.wait()

      assert p.returncode == 0, f"Download failed, errcode '{p.returncode}'"
      assert isfile(partpath), f"Can't find output file '{partpath}'"

      with open(partpath,"rb") as f:
        if sha256 is not None:
          realhash=sha256sum(f.read()).hexdigest()
          assert realhash==c.sha256, (f"Expected sha256 checksum '{c.sha256}', "
                                      f"but got '{realhash}'")
        elif sha1 is not None:
          realhash=sha1sum(f.read()).hexdigest()
          assert realhash==c.sha1, (f"Expected sha1 checksum '{c.sha1}', "
                                      f"but got '{realhash}'")
        else:
          assert False, 'Either sha256 or sha1 arguments should be set'

      fullpath=join(o,fname)
      rename(partpath, fullpath)

      if 'unpack' in c.mode:
        _unpack_inplace(o, fullpath, 'remove' in c.mode)

    except Exception as e:
      error(f"Download failed: {e}")
      error(f"Keeping temporary directory {o}")
      raise

  return mkdrv(_instantiate(), match_only(), build_wrapper(_realize), r)



def fetchlocal(sha256:str,
               path:Optional[str]=None,
               envname:Optional[str]=None,
               mode:str='unpack,remove',
               name:Optional[str]=None,
               filename:Optional[str]=None,
               check_promises:bool=True,
               r:Optional[Registry]=None,
               **kwargs)->DRef:
  """ Copy local file into Pylightnix storage. This function is typically
  intended to register application-specific files which are distributed with a
  source repository.

  See `fetchurl` for arguments description.

  If 'unpack' is not expected, then the promise named 'out_path' is created.

  FIXME: Switch regular `fetchurl` to `curl` and call it with `file://` URLs.
  """

  path_:Optional[str]=None
  if path is not None:
    path_=path
  if envname is not None:
    assert envname in environ, (
      f"Environment variable {envname} should be set")
    path_=environ[envname]
  assert path_ is not None, \
    f"Either 'path' or 'envname' should be specified"
  fname=filename or str(basename(path_))
  assert len(fname)>0, ("Destination filename shouldn't be empty. "
                        "Try specifying a valid `filename` argument")

  def _instantiate()->Config:
    if 'unpack' in mode:
      assert AUNPACK() is not None
    assert path is not None or envname is not None, (
      "Either `path` or `envname` argument must be specified")
    assert path is None or envname is None, (
      "`path` and `envname` arguments can't be both set")
    kwargs.update({'name':name or 'fetchlocal'})
    if path is not None:
      kwargs.update({'path':path})
    if envname is not None:
      kwargs.update({'envname':envname})
    kwargs.update({'sha256':sha256, 'mode':mode})
    if 'unpack' not in mode:
      kwargs.update({'out_path': [selfref, fname]})
    return mkconfig(kwargs)

  def _realize(b:Build)->None:
    c=cfgcattrs(build_config(b))
    o=build_outpath(b)

    try:
      assert path_ is not None
      partpath=join(o,fname)+'.tmp'
      fullpath=join(o,fname)

      copyfile(path_, partpath)
      assert isfile(partpath), f"Can't copy '{path_}' to '{partpath}'"

      with open(partpath,"rb") as f:
        realhash=sha256sum(f.read()).hexdigest()
        assert realhash==c.sha256, (f"Expected sha256 checksum '{c.sha256}', "
                                    f"but got '{realhash}'")
      rename(partpath,fullpath)

      if 'unpack' in c.mode:
        _unpack_inplace(o, fullpath, 'remove' in c.mode)

    except Exception as e:
      error(f"Copying failed: {e}")
      error(f"Keeping temporary directory {o}")
      raise

  return mkdrv(_instantiate(), match_only(), build_wrapper(_realize), r)

