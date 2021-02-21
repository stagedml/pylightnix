# Copyright 2021, Sergey Mironov
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

""" Functions for moving parts of the storage to and from archives.  """

from pylightnix.imports import (Popen, dirname, basename, remove, join,
                                relpath, rename, splitext, mkdtemp, basename,
                                isfile, isdir)
from pylightnix.types import (RRef, List, Dict, Path, Iterable, Optional, SPath,
                              Manager, DRef, Config, RConfig, Build)
from pylightnix.core import (store_deepdeps, store_deepdepRrefs,
                             store_rref2path, store_dref2path, storage, tempdir,
                             storagename, alldrefs, rootdrefs, rref2dref,
                             config_deps, store_config, build_wrapper,
                             match_all, mkdrv, realizeMany, instantiate)
from pylightnix.utils import (try_executable, dirrm)



APACK=try_executable('apack',
                     'PYLIGHTNIX_APACK',
                     '`apack` executable not found. Please install `atool` system '
                     'pacakge or set PYLIGHTNIX_APACK env var.',
                     '`arch.pack` procedure will fail.')
AUNPACK=try_executable('aunpack',
                     'PYLIGHTNIX_AUNPACK',
                     '`aunpack` executable not found. Please install `atool` system '
                     'pacakge or set PYLIGHTNIX_AUNPACK env var.',
                     '`arch.unpack` procedure will fail.')


def pack(roots:List[RRef], out:Path, S=None)->None:
  tmp=splitext(out)[0]+'_tmp'+splitext(out)[1]
  try:
    remove(tmp)
  except KeyboardInterrupt:
    raise
  except Exception:
    pass
  rrefs=store_deepdepRrefs(roots,S)
  store_holder=dirname(storage(S))
  retcode=0
  done=False
  try:
    for rref in rrefs | set(roots):
      p=Popen([APACK(), tmp,
               relpath(store_dref2path(rref2dref(rref),S), start=store_holder),
               relpath(store_rref2path(rref,S), start=store_holder)],
              cwd=store_holder)
      p.wait()
      assert p.returncode==0, f"Failed to pack {rref}. Retcode is {p.returncode}"
    done=True
  finally:
    if done:
      rename(tmp,out)
    else:
      try:
        remove(tmp)
      except FileNotFoundError:
        pass

def unpack(archive:Path,S=None)->None:
  tmppath=mkdtemp(suffix=f"_{basename(archive)}", dir=tempdir())
  try:
    p=Popen([AUNPACK(), '-X', tmppath, archive], cwd=tempdir())
    p.wait()
    assert p.returncode==0, \
      f"Failed to unpack '{archive}'. Retcode is {p.returncode}"
    archstore=SPath(join(tmppath, storagename()))
    assert isdir(archstore), \
      f"Archive '{archive}' didn't contain a directory '{storagename()}'"
    # copyclosure(rootdrefs(S=archstore), archstore, S)
  finally:
    # dirrm(tmppath)
    pass

def copyclosure(rrefs:Iterable[RRef], S:SPath, D:Optional[SPath]=None)->None:
  """ Copy the closure of `rrefs` from storage `S` to storage `D` (which
  defaults to the globl-default storage).

  TODO: Implement a non-recursive version.
  """

  def _stage(m:Manager, cfg:RConfig)->DRef:
    for dep_dref in config_deps(cfg):
      dep=_stage(m, store_config(dep_dref,S=S))
      assert dep==dep_dref
    def _make(b:Build)->None:
      assert False, "Not impl"
    # We pass RConfig in place of Config. Not sure it would work.
    return mkdrv(m, cfg, match_all, build_wrapper(_make))

  # for dref in alldrefs(S=S):
  #   print(dref)
  for root_dref in rootdrefs(S=S):
    print("Realizing root:",root_dref)
    realizeMany(instantiate(_stage, store_config(root_dref,S=S), S=D))
  assert False, "Not impl"


