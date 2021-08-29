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
from time import sleep
import re
import os
from subprocess import Popen, PIPE
from select import select

Chunk=List[str]

def scanmd(fpath:str)->List[Chunk]:
  acc:list=[]; acc2:list=[]; inchunk=False
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

def readout(fdr, prompt:bytes=b'>>>',timeout:Optional[int]=10)->str:
  acc:bytes=b''
  while select([fdr],[],[],timeout)[0] != []:
    r=os.read(fdr, 1024);
    if r==b'':
      print('readout retval', acc.decode('utf-8').replace("\n","|"))
      return acc.decode('utf-8')
    print('... readout got', r.decode('utf-8').replace("\n","|"))
    acc+=r
    if search(prompt,acc,re.MULTILINE):
      print('readout match', acc.decode('utf-8').replace("\n","|"))
      return acc.decode('utf-8')
  print('readout timeout')
  return acc.decode('utf-8',acc.decode('utf-8').replace("\n","|"))


def interact(fdr, fdw, text:str, prompt:str='>>>')->str:
  print('Sending return')
  os.write(fdw,'\n\n\n'.encode())
  print('Waiting for prompt')
  readout(fdr)
  print('Sending the message')
  os.write(fdw,text.encode())
  os.write(fdw,'\n'.encode())
  print('Reading the answer')
  res=readout(fdr)
  print('Done')
  return res

def run():
  fdr=os.open('out.pipe', os.O_RDONLY | os.O_NONBLOCK | os.O_SYNC)
  fdw=os.open('inp.pipe', os.O_WRONLY | os.O_SYNC)
  # interact(fdr,fdw,'3+2')
  interact(fdr,fdw,'3+2')

# def interact(fpipe:str, chunk:Chunk)->None:
#   with open(fpipe,'w') as w:
#     w.write(
#   with open(fpipe,'r') as r:


