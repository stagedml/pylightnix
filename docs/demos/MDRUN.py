from pylightnix import (StorageSettings, Matcher, Build, Context, Path, RefPath,
                        Config, Manager, RRef, DRef, Path, build_path,
                        build_outpath, build_cattrs, mkdrv, rref2path, mkconfig,
                        tryread, fetchurl, instantiate, realize, match_only,
                        build_wrapper, selfref, mklens, instantiate_inplace,
                        realize_inplace, rmref, fsinit, allrrefs,
                        gc, redefine, match_some, match_latest, dirrm,
                        mksettings, readstr, writestr, context_deref, rrefctx,
                        rref2dref, realizeAll)
from typing import List, Optional
from re import search, fullmatch, match
from time import sleep
import re
import os
from subprocess import Popen, PIPE, call, DEVNULL
from select import select
from os import environ, system, spawnl

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

def mkre(prompt:str):
  return re.compile(f"(.*)(?={prompt})|{prompt}".encode('utf-8'),
                    re.A|re.MULTILINE|re.DOTALL)

def readout(fdr, prompt=mkre('>>>'),timeout:Optional[int]=10)->str:
  acc:bytes=b''
  while select([fdr],[],[],timeout)[0] != []:
    r=os.read(fdr, 1024);
    if r==b'':
      print('readout retval', acc.decode('utf-8').replace("\n","|"))
      return acc.decode('utf-8')
    acc+=r
    print('... readout got', acc.decode('utf-8').replace("\n","|"))
    m=match(prompt,acc)
    if m:
      ans=m.group(1)
      print('readout match:', ans.decode('utf-8').replace("\n","|"))
      return ans.decode('utf-8')
  print('readout timeout')
  return acc.decode('utf-8').replace("\n","|")


def interact(fdr, fdw, text:str, prompt:str='>>>')->str:
  print('Sending return')
  os.write(fdw,'32567\n'.encode())
  print('Waiting for prompt')
  readout(fdr,prompt=mkre('32567\n>>>'))
  print('Sending the message')
  os.write(fdw,text.encode())
  os.write(fdw,'\n'.encode())
  print('Reading the answer')
  res=readout(fdr)
  print('Done')
  return res

def run():
  fdr=os.open('_out.pipe', os.O_RDONLY | os.O_SYNC)
  fdw=os.open('_inp.pipe', os.O_WRONLY | os.O_SYNC)
  # interact(fdr,fdw,'3+2')
  interact(fdr,fdw,'3+2')

def mdrun():
  environ['PYLIGHTNIX_ROOT']='_pylightnix'
  fsinit()
  chunks=scanmd('_test.md')
  fdw=os.open('_inp.pipe', os.O_WRONLY | os.O_SYNC)
  fdr=os.open('_out.pipe', os.O_RDONLY | os.O_SYNC)
  try:

    def _make(b:Build):
      print(f'Executing {mklens(b).name.val}')
      res=interact(fdr,fdw,''.join(mklens(b).code.val))
      writestr(mklens(b).stdout.syspath,res)

    def _stages(m:Manager)->List[DRef]:
      acc:list=[]
      for i,chunk in enumerate(chunks):
        cfg={'name':f'chunk_{i}',
             'code':chunk,
             'prev':acc[-1] if len(acc)>0 else None,
             'stdout':[selfref,'stdout.txt']}
        dref=mkdrv(m,mkconfig(cfg),match_only(),build_wrapper(_make))
        acc.append(dref)
      return acc

    ctx=realizeAll(instantiate(_stages))
    for i,dref in enumerate(ctx):
      print(f'Querying chunk {i}')
      print(mklens(dref,ctx=ctx).stdout.contents)
  finally:
    os.close(fdr)
    os.close(fdw)

def start_session():
  system('kill $(cat _pid.txt) >/dev/null 2>&1')
  system('chmod -R +w _pylightnix 2>/dev/null && rm -rf _pylightnix')
  system('mkfifo _inp.pipe _out.pipe 2>/dev/null')
  if os.fork()==0:
    system(('python -uic "import os;'
            'os.open(\'_inp.pipe\',os.O_RDWR);'
            'os.open(\'_out.pipe\',os.O_RDWR);"'
            '<_inp.pipe >_out.pipe 2>&1 & echo $! >_pid.txt'))



