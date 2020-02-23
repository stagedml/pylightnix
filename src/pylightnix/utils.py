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

from pylightnix.imports import ( datetime, gmtime, timegm, join, makedirs,
    symlink, basename, mkdir, isdir, isfile, islink, remove, sha256, EEXIST,
    json_dumps, json_loads, makedirs, replace, dirname, walk, abspath,
    normalize, re_sub, split, json_load, find_executable, chmod, S_IWRITE, S_IREAD,
    S_IRGRP, S_IROTH, S_IXUSR, S_IXGRP, S_IXOTH, walk, stat, ST_MODE, S_IWGRP,
    S_IWOTH, rmtree, rename, getsize )

from pylightnix.types import ( Hash, Path, List, Any, Optional, Iterable, IO,
    DRef, RRef, Tuple, Callable )

from pylightnix.tz import tzlocal

#: Defines the `strftime`-compatible format of time, used in e.g.
#: `__buildtime__.txt` files. Do not change!
PYLIGHTNIX_TIME="%y%m%d-%H:%M:%S:%f%z"

def timestring(sec:Optional[float]=None)->str:
  """ Return a time string, representing the local time, with a timezone
  suffix. Resolution is subsecond, platform-dependent. """
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
  except ValueError as e:
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
  """ Create a `dst` symlink poinitnig to `src`. Overwrites existing files, if any """
  makedirs(dirname(dst),exist_ok=True)
  symlink(src,dst+'__',**kwargs)
  replace(dst+'__',dst)

def encode(s:str, encoding:str='utf-8')->bytes:
  return bytes(s, encoding)

def datahash(data:Iterable[bytes])->Hash:
  e=sha256()
  nitems=0
  for s in data:
    e.update(s)
    nitems+=1
  if nitems==0:
    print('Warning: datahash: called on empty iterator')
  return Hash(e.hexdigest())

def dirhash(path:Path)->Hash:
  """ Calculate recursive SHA256 hash of a directory. Ignore files with names
  starting with underscope ('_').

  FIXME: Include file/directory names into hash data
  """
  assert isdir(path), f"dirhash(path) expects directory path, not '{path}'"

  def _iter()->Iterable[bytes]:
    for root, dirs, filenames in walk(abspath(path), topdown=True):
      for filename in filenames:
        if len(filename)>0 and filename[0] != '_':
          with open(abspath(join(root, filename)),'rb') as f:
            yield f.read()

  return datahash(_iter())

def filerw(f:Path)->None:
  assert isfile(f)
  chmod(f, stat(f)[ST_MODE] | (S_IWRITE) )

def filero(f:Path)->None:
  assert isfile(f)
  chmod(f, stat(f)[ST_MODE] & ~(S_IWRITE | S_IWGRP | S_IWOTH) )

def dirro(o:Path)->None:
  for root, dirs, files in walk(o):
    for d in dirs:
      mode=stat(join(root, d))[ST_MODE]
      chmod(join(root, d), mode & ~(S_IWRITE | S_IWGRP | S_IWOTH) )
    for f in files:
      filero(Path(join(root, f)))
  chmod(o, stat(o)[ST_MODE] & ~(S_IWRITE | S_IWGRP | S_IWOTH) )

def dirrw(o:Path)->None:
  for root, dirs, files in walk(o):
    for d in dirs:
      mode=stat(join(root, d))[ST_MODE]
      chmod(join(root, d), mode | (S_IWRITE) )
    for f in files:
      filerw(Path(join(root, f)))
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
  try:
    tmppath=Path(path+'.tmp')
    rename(path,tmppath)
    dirrw(tmppath)
    rmtree(tmppath)
  except FileNotFoundError:
    if not ignore_not_found:
      raise

def scanref_list(l:list)->Tuple[List[DRef],List[RRef]]:
  """ Scan Python list of arbitraty data for References.

  FIXME: Add better detection criteia, at least like in `assert_valid_ref`
  """
  assert isinstance(l,list)
  drefs:List[DRef]=[]; rrefs:List[RRef]=[]
  for i in l:
    if isinstance(i,list):
      dref2,rref2=scanref_list(i)
    elif isinstance(i,dict):
      dref2,rref2=scanref_dict(i)
    elif isinstance(i,str):
      if i[:5]=='dref:':
        dref2=[DRef(i)]; rref2=[]
      elif i[:5]=='rref:':
        dref2=[]; rref2=[RRef(i)]
      else:
        dref2=[]; rref2=[]
    else:
      dref2=[]; rref2=[]
    drefs+=dref2; rrefs+=rref2
  return (drefs,rrefs)

def scanref_dict(obj:dict)->Tuple[List[DRef],List[RRef]]:
  assert isinstance(obj,dict)
  return scanref_list(list(obj.values()))

def dicthash(d:dict)->Hash:
  """ Calculate hashsum of a Python dict. Top-level fields starting from '_' are ignored """
  string="_".join(str(k)+"="+str(v) for k,v in sorted(d.items()) if len(k)>0 and k[0]!='_')
  return Hash(sha256(string.encode('utf-8')).hexdigest())

def assert_serializable(d:Any, argname:str='dict')->Any:
  error_msg=(f"Content of this '{argname}' of type {type(d)} is not JSON-serializable!"
             f"\n\n{d}\n\n"
             f"Make sure that `json.dumps`/`json.loads` work on it and are able "
             f"to preserve the value. Typically, we want to use only simple Python types"
             f"like lists, dicts, strings, ints, etc. In particular,"
             f"overloaded floats like `np.float32` don't work. Also, we"
             f"don't use Python tuples, because they default JSON implementation convert "
             f"them to lists")
  s=json_dumps(d)
  assert s is not None, error_msg
  d2=json_loads(s)
  assert str(d)==str(d2), error_msg
  return d2

def assert_valid_dict(d:dict, argname:str)->None:
  assert isinstance(d,dict)
  d2=assert_serializable(d, argname)
  h1=dicthash(d)
  h2=dicthash(d2)
  assert h1==h2

def readjson(json_path:str)->Any:
  with open((json_path), "r") as f:
    return json_load(f)

def tryread(path:Path)->Optional[str]:
  try:
    with open(path,'r') as f:
      return f.read()
  except Exception:
    return None

def trywrite(path:Path, data:str)->bool:
  try:
    with open(path,'w') as f:
      f.write(data)
    return True
  except Exception:
    return False

def try_executable(name:str, not_found_message:Optional[str]=None)->Callable[[],str]:
  e=find_executable(name)
  if e is None:
    def _err():
      assert False, not_found_message
      return f"<{name}_not_found>"
    return _err
  else:
    return lambda: str(e)

def get_executable(name:str, not_found_message:str)->str:
  e=try_executable(name)
  return e()

