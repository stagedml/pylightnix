from pylightnix import *
from typing import List, Optional
from re import search, match as re_match
import re
import os
import sys
from select import select
from os import environ, system

Chunk=List[str]

def scanmd(fpath:str)->List[Chunk]:
  acc:list=[]; acc2:list=[]; inchunk=False
  for line in open(fpath).readlines():
    if inchunk:
      if search('^\s*```', line):
        inchunk=False
        acc2.append(acc); acc=[]
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
      return acc.decode('utf-8')
    acc+=r
    m=re_match(prompt,acc)
    if m:
      ans=m.group(1)
      return ans.decode('utf-8')
  return acc.decode('utf-8').replace("\n","|")

def interact(fdr, fdw, text:str, prompt:str='>>>')->str:
  os.write(fdw,'32567\n'.encode())
  readout(fdr,prompt=mkre('32567\n>>>'))
  os.write(fdw,text.encode())
  os.write(fdw,'\n'.encode())
  res=readout(fdr)
  return res

def use_session(inpath:str, outpath:str):
  environ['PYLIGHTNIX_ROOT']='_pylightnix'
  fsinit()
  chunks=scanmd(inpath)
  fdw=os.open('_inp.pipe', os.O_WRONLY | os.O_SYNC)
  fdr=os.open('_out.pipe', os.O_RDONLY | os.O_SYNC)
  try:
    def _make(b:Build):
      print(f'Evaluating chunk {mklens(b).name.val}')
      res=interact(fdr,fdw,''.join(mklens(b).code.val))
      writestr(mklens(b).stdout.syspath,res)

    def _stages(m:Manager)->Dict[int,DRef]:
      cache={}; prev:Optional[DRef]=None
      for i,chunk in enumerate(chunks):
        cfg={'name':f'chunk_{i}',
             'code':chunk,
             'prev':prev,
             'stdout':[selfref,'stdout.txt']}
        cache[i]=mkdrv(m,mkconfig(cfg),match_only(),build_wrapper(_make))
        prev=cache[i]
      return cache

    cache,ctx=realizeAll(instantiate(_stages))
  finally:
    os.close(fdr)
    os.close(fdw)

  for i,chunk in enumerate(chunks):
    print(f'Querying chunk {i}:')
    print(mklens(cache[i],ctx=ctx).stdout.contents)

def start_session():
  system('kill $(cat _pid.txt) >/dev/null 2>&1')
  system('chmod -R +w _pylightnix 2>/dev/null && rm -rf _pylightnix')
  system('mkfifo _inp.pipe _out.pipe 2>/dev/null')
  if os.fork()==0:
    system(('python -uic "import os;'
            'os.open(\'_inp.pipe\',os.O_RDWR);'
            'os.open(\'_out.pipe\',os.O_RDWR);"'
            '<_inp.pipe >_out.pipe 2>&1 & echo $! >_pid.txt'))

if __name__=='__main__':
  argv=sys.argv[1:]
  if len(argv)<2 or any([a in ['help','-h','--help'] for a in argv]):
    print(('Usage:\n'
           '    MDRUN [--restart] FILE.md.in FILE.md\n'
           'Executes all the Python code sections of the input Markdown '
           'document. Paste the result of each section below the original '
           'section in the output document.\n'
           'All Python code is executed in a Python interpreter running in '
           'the background. Its pid is saved in "_pid.txt" file and the '
           'communication go through named pipes "_inp.pipe" and "_out.pipe".\n'
           'MDRUN assumes that the latter sections depend on the earlier ones. '
           'Execution results are cached and stored in the Pylightnix cache '
           'storage folder "_pylightnix".'))
    sys.exit(1)
  if argv[0] in ['--restart','-r']:
    start_session(); argv=argv[1:]
  if not os.path.isfile('_pid.txt'):
    start_session()
  use_session(argv[0],argv[1])
