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

from pylightnix.imports import (sha256 as sha256sum, urlparse, Popen, remove,
    basename, join, rename, isfile, copyfile )
from pylightnix.types import ( DRef, Manager, Build, Context, Name,
    Path, Optional, List, Config )
from pylightnix.core import ( mkconfig, mkbuild, build_cattrs, build_outpath,
    mkdrv, match_only, build_wrapper, promise )
from pylightnix.utils import ( try_executable, makedirs )


WGET=try_executable('wget', 'Please install `wget` pacakge.')
AUNPACK=try_executable('aunpack', 'Please install `apack` tool from `atool` package.')


def _unpack(o:str, fullpath:str, remove_file:bool):
  print(f"Unpacking {fullpath}..")
  p=Popen([AUNPACK(), fullpath], cwd=o)
  p.wait()
  assert p.returncode == 0, f"Unpack failed, errcode '{p.returncode}'"
  if remove_file:
    print(f"Removing {fullpath}..")
    remove(fullpath)


def fetchurl(m:Manager,
             url:str,
             sha256:str,
             mode:str='unpack,remove',
             name:Optional[str]=None,
             filename:Optional[str]=None,
             force_download:bool=False,
             check_promises:bool=True,
             **kwargs)->DRef:
  """ Download and unpack an URL addess.

  Downloading is done by calling `wget` application. Optional unpacking is
  performed with the `aunpack` script from `atool` package. `sha256` defines the
  expected SHA-256 hashsum of the stored data. `mode` allows to tweak the
  stage's behavior: adding word 'unpack' instructs fetchurl to unpack the
  package, adding 'remove' instructs it to remove the archive after unpacking.

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
    return fetchurl(
      m,
      name='hello-src',
      url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
      sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b')

  rref:RRef=realize(instantiate(hello_src))
  print(rref2path(rref))
  ```
  """

  import pylightnix.core
  tmpfetchdir=join(pylightnix.core.PYLIGHTNIX_TMP,'fetchurl')

  def _instantiate()->Config:
    assert WGET() is not None
    assert AUNPACK() is not None
    makedirs(tmpfetchdir, exist_ok=True)
    kwargs.update({'name':name or 'fetchurl',
                   'url':url,
                   'sha256':sha256,
                   'mode':mode})
    return mkconfig(kwargs)

  def _realize(b:Build)->None:
    c=build_cattrs(b)
    o=build_outpath(b)

    download_dir=o if force_download else tmpfetchdir

    try:
      fname=filename or basename(urlparse(c.url).path)
      assert len(fname)>0, ("Downloadable filename shouldn't be empty. "
                            "Try specifying a valid `filename` argument")
      partpath=join(download_dir,fname+'.tmp')
      p=Popen([WGET(), "--continue", '--output-document', partpath, c.url],
              cwd=download_dir)
      p.wait()

      assert p.returncode == 0, f"Download failed, errcode '{p.returncode}'"
      assert isfile(partpath), f"Can't find output file '{partpath}'"

      with open(partpath,"rb") as f:
        realhash=sha256sum(f.read()).hexdigest();
        assert realhash==c.sha256, (f"Expected sha256 checksum '{c.sha256}', "
                                    f"but got '{realhash}'")

      fullpath=join(o,fname)
      rename(partpath, fullpath)

      if 'unpack' in c.mode:
        _unpack(o, fullpath, 'remove' in c.mode)

    except Exception as e:
      print(f"Download failed:",e)
      print(f"Temp folder {o}")
      raise

  return mkdrv(m, _instantiate(), match_only(), build_wrapper(_realize),
                  check_promises=check_promises)



def fetchlocal(m:Manager,
             path:str,
             sha256:str,
             mode:str='unpack,remove',
             name:Optional[str]=None,
             filename:Optional[str]=None,
             **kwargs)->DRef:
  """ Copy local file into Pylightnix storage. This function is typically
  intended to register application-specific files which are distributed with a
  source repository.


  FIXME: Switch regular `fetchurl` to `curl` and call it with `file://` URLs.

  """

  def _instantiate()->Config:
    assert AUNPACK() is not None
    kwargs.update({'name':name or 'fetchlocal',
                   'path':path,
                   'sha256':sha256,
                   'mode':mode})
    return mkconfig(kwargs)

  def _realize(b:Build)->None:
    c=build_cattrs(b)
    o=build_outpath(b)

    try:
      fname=filename or basename(path)
      assert len(fname)>0, ("Destination filename shouldn't be empty. "
                            "Try specifying a valid `filename` argument")
      partpath=join(o,fname+'.tmp')
      copyfile(c.path, partpath)
      assert isfile(partpath), f"Can't find output file '{partpath}'"

      with open(partpath,"rb") as f:
        realhash=sha256sum(f.read()).hexdigest();
        assert realhash==c.sha256, (f"Expected sha256 checksum '{c.sha256}', "
                                    f"but got '{realhash}'")

      fullpath=join(o,fname)
      rename(partpath, fullpath)

      if 'unpack' in c.mode:
        _unpack(o, fullpath, 'remove' in c.mode)

    except Exception as e:
      print(f"Copying failed:",e)
      print(f"Temp folder {o}")
      raise

  return mkdrv(m, _instantiate(), match_only(), build_wrapper(_realize))

