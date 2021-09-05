from pylightnix import *
from typing import List, Optional
from re import search, match as re_match
import re
import os
import sys
from select import select
from os import environ, system

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

def interact(fdr, fdw, text:str)->str:
  os.write(fdw,'3256748426384\n'.encode())
  x=readout(fdr,prompt=mkre('3256748426384\n'))
  os.write(fdw,text.encode())
  os.write(fdw,'\n'.encode())
  os.write(fdw,'3256748426384\n'.encode())
  res=readout(fdr,prompt=mkre('3256748426384\n'))
  return res

def scanmd(fpath:str)->Iterable[Tuple[Optional[str],
                                      Optional[List[str]]]]:
  acc:list=[]; inchunk=False
  f=sys.stdin if fpath=='-' else open(fpath,'r')
  for line in f.readlines():
    if inchunk:
      if search('^\s*```', line):
        inchunk=False;
        yield (None,acc)
      else:
        acc.append(line)
    else:
      if search('^\s*```',line):
        inchunk=True; acc=[]
      else:
        yield (line,None)

def use_session(inpath:str, outpath:str):
  fdw=os.open('_inp.pipe', os.O_WRONLY | os.O_SYNC)
  fdr=os.open('_out.pipe', os.O_RDONLY | os.O_SYNC)
  S=mkSS('_pylightnix')
  fsinit(S)

  def _realize(b:Build):
    print(f'Evaluating chunk {mklens(b).name.val}')
    res=interact(fdr,fdw,''.join(mklens(b).code.val))
    writestr(mklens(b).stdout.syspath,res)

  with current_registry(Registry(S)):
    prev:Optional[DRef]=None
    of=sys.stdout if outpath=='-' else open(outpath,'w')
    nchunk=0
    for line,chunk in scanmd(inpath):
      if line:
        of.write(line)
      if chunk:
        of.write('```python\n')
        of.write(''.join(chunk))
        of.write('```\n')
        cfg={'name':f'chunk_{nchunk}',
             'code':chunk,
             'prev':prev,
             'stdout':[selfref,'stdout.txt']}
        prev=mkdrv(mkconfig(cfg), match_only(), build_wrapper(_realize))
        rref=realize1(instantiate(prev))
        of.write('```\n')
        of.write(mklens(rref).stdout.contents)
        of.write('\n```\n')
        nchunk+=1

def start_session():
  system('kill $(cat _pid.txt) >/dev/null 2>&1')
  system('chmod -R +w _pylightnix 2>/dev/null && rm -rf _pylightnix')
  system('mkfifo _inp.pipe _out.pipe 2>/dev/null')
  if os.fork()==0:
    sys.stdout.close(); sys.stderr.close(); sys.stdin.close()
    system(('python -uic "import os; import sys; sys.ps1=\'\';'
            'os.open(\'_inp.pipe\',os.O_RDWR);'
            'os.open(\'_out.pipe\',os.O_RDWR);"'
            '<_inp.pipe >_out.pipe 2>&1 & echo $! >_pid.txt'))
    exit(0)

if __name__=='__main__':
  argv=sys.argv[1:]
  if len(argv)<2 or any([a in ['help','-h','--help'] for a in argv]):
    print(('Usage:\n\n'
           '    MDRUN [--restart] FILE.md.in FILE.md'
           '\n\n'
           '    Example: `cat test.md | python MDRUN.py - -`'
           '\n\n'
           'Execute Python code sections found in the input Markdown '
           'FILE.md.in. Create the output document FILE.md by pasting '
           'the result of each section below the original. '
           '"-" is accepted as a placeholder for STDIN or STDOUT.'
           '\n\n'
           'All Python code is executed in a Python interpreter running in '
           'the background. Its pid is saved in "_pid.txt" file and the '
           'communication go through named pipes "_inp.pipe" and "_out.pipe".'
           '\n\n'
           'MDRUN assumes that the latter sections depend on the earlier ones. '
           'Execution results are cached and stored in the Pylightnix cache '
           'storage folder "_pylightnix".'))
    sys.exit(1)
  if any([a in ['--restart','-r'] for a in argv]):
    start_session()
  if not os.path.isfile('_pid.txt'):
    start_session()
  use_session(*[a for a in argv if a=='-' or a[0]!='-'])
