from pylightnix.imports import ( strftime, join, makedirs,
    symlink, basename, mkdir, isdir, isfile, islink, remove, sha256, EEXIST,
    json_dumps, json_loads, makedirs, replace, dirname, walk, abspath,
    normalize, re_sub, split )

from pylightnix.types import ( Hash, Path, List, Any, Optional, Iterable, IO,
    DRef, IRef, Ref)


def timestring()->str:
  return strftime("%m%d-%H:%M:%S")

def logdir(tag:str, logrootdir:Path, timetag:Optional[str]=None):
  timetag=timestring() if timetag is None else timetag
  return join(logrootdir,((str(tag)+'_') if len(tag)>0 else '')+timetag)

def mklogdir(
    tag:str,
    logrootdir:Path,
    subdirs:list=[],
    symlinks:bool=True,
    timetag:Optional[str]=None)->Path:
  """ Creates `<logrootdir>/<tag>_<time>` folder and  `<logrootdir>/_<tag>_latest` symlink to
  it. """
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
    mkdir(logpath+'/'+sd)
  return Path(logpath)

def splitpath(p:Path)->List[str]:
  """ Return folders of path as a list """
  path=str(p)
  parts=[]
  while True:
    path,fname=split(path)
    if len(fname)>0:
      parts.append(fname)
    if len(path)==0 or path[-1]=='/':
      break
  return list(reversed(parts))

def forcelink(src:Path,dst:Path,**kwargs)->None:
  """ Create a `dst` symlink poinitnig to `src`. Overwrites existing files, if any """
  makedirs(dirname(dst),exist_ok=True)
  symlink(src,dst+'__',**kwargs)
  replace(dst+'__',dst)

def slugify(value:str)->str:
  """ Normalizes string, converts to lowercase, removes non-alpha characters,
  and converts spaces to hyphens.

  Ref. https://stackoverflow.com/a/295466/1133157
  """
  value = str(value)
  value = normalize('NFKC', value)
  value = re_sub(r'[^\w\s-]', '', value.lower()).strip()
  value = re_sub(r'[-\s]+', '-', value)
  return value

def datahash(data:Iterable[str])->Hash:
  e=sha256()
  nitems=0
  for s in data:
    e.update(s)
    items+=1
  if items==0:
    print('Warning: datahash: called on empty iterator')
  return Hash(e.hexdigest())


def dhash(path:Path)->Hash:
  """ Calculate recursive SHA256 hash of a directory.
  FIXME: stop ignoring file/directory names
  Don't count files starting from underscope ('_')
  """
  assert isdir(path), f"dhash(path) expects directory path, not '{path}'"

  def _iter()->Iterable[Path]:
    for root, dirs, filenames in walk(abspath(path), topdown=True):
      for filename in filenames:
        if len(filename)>0 and filename[0] != '_':
          with open(abspath(join(root, filename)),'r') as f:
            yield f.read()

  return datashash(_iter())

def scanref_list(l:list)->List[Ref]:
  """
  FIXME: Add a better reference detection, in the `assert_valid_ref` style
  """
  assert isinstance(l,list)
  res:list=[]
  for i in l:
    if isinstance(i,tuple):
      res+=scanref_tuple(i)
    elif isinstance(i,list):
      res+=scanref_list(i)
    elif isinstance(i,dict):
      res+=scanref_dict(i)
    elif isinstance(i,str):
      if i[:5]=='dref:':
        res.append(DRef(i))
      elif i[:5]=='iref:':
        res.append(IRef(i))
      else:
        pass # just a regular string
  return res

def scanref_tuple(t:tuple)->List[Ref]:
  assert isinstance(t,tuple)
  return scanref_list(list(t))

def scanref_dict(obj:dict)->List[Ref]:
  assert isinstance(obj,dict)
  return scanref_list(list(obj.values()))


def dicthash(d:dict)->Hash:
  """ Calculate hashsum of a Python dict. Top-level fields starting from '_' are ignored """
  string="_".join(str(k)+"="+str(v) for k,v in sorted(d.items()) if len(k)>0 and k[0]!='_')
  return Hash(sha256(string.encode('utf-8')).hexdigest())

def assert_serializable(d:Any, argname:str)->Any:
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
  d2=assert_serializable(d, argname)
  assert dicthash(d)==dicthash(d2)

def readjson(json_path:str)->Any:
  with open(json_path), "r") as f:
    return json_load(f)

