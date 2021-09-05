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
                                copyfile, environ, getLogger, isabs, isdir,
                                splitext, re_sub )
from pylightnix.types import ( DRef, Registry, Build, Context, Name,
    Path, Optional, List, Config, RefPath )
from pylightnix.core import ( mkconfig, mkdrv, match_only,
                             PYLIGHTNIX_NAMEPAT, cfgcattrs, selfref,
                             fstmpdir, tlregistry )
from pylightnix.build import ( build_outpath,
    build_paths, build_deref_, build_config, build_wrapper, build_wrapper )
from pylightnix.utils import ( try_executable, makedirs, filehash )
from pylightnix.lens import ( mklens )

logger=getLogger(__name__)
info=logger.info
error=logger.error

CURL=try_executable('curl',
                    'PYLIGHTNIX_CURL',
                    '`curl` executable not found. Please install `curl` system '
                    'pacakge or set PYLIGHTNIX_CURL env var.',
                    '`fetchurl2` stage will fail.')

AUNPACK=try_executable('aunpack',
                       'PYLIGHTNIX_AUNPACK',
                       '`aunpack` executable not found. Please install `atool` '
                       'system package or set PYLIGHTNIX_AUNPACK env var.',
                       '`unpack` stage will fail')

def fetchurl2(url:str,
              sha256:Optional[str]=None,
              sha1:Optional[str]=None,
              name:Optional[str]=None,
              filename:Optional[str]=None,
              force_download:bool=False,
              r:Optional[Registry]=None,
              **kwargs)->DRef:
  """ Download file given it's URL addess.

  Downloading is done by calling `curl` application. The path to the executable
  may be altered by setting the `PYLIGHTNIX_CURL` environment variable.

  Agruments:
  - `r:Registry` the dependency resolution [Registry](#pylightnix.types.Registry).
  - `url:str` URL to download from. Should point to a single file.
  - `sha256:str` SHA-256 hash sum of the file.
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
    return fetchurl2(
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
  tmpfetchdir=join(fstmpdir(r.S),'fetchurl2')
  assert isabs(tmpfetchdir), (f"Expected an absolute PYLIGHTNIX_TMP path, "
                              f"got {tmpfetchdir}")

  filename_=filename or basename(urlparse(url).path)
  assert len(filename_)>0, ("Downloadable filename shouldn't be empty. "
                            "Try specifying a valid `filename` argument")
  assert CURL() is not None
  makedirs(tmpfetchdir, exist_ok=True)

  if name is None:
    name='fetchurl2'

  if sha256 is None and sha1 is None:
    if isfile(url):
      sha256=filehash(Path(url))
      url=f'file://{url}'
    else:
      assert False, ("Either `sha256` or `sha1` arguments should be specified "
                     "for URLs")

  def _config()->dict:
    args:dict={'name':name}
    if sha1 is not None:
      args.update({'sha1':sha1})
    if sha256 is not None:
      args.update({'sha256':sha256})
    args.update({'out':[selfref, filename_]})
    args.update(**kwargs)
    return args

  def _make(b:Build)->None:
    c=cfgcattrs(build_config(b))
    o=build_outpath(b)

    download_dir=o if force_download else tmpfetchdir
    partpath=join(download_dir,filename_+'.tmp')

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
      fullpath=join(o,filename_)
      rename(partpath, fullpath)

    except Exception as e:
      error(f"Download failed: {e}")
      error(f"Keeping temporary directory {o}")
      raise

  return mkdrv(mkconfig(_config()),
               match_only(),
               build_wrapper(_make),
               r)


def unpack(path:Optional[str]=None,
           refpath:Optional[RefPath]=None,
           name:Optional[str]=None,
           sha256:Optional[str]=None,
           sha1:Optional[str]=None,
           aunpack_args:List[str]=[],
           r:Optional[Registry]=None,
           **kwargs)->DRef:

  if path:
    assert refpath is None
  if refpath:
    assert path is None
  assert path or refpath

  def _config()->dict:
    args={'name':name if name else 'unpack',
          'path':path,
          'refpath':refpath,
          'aunpack_args':aunpack_args}
    if sha1 is not None:
      args.update({'sha1':sha1})
    if sha256 is not None:
      args.update({'sha256':sha256})
    args.update(**kwargs)
    return args

  def _make(b:Build):
    if mklens(b).get('refpath').optval is not None:
      fullpath=mklens(b).get('refpath').syspath
    if mklens(b).get('path').optval is not None:
      fullpath=mklens(b).get('path').syspath
    assert fullpath is not None
    info(f"Unpacking {fullpath}..")
    p=Popen([AUNPACK(), fullpath]+aunpack_args, cwd=mklens(b).syspath)
    p.wait()
    assert p.returncode == 0, f"Unpack failed, errcode '{p.returncode}'"
  return mkdrv(mkconfig(_config()), match_only(), build_wrapper(_make), r)

