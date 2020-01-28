from pylightnix.types import ( Iterable, List, Union, Optional, DRef, RRef )
from pylightnix.imports import ( isfile, isdir, listdir, join, rmtree )
from pylightnix.core import ( store_dref2path, rref2path, isrref, isdref )


def lsdref_(r:DRef)->Iterable[str]:
  p=store_dref2path(r)
  for d in listdir(p):
    p2=join(d,p)
    if isdir(p2):
      yield d

def lsrref_(r:RRef)->Iterable[str]:
  p=rref2path(r)
  for d in listdir(p):
    yield d

def lsref(r:Union[RRef,DRef])->List[str]:
  if isrref(r):
    return list(lsrref_(RRef(r)))
  elif isdref(r):
    return list(lsdref_(DRef(r)))
  else:
    assert False, f"Invalid reference {r}"

def catrref_(r:RRef, fn:List[str])->Iterable[str]:
  with open(join(rref2path(r),*fn),'r') as f:
    for l in f.readlines():
      yield l

def catref(r:str, fn:List[str])->List[str]:
  if isrref(r):
    return list(catrref_(RRef(r),fn))
  else:
    assert False, 'not implemented'

def rmrref(r:RRef)->None:
  rmtree(rref2path(r))

def rmdref(r:DRef)->None:
  rmtree(store_dref2path(r))

def rmref(r:Union[RRef,DRef])->None:
  if isrref(r):
    rmrref(RRef(r))
  elif isdref(r):
    rmdref(DRef(r))
  else:
    assert False, f"Invalid reference {r}"





