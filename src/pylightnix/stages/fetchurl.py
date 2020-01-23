from pylightnix.imports import (sha256, urlparse, Popen, remove, basename, join, rename, isfile )
from pylightnix.types import ( DRef, Manager, Config, Build, Context, Name, Path )
from pylightnix.core import ( mkconfig, mkbuild, build_cattrs, build_outpath,
    mkdrv, only, build_wrapper )
from pylightnix.utils import ( get_executable )


WGET=get_executable('wget', 'Please install `wget` pacakge')
AUNPACK=get_executable('aunpack', 'Please install `apack` tool from `atool` package')


def config(url:str, sha256:str, mode:str='unpack,remove', name:Name=None)->Config:
  return mkconfig(locals())

# def downloaded(s:State)->State:
#   return state_add(s, 'download')

def download(b:Build)->None:
  c=build_cattrs(b)
  o=build_outpath(b)

  try:
    fname=basename(urlparse(c.url).path)
    partpath=join(o,fname+'.tmp')
    p=Popen([WGET, "--continue", '--output-document', partpath, c.url], cwd=o)
    p.wait()

    assert p.returncode == 0, f"Download failed, errcode '{p.returncode}'"
    assert isfile(partpath), f"Can't find output file '{partpath}'"

    with open(partpath,"rb") as f:
      realhash=sha256(f.read()).hexdigest();
      assert realhash==c.sha256, f"Expected sha256 checksum '{c.sha256}', but got '{realhash}' instead"

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

    # protocol_add(m, 'download')
  except Exception as e:
    print(f"Download failed:",e)
    print(f"Temp folder {o}")
    raise


def fetchurl(m:Manager, *args, **kwargs)->DRef:
  def _instantiate()->Config:
    return config(*args, **kwargs)
  return mkdrv(m, _instantiate, only, build_wrapper(download))



