from pylightnix import (StorageSettings, Matcher, Build, Context, Path, RefPath,
                        Config, Manager, RRef, DRef, Path, build_path,
                        build_outpath, build_cattrs, mkdrv, rref2path, mkconfig,
                        tryread, fetchurl, instantiate, realize, match_only,
                        build_wrapper, selfref, mklens, instantiate_inplace,
                        realize_inplace, rmref, fsinit, pack, unpack, allrrefs,
                        gc, redefine, match_some, match_latest, dirrm,
                        mksettings, readstr, writestr)

from typing import List, Optional

from re import search
import re

Chunk=List[str]

def scanmd(fpath:str)->List[Chunk]:
  acc=[]; acc2=[]; inchunk=False
  for line in open(fpath).readlines():
    if inchunk:
      if search('^\s*```', line):
        inchunk=False
        acc2.append(acc)
        acc=[]
      else:
        acc.append(line)
    else:
      if search('^\s*```',line):
        inchunk=True
      else:
        pass
  return acc2


