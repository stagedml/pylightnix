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


""" Random utils and helper functions """


from pylightnix.imports import (datetime, gmtime, timegm, join, makedirs,
    symlink, basename, mkdir, isdir, isfile, islink, remove, sha256, EEXIST,
    json_dumps, json_loads, makedirs, replace, dirname, walk, abspath,
    normalize, re_sub, split, json_load, find_executable, chmod, S_IWRITE,
    S_IREAD, S_IRGRP, S_IROTH, S_IXUSR, S_IXGRP, S_IXOTH, stat, ST_MODE,
    S_IWGRP, S_IWOTH, rmtree, rename, getsize, readlink, partial, copytree,
    chain, getLogger, environ, defaultdict, PriorityQueue)

from pylightnix.types import (Union, Hash, Path, List, Any, Optional,
                              Iterable, IO, DRef, RRef, Tuple, Callable,
                              Set)

from typing import TypeVar
from pylightnix.tz import tzlocal

#: Defines the `strftime`-compatible format of time, used in e.g.
#: `__buildtime__.txt` files. Do not change!
PYLIGHTNIX_TIME="%y%m%d-%H:%M:%S:%f%z"

#: Placeholder for self-reference
PYLIGHTNIX_SELF_TAG = "__self__"

#: Self-reference marker. Intended to be used as a first item of `RefPath`s.
selfref = PYLIGHTNIX_SELF_TAG

logger=getLogger(__name__)
warning=logger.warning
info=logger.info
debug=logger.debug


def timestring(sec:Optional[float]=None)->str:
  """ Return a time string, representing the local time, with a timezone
  suffix. Resolution is subsecond, platform-dependent.

  Arguments:
  - `sec:Optional[float]=None` Number of seconds since Epoch to convert to
    a timestring. If none, take the current time.
  """
  if sec is None:
    dt=datetime.now(tzlocal())
  else:
    dt=datetime.fromtimestamp(sec,tz=tzlocal())
  return dt.strftime(PYLIGHTNIX_TIME)

def parsetime(time:str)->Optional[float]:
  """ Parses the time string into floating-seconds since the Epoch. String
  format is fixed and compatible with `timestring`. """
  try:
    return datetime.strptime(time,PYLIGHTNIX_TIME).timestamp()
  except ValueError:
    return None
  except OverflowError:
    return None

def logdir(tag:str, logrootdir:Path, timetag:Optional[str]=None):
  timetag=timestring() if timetag is None else timetag
  return join(logrootdir,((str(tag)+'_') if len(tag)>0 else '')+timetag)

def mklogdir(
    tag:str,
    logrootdir:Path,
    subdirs:list=[],
    symlinks:bool=True,
    timetag:Optional[str]=None)->Path:
  """ Create `<logrootdir>/<tag>_<time>` folder and set
  `<logrootdir>/_<tag>_latest` symlink to point to it. """
  logpath=logdir(tag, logrootdir=logrootdir, timetag=timetag)
  makedirs(logpath, exist_ok=True)
  if symlinks:
    linkname=join(logrootdir,(('_'+str(tag)+'_latest') if len(tag)>0 else '_latest'))
    try:
      symlink(basename(logpath),linkname)
    except OSError as e:
      if e.errno == EEXIST:
        remove(linkname)
        symlink(basename(logpath),linkname)
      else:
        raise e
  for sd in subdirs:
    makedirs(join(logpath,sd), exist_ok=True)
  return Path(logpath)

def forcelink(src:Path,dst:Path,**kwargs)->None:
  """ Create a `dst` symlink poinitnig to `src`. Overwrite existing files, if any """
  makedirs(dirname(dst),exist_ok=True)
  symlink(src,dst+'__',**kwargs)
  replace(dst+'__',dst)

def encode(s:str, encoding:str='utf-8')->bytes:
  return bytes(s, encoding)

def datahash(data:Iterable[Tuple[str,bytes]],
             verbose:bool=False)->Hash:
  e=sha256()
  nitems=0
  for hint,s in data:
    e.update(s)
    if verbose:
      debug(f'Adding {hint}: {e.hexdigest()}')
    nitems+=1
  if nitems==0:
    warning("datahash() was called with empty iterator")
  return Hash(e.hexdigest())

def dirhash_iter(path:Path)->Iterable[Tuple[str,bytes]]:
  assert isdir(path), f"dirhash() expects directory path, not '{path}'"
  for root, dirs, filenames in walk(abspath(path), topdown=True):
    for filename in sorted(filenames):
      if len(filename)>0 and filename[0] != '_':
        localpath=abspath(join(root, filename))
        if islink(localpath):
          yield (f'link:{localpath}',encode(readlink(localpath)))
        with open(localpath,'rb') as f:
          yield (localpath,f.read())

def dirshash(paths:Iterable[Path], verbose:bool=False)->Hash:
  """ Calculate recursive SHA256 hash of a directory. Ignore files with names
  starting with underscope ('_'). For symbolic links, hash the result of
  `readlink(link)`.

  FIXME: Include file/directory names the into hash data.
  FIXME: Figure out how does sha265sum handle symlinks and do the same thing.
  FIXME: Stop loading whole files in memory for calculating hashes
  """
  return datahash(chain.from_iterable([dirhash_iter(p) for p in paths]),
                  verbose=verbose)

def dirhash(path:Path, verbose:bool=False)->Hash:
  return dirshash([path], verbose=verbose)

def filehash(path:Path)->Hash:
  assert isfile(path), f"filehash() expects a file path, not '{path}'"
  with open(path,'rb') as f:
    return datahash([(path,f.read())])

def filerw(f:Path)->None:
  assert isfile(f), f"'{f}' is not a file"
  chmod(f, stat(f)[ST_MODE] | (S_IWRITE))

def filero(f:Path)->None:
  assert isfile(f), f"'{f}' is not a file"
  chmod(f, stat(f)[ST_MODE] & ~(S_IWRITE | S_IWGRP | S_IWOTH))

def dirro(o:Path)->None:
  for root, dirs, files in walk(o):
    for d in dirs:
      mode=stat(join(root, d))[ST_MODE]
      chmod(join(root, d), mode & ~(S_IWRITE | S_IWGRP | S_IWOTH) )
    for f in files:
      if isfile(f):
        filero(Path(join(root, f)))
      if islink(f):
        warning(f"Pylightnix doesn't guarantee the consistency of symlink '{f}'")
  chmod(o, stat(o)[ST_MODE] & ~(S_IWRITE | S_IWGRP | S_IWOTH) )

def dirrw(o:Path)->None:
  for root, dirs, files in walk(o):
    for d in dirs:
      mode=stat(join(root, d))[ST_MODE]
      chmod(join(root, d), mode | (S_IWRITE) )
    for f in files:
      if isfile(f):
        filerw(Path(join(root, f)))
      if islink(f):
        warning(f"Pylightnix doesn't guarantee the consistency of symlink '{f}'")
  chmod(o, stat(o)[ST_MODE] | (S_IWRITE | S_IWGRP | S_IWOTH) )


def dirsize(o:Path)->int:
  """ Return size in bytes """
  total_size=0
  for dirpath, dirnames, filenames in walk(o):
    for f in filenames:
      fp=join(dirpath, f)
      if not islink(fp):
        total_size += getsize(fp)
  return total_size

def dirchmod(o:Path, mode:str)->None:
  if mode=='ro':
    dirro(o)
  elif mode=='rw':
    dirrw(o)
  else:
    assert False, f"Attempt to set invalid mode {mode} for path {o}"

def dirrm(path:Path, ignore_not_found:bool=True)->None:
  """ Powerful folder remover. Firts rename it to the temporary name. Deal with
  possible write-protection. """
  # FIXME: May fail with 'Directory not empty' if tmppath is not empty.
  try:
    tmppath=Path(path+'.tmp')
    rename(path,tmppath)
    dirrw(tmppath)
    rmtree(tmppath)
  except FileNotFoundError:
    if not ignore_not_found:
      raise

def dircp(src:Path, dst:Path, make_rw:bool=False)->None:
  """ Powerful folder copyier. """
  assert isdir(src)
  assert not isdir(dst)
  tmppath=Path(dst+'.tmp')
  copytree(src,tmppath)
  if make_rw:
    dirrw(tmppath)
  rename(tmppath,dst)


def isrref(ref:Any)->bool:
  """ FIXME: Add better detection criteia, at least like in `assert_valid_ref` """
  return isinstance(ref,str) and len(ref)>=5+32+1+32 and ref[:5]=='rref:'

def isdref(ref:Any)->bool:
  return isinstance(ref,str) and len(ref)>=5+32 and ref[:5]=='dref:'

def isrefpath(p:Any)->bool:
  return isinstance(p,list) and len(p)>0 and isdref(p[0]) and all([isinstance(x,str) for x in p])

def isselfpath(p:Any)->bool:
  return isinstance(p,list) and len(p)>0 and all([isinstance(x,str) for x in p]) and \
         p[0]==PYLIGHTNIX_SELF_TAG

def isclosure(x:Any)->bool:
  return isinstance(x,tuple) and len(x)==4 and \
      isinstance(x[2],list) and all([isdref(r) for r in x[1]]) \
         and isinstance(x[2],list)

Mutator=Callable[[Any,Any],Any]

def traverse_tuple(t:tuple,mut:Mutator)->None:
  """ Traverse an arbitrary Python tuple. Forbids changing items. """
  assert isinstance(t,tuple)
  for i in range(len(t)):
    x=mut(i,t[i])
    assert x==t[i], "Can't change tuple item"
    if isinstance(t[i],list):
      scanref_list(t[i])
    elif isinstance(t[i],dict):
      traverse_dict(t[i],mut)
    elif isinstance(t[i],tuple):
      traverse_tuple(t[i],mut)

def traverse_list(l:list,mut:Mutator)->None:
  """ Traverse an arbitrary Python list. """
  assert isinstance(l,list)
  for i in range(len(l)):
    l[i]=mut(i,l[i])
    if isinstance(l[i],list):
      traverse_list(l[i],mut)
    elif isinstance(l[i],dict):
      traverse_dict(l[i],mut)
    elif isinstance(l[i],tuple):
      traverse_tuple(l[i],mut)

def traverse_dict(d:dict, mut:Mutator)->None:
  """ Traverse an arbitrary Python dict. """
  assert isinstance(d,dict)
  for k in d.keys():
    d[k]=mut(k,d[k])
    if isinstance(d[k],list):
      traverse_list(d[k],mut)
    elif isinstance(d[k],dict):
      traverse_dict(d[k],mut)
    elif isinstance(d[k],tuple):
      traverse_tuple(d[k],mut)

def scanref_list(l:list)->Tuple[List[DRef],List[RRef]]:
  drefs=[];rrefs=[]
  def _mutator(key,val):
    nonlocal drefs,rrefs
    if isrref(val):
      rrefs.append(RRef(val))
    elif isdref(val):
      drefs.append(DRef(val))
    return val
  traverse_list(l, _mutator)
  return (drefs,rrefs)

def scanref_dict(d:dict)->Tuple[List[DRef],List[RRef]]:
  assert isinstance(d,dict)
  return scanref_list(list(d.values()))

def dicthash(d:dict)->Hash:
  """ Calculate hashsum of a Python dict. Top-level fields starting from '_' are
  ignored """
  string="_".join(str(k)+"="+str(v) for k,v in sorted(d.items()) \
                  if len(k)>0 and k[0]!='_')
  return Hash(sha256(string.encode('utf-8')).hexdigest())

def assert_serializable(d:Any, argname:str='dict')->Any:
  error_msg=(f"Content of this '{argname}' of type {type(d)} is not "
             f"JSON-serializable!\n\n{d}\n\n"
             f"Make sure that `json.dumps`/`json.loads` work on it and are "
             f"are to preserve the value. Typically, we want to use only "
             f"simple Python types"
             f"like lists, dicts, strings, ints, etc. In particular,"
             f"overloaded floats like `np.float32` don't work. Also, we"
             f"don't allow Python tuples, because the default JSON "
             f"serialization converts them to lists.")
  s=json_dumps(d)
  assert s is not None, error_msg
  d2=json_loads(s)
  assert str(d)==str(d2), error_msg
  return d2

def assert_valid_dict(d:dict, argname:str)->dict:
  assert isinstance(d,dict)
  d2=assert_serializable(d, argname)
  h1=dicthash(d)
  h2=dicthash(d2)
  assert h1==h2
  return d

def readstr(path:str)->str:
  with open(path,'r') as f:
    return f.read()

def writestr(path:str, data:str)->None:
  with open(path,'w') as f:
    f.write(data)

def writejson(path:str,
              data:Union[dict,list,int,float,bool],
              indent:Optional[int]=None)->None:
  writestr(path, json_dumps(data, indent=indent))

def readjson(json_path:str)->Any:
  with open(json_path, "r") as f:
    return json_load(f)

_A=TypeVar('_A')
_B=TypeVar('_B')
def trycatch(f:Callable[[],_A], default:_A, mp:Callable[[_A],_B])->_B:
  """ FIXME: don't handle all exceptions, handle only string-related ones """
  try:
    return mp(f())
  except KeyboardInterrupt:
    raise
  except Exception:
    return mp(default)

def tryreadjson(json_path:str)->Optional[Any]:
  none:Optional[Any]=None
  return trycatch(partial(readjson,json_path=json_path),none,lambda x:x)

C=TypeVar('C')
def maybereadjson(path:str,default:Any,mp:Callable[[Any],C])->C:
  return trycatch(partial(readjson,json_path=path),default,mp)

def tryreadstr(path:str)->Optional[str]:
  none:Optional[str]=None
  return trycatch(partial(readstr, path=path),none,lambda x:x)

D=TypeVar('D')
def maybereadstr(path:str,default:str,mp:Callable[[str],D])->D:
  return trycatch(partial(readstr, path=path),default,mp)

def tryreadjson_def(json_path:str, default:Any)->Any:
  return trycatch(partial(readjson,json_path=json_path),default,lambda x:x)

def tryreadstr_def(path:str, default:str)->str:
  return trycatch(partial(readstr, path=path),default,lambda x:x)

def tryread(path:Path)->Optional[str]:
  none:Optional[str]=None
  return trycatch(partial(readstr,path=path),none,lambda x:x)

def tryread_def(path:Path, default:str)->str:
  return trycatch(partial(readstr,path=path),default,lambda x:x)

def trywrite(path:Path, data:str)->bool:
  def _do():
    writestr(path,data)
    return True
  return trycatch(_do,False,lambda x:x)

def try_executable(name:str,
                   envname:str,
                   not_found_message:Optional[str],
                   not_found_warning:Optional[str])->Callable[[],str]:
  e=environ.get(envname)
  if e is None:
    e=find_executable(name)
  if e is None:
    warning(not_found_message)
    warning(not_found_warning)
    def _err()->str:
      assert False, not_found_message
    return _err
  else:
    info(f"Using {name} system executable: {e}")
    return lambda: str(e)

def concat(l:List[List[Any]])->List[Any]:
  return list(chain.from_iterable(l))

def kahntsort(nodes:Iterable[Any],
              inbounds:Callable[[Any],Set[Any]])->Optional[List[Any]]:
  """ Kahn's algorithm for topological sorting. Takes iterable `nodes` and
  pure-function `inbounds`. Output list of nodes in topological order, or None
  if graph has cycle.

  One modification is that we use PriorityQueue insted of plain list to put
  take name-order into account.
  """
  indeg:dict={}
  outbounds:dict=defaultdict(set)
  q:PriorityQueue=PriorityQueue()
  sz:int=0
  for n in nodes:
    ns=inbounds(n)
    outbounds[n]|=set()
    indeg[n]=0
    for inn in ns:
      outbounds[inn].add(n)
      indeg[n]+=1
    if indeg[n]==0:
      q.put(n)
    sz+=1

  acc=[]
  cnt=0
  while not q.empty():
    n=q.get()
    acc.append(n)
    for on in outbounds[n]:
      indeg[on]-=1
      if indeg[on]==0:
        q.put(on)
    cnt+=1

  return None if cnt>sz else acc

def dagroots(sorted_nodes:List[Any],
             inbounds:Callable[[Any],Set[Any]])->Set[Any]:
  """ Return a set of root nodes of a DAG. DAG should be topologically sorted.
  """
  nonroots=set()
  acc=set()
  for node in reversed(sorted_nodes):
    if node not in nonroots:
      acc.add(node)
    nonroots|=inbounds(node)
  return acc


