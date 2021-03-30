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
                                relpath, rename, splitext, mkdtemp, isfile,
                                isdir, shutil_copy)
from pylightnix.types import (RRef, List, Dict, Path, Iterable, Optional,
                              SPath, Manager, DRef, Config, RConfig, Build,
                              RRefGroup, Set)
from pylightnix.core import (drefdeps, rrefdeps,
                             store_rref2path, store_dref2path, storage,
                             tempdir, storagename, alldrefs, rootdrefs,
                             rootrrefs, rref2dref, config_deps, drefcfg_,
                             mkdrv, realize, realizeMany,
                             instantiate, rrefs2groups, store_deref, rrefdata,
                             config_name, tag_out, store_deref_, realizeGroups,
                             match_exact, exact, groups2rrefs,
                             config_substitutePromises)
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
  rrefs=rrefdeps(roots,S)
  store_holder=dirname(storage(S))
  done=False
  try:
    for rref in rrefs | set(roots):
      p=Popen([APACK(), '-q', tmp,
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
  tmppath=Path(mkdtemp(suffix=f"_{basename(archive)}", dir=tempdir()))
  try:
    p=Popen([AUNPACK(), '-q', '-X', tmppath, archive], cwd=tempdir())
    p.wait()
    assert p.returncode==0, \
      f"Failed to unpack '{archive}'. Retcode is {p.returncode}"
    archstore=SPath(join(tmppath, storagename()))
    assert isdir(archstore), \
      f"Archive '{archive}' didn't contain a directory '{storagename()}'"
    copyclosure(rrefs2groups(rootrrefs(S=archstore),S=archstore),S=archstore,D=S)
  finally:
    dirrm(tmppath)
    pass

def deref_(ctxgr, dref, S):
  """ FIXME Figure out what happens here. """
  return store_deref_(context_holder=ctxgr[tag_out()], dref=dref, S=S) \
          if dref!=rref2dref(ctxgr[tag_out()]) else [ctxgr]

def copyclosure(rrefgs_S:Iterable[RRefGroup], S:SPath, D:Optional[SPath]=None)->None:
  """ Copy the closure of `rrefs` from source storage `S` to the destination
  storage `D`. By default, use global storage as a desitnation.

  TODO: Implement a non-recursive version.
  """
  for rrefg_S in rrefgs_S:
    visited_drefs:Set[DRef]=set()

    dref_S:DRef=rref2dref(rrefg_S[tag_out()])

    def _stage(m:Manager, dref:DRef)->DRef:
      nonlocal visited_drefs
      cfg=drefcfg_(dref,S=S)
      # print(f"Instantiating {cfg}")
      if dref not in visited_drefs:
        for dep_dref in config_deps(config_substitutePromises(cfg,dref)):
          if dep_dref!=dref:
            _stage(m, dep_dref)

      def _make(b:Build)->None:
        """ 'Realize' the derivation in `D` by copying its contents from `S` """
        grps_S=deref_(rrefg_S, b.dref, S=S)
        # print(f'Building {b.dref} with {b.context}')
        # print(grps_S)
        grps=build_setoutgroups(b, [list(grp.keys()) for grp in grps_S])
        for g_S,g in zip(grps_S,grps):
          for tag,rref in g_S.items():
            # print(f'Copying {tag} : {rref}')
            assert tag in g
            for artifact in rrefdata(rref,S):
              shutil_copy(artifact, g[tag])

      rrefgs_S1=deref_(rrefg_S, dref, S=S)
      # print(f"Expecting to get: {rrefgs_S1}")
      dref2=mkdrv(m, cfg, match_exact(rrefgs_S1), build_wrapper(_make))
      visited_drefs.add(dref2)
      assert dref==dref2, f"{dref} != {dref2}"
      return dref2

    rrefgs_D=realizeGroups(instantiate(_stage, dref_S, S=D))
    assert len(rrefgs_D)==1, f"{rrefgs_D}"
    assert rrefgs_D[0]==rrefg_S, f"{rrefgs_D[0]}!={rrefg_S}"


  # assert False, "Not impl"


