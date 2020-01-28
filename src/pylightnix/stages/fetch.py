from pylightnix.imports import (sha256 as sha256sum, urlparse, Popen, remove,
    basename, join, rename, isfile )
from pylightnix.types import ( DRef, Manager, Config, Build, Context, Name,
    Path, Optional)
from pylightnix.core import ( mkconfig, mkbuild, build_cattrs, build_outpath,
    mkdrv, only, build_wrapper )
from pylightnix.utils import ( get_executable )


WGET=get_executable('wget', 'Please install `wget` pacakge')
AUNPACK=get_executable('aunpack', 'Please install `apack` tool from `atool` package')



def fetchurl(m:Manager, url:str, sha256:str, mode:str='unpack,remove',
             name:Optional[Name]=None, filename:Optional[str]=None)->DRef:
  """ Download and unpack an URL addess.

  Downloading is done by calling `wget` application. Optional unpacking is
  performed with the `aunpack` script from `atool` package. `sha256` defines the
  expected SHA-256 hashsum of the stored data. `mode` allows to tweak the
  stage's behavior: adding word 'unpack' instructs fetchurl to unpack the
  package, adding 'remove' instructs it to remove the archive after unpacking.
  """

  def _instantiate()->Config:
    return mkconfig({'name':name or 'fetchurl',
                     'url':url,
                     'sha256':sha256,
                     'mode':mode})

  def _realize(b:Build)->None:
    c=build_cattrs(b)
    o=build_outpath(b)

    try:
      fname=filename or basename(urlparse(c.url).path)
      assert len(fname)>0,"Downloadable filename shouldn't be empty. Try specifying a valid `filename` argument"
      partpath=join(o,fname+'.tmp')
      p=Popen([WGET, "--continue", '--output-document', partpath, c.url], cwd=o)
      p.wait()

      assert p.returncode == 0, f"Download failed, errcode '{p.returncode}'"
      assert isfile(partpath), f"Can't find output file '{partpath}'"

      with open(partpath,"rb") as f:
        realhash=sha256sum(f.read()).hexdigest();
        assert realhash==c.sha256, f"Expected sha256 checksum '{c.sha256}', but got '{realhash}'"

      fullpath=join(o,fname)
      rename(partpath, fullpath)

      if 'unpack' in c.mode:
        print(f"Unpacking {fullpath}..")
        p=Popen([AUNPACK, fullpath], cwd=o)
        p.wait()
        assert p.returncode == 0, f"Unpack failed, errcode '{p.returncode}'"
        if 'remove' in c.mode:
          print(f"Removing {fullpath}..")
          remove(fullpath)

    except Exception as e:
      print(f"Download failed:",e)
      print(f"Temp folder {o}")
      raise

  return mkdrv(m, _instantiate, only(), build_wrapper(_realize))



