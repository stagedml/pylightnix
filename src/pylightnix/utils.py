from pylightnix.imports import ( strftime, join, makedirs,
    symlink, basename, mkdir, isdir, isfile, islink, remove, sha256, EEXIST,
    json_dumps, json_loads, makedirs, replace, dirname, walk, abspath,
    normalize, re_sub, split, json_load, find_executable )

from pylightnix.types import ( Hash, Path, List, Any, Optional, Iterable, IO,
    DRef, RRef, Tuple)


def timestring()->str:
  return strftime("%m%d-%H:%M:%S%z")

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
  """ Calculate recursive SHA256 hash of a directory.
  FIXME: stop ignoring file/directory names
  Don't count files starting from underscope ('_')
  """
  assert isdir(path), f"dirhash(path) expects directory path, not '{path}'"

  def _iter()->Iterable[bytes]:
    for root, dirs, filenames in walk(abspath(path), topdown=True):
      for filename in filenames:
        if len(filename)>0 and filename[0] != '_':
          with open(abspath(join(root, filename)),'rb') as f:
            yield f.read()

  return datahash(_iter())

def scanref_list(l:list)->Tuple[List[DRef],List[RRef]]:
  """
  FIXME: Add a better reference detection, in the `assert_valid_ref` style
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

# def scanref_tuple(t:tuple)->Tuple[List[DRef],List[RRef]]:
#   assert isinstance(t,tuple)
#   return scanref_list(list(t))

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

def get_executable(name:str, not_found_message:str)->str:
  e=find_executable(name)
  assert e is not None, not_found_message
  return e

