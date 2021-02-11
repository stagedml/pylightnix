from pylightnix.imports import (Popen, dirname, basename, remove, join,
                                relpath, rename, splitext)
from pylightnix.types import (RRef, List, Path)
from pylightnix.core import (store_deepdeps, store_deepdepRrefs, rref2path)
from pylightnix.utils import (try_executable)



APACK=try_executable('apack',
                     'PYLIGHTNIX_APACK',
                     '`apack` executable not found. Please install `atool` system '
                     'pacakge or set PYLIGHTNIX_APACK env var.',
                     '`arch.pack` procedure will fail.')


def pack(roots:List[RRef], out:Path)->None:
  tmp=splitext(out)[0]+'_tmp'+splitext(out)[1]
  rrefs=store_deepdepRrefs(roots)
  try:
    remove(tmp)
  except KeyboardInterrupt:
    raise
  except Exception:
    pass
  import pylightnix.core
  store_holder=dirname(pylightnix.core.PYLIGHTNIX_STORE)
  for rref in rrefs | set(roots):
    p=Popen([APACK(), tmp, relpath(rref2path(rref), start=store_holder)],
          cwd=store_holder)
    p.wait()
  rename(tmp,out)

