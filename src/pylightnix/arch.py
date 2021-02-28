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
                                isfile, isdir, copytree)
from pylightnix.types import (RRef, List, Dict, Path, Iterable, Optional, SPath,
                              Manager, DRef, Config, RConfig, Build)
from pylightnix.core import (store_deepdeps, store_deepdepRrefs,
                             store_rref2path, store_dref2path, storage, tempdir,
                             storagename, alldrefs, rootdrefs, rootrrefs,
                             rref2dref, config_deps, store_config_, match_all,
                             mkdrv, realize, realizeMany, instantiate,
                             rrefs2groups, store_deref, rrefdata, config_name)
from pylightnix.build import (build_setoutgroups, build_wrapper)
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
    copyclosure(rootrrefs(S=archstore), archstore, S)
  finally:
    # dirrm(tmppath)
    pass

def copyclosure(rrefs_S:Iterable[RRef], S:SPath, D:Optional[SPath]=None)->None:
  """ Copy the closure of `rrefs` from source storage `S` to the destination
  storage `D`. By default, use global storage as a desitnation.

  TODO: Implement a non-recursive version.
  TODO: Replace copytree with a smth like movetree
  """
  for rref_S in rrefs_S:

    dref_S:DRef=rref2dref(rref_S)

    def _stage(m:Manager, cfg:RConfig)->DRef:
      print(f"Instantiating {config_name(cfg)}")
      for dep_dref in config_deps(cfg):
        dep=_stage(m, store_config_(dep_dref,S=S))
        assert dep==dep_dref, f"{dep} != {dep_dref}"

      def _make(b:Build)->None:
        """ 'Realize' the derivation in `D` by copying its contents from `S` """
        rrefs=store_deref(context_holder=rref_S, dref=b.dref, S=S)
        grps_S=rrefs2groups(rrefs, S=S)
        grps=build_setoutgroups(b, [list(grp.keys()) for grp in grps_S])
        for g_S,g in zip(grps_S,grps):
          for tag,rref in g_S:
            assert tag in g
            for artifact in rrefdata(rref,S):
              copytree(artifact, join(g[tag],basename(artifact)))
      # We pass RConfig in place of Config. Not sure if its going to work or not.
      return mkdrv(m, cfg, match_all(), build_wrapper(_make))

    rref_D=realize(instantiate(_stage, store_config_(dref_S,S=S), S=D))
    assert rref_D==rref_S, f"{rref_D}!={rref_S}"


  # assert False, "Not impl"


