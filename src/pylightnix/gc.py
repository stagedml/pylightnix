from pylightnix.imports import (sha256, deepcopy, isdir, islink, makedirs,
                                join, json_dump, json_load, json_dumps,
                                json_loads, isfile, relpath, listdir, rmtree,
                                mkdtemp, replace, environ, split, re_match,
                                ENOTEMPTY, get_ident, contextmanager,
                                OrderedDict, lstat, maxsize, readlink, chain,
                                getLogger, walk, abspath)

from pylightnix.utils import (dirhash, assert_serializable, assert_valid_dict,
                              dicthash, scanref_dict, scanref_list, forcelink,
                              timestring, parsetime, datahash, readjson,
                              tryread, encode, dirchmod, dirrm, filero, isrref,
                              isdref, traverse_dict, ispromise, isclaim,
                              tryread_def, tryreadjson_def, isrefpath,
                              dirsize)

from pylightnix.types import (Dict, List, Any, Tuple, Union, Optional, Iterable,
                              IO, Path, Hash, DRef, RRef, RefPath, PromisePath,
                              HashPart, Callable, Context, Name, NamedTuple,
                              Build, RConfig, ConfigAttrs, Derivation, Stage,
                              Manager, Matcher, Realizer, Set, Closure,
                              Generator, Key, BuildArgs, PYLIGHTNIX_PROMISE_TAG,
                              PYLIGHTNIX_CLAIM_TAG, Config, RealizeArg,
                              InstantiateArg, Tag, Group, RRefGroup)

from pylightnix.core import (instantiate, realize, path2rref, path2dref,
                             store_gc, rref2path)

from pylightnix.bashlike import (rmref)


def diskspace_h(sz:int)->str:
  return f"{sz//2**10:4} K" if sz<2**20 else \
         f"{sz//2**20:4} M" if sz<2**30 else \
         f"{sz//2**30:4} G"


def gc_exceptions(keep_paths:List[Path])->Tuple[List[DRef],List[RRef]]:
  """ Scans `keep_paths` list for references to Pylightnix storage. Ignores
  unrelated filesystem objects. """
  keep_drefs:List[DRef]=[]
  keep_rrefs:List[RRef]=[]

  def _check(f:str):
    nonlocal keep_drefs, keep_rrefs
    if islink(a):
      rref=path2rref(a)
      if rref is not None:
        keep_rrefs.append(rref)
      else:
        dref=path2dref(a)
        if dref is not None:
          keep_drefs.append(dref)

  for path in keep_paths:
    if islink(path):
      _check(path)
    elif isdir(path):
      for root, dirs, filenames in walk(path, topdown=True):
        for dirname in sorted(dirs):
          a=Path(abspath(join(root, dirname)))
          _check(a)
    else:
      pass
  return keep_drefs,keep_rrefs


def gc_candidates(keep:Tuple[List[DRef],List[RRef]])->Tuple[Set[DRef],Set[RRef]]:
  """ Query the garbage collector. GC removes any model which is not symlinked under
  `keep_dir` folder.

  Return the links to be removed. Run `gc(force=True)` to actually remove the
  links.  """
  return store_gc(keep_drefs=keep[0], keep_rrefs=keep[1])


def gc(keep_dirs:List[Path],
       interactive:bool=True,
       verbose:bool=True)->None:
  """ Simple console garbage collector. `gc` removes any model which is not
  symlinked under `keep_dir` and is not in short list of pre-defined models.

  Pass `interactive=False` to delete the data without request for confirmation.
  """
  import sys
  assert (not interactive) or sys.__stdin__.isatty(), (
    "`gc` needs TTY to be called with `interactive=True`" )
  assert not (verbose and not interactive), (
    "gc: `verbose=True` implies `interactive=True`" )

  drefs,rrefs=gc_candidates(gc_exceptions(keep_dirs))

  if verbose:
    total=0
    if len(drefs)+len(rrefs)>0:
      print("Objects to be removed:")
    rrefs_pairs=sorted([(rref, dirsize(rref2path(rref))) for rref in rrefs],
             key=lambda x:x[1])
    for dref in drefs:
      print(f"\t{dref}")
    for rref,sz in rrefs_pairs:
      print(f"{diskspace_h(sz)}\t{rref}")
      total+=sz
    print(f"{diskspace_h(total)}\ttotal")

  if interactive:
    print("Confirm removal? [yN]")
    ans=input()
    if ans.lower() != 'y':
      print("Cancelled by user")
      return

  for rref in rrefs:
    rmref(rref)
  for dref in drefs:
    rmref(dref)

