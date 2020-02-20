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

from pylightnix.types import ( Closure, Context, Derivation, RRef, DRef, List,
    Tuple, Optional, Generator, Path, Build, Union  )

from pylightnix.core import ( realizeSeq, store_realize, RealizeSeqGen,
    mkbuild, build_outpaths )

class ReplHelper:
  def __init__(self, gen:RealizeSeqGen)->None:
    self.gen:Optional[RealizeSeqGen]=gen
    self.dref:Optional[DRef]=None
    self.context:Optional[Context]=None
    self.drv:Optional[Derivation]=None
    self.build:Optional[Build]=None
    self.rrefs:Optional[List[RRef]]=None

def repl_continueMany(rh:ReplHelper, out_paths:Optional[List[Path]]=None)->Optional[List[RRef]]:
  try:
    assert rh.gen is not None
    assert rh.dref is not None
    assert rh.context is not None
    assert rh.drv is not None
    if out_paths is None:
      if rh.build is not None:
        out_paths=build_outpaths(rh.build)
        rh.build=None
    rrefs:Optional[List[RRef]]
    if out_paths is not None:
      rrefs=[store_realize(rh.dref,rh.context,out_path) for out_path in out_paths]
    else:
      rrefs=None
    rh.dref,rh.context,rh.drv=rh.gen.send((rrefs,False))
  except StopIteration as e:
    rh.gen=None
    rh.build=None
    rh.rrefs=e.value
  return rh.rrefs

PYLIGHTNIX_REPL_HELPER:Optional[ReplHelper]=None

def repl_continue(out_paths:Optional[List[Path]]=None, rh:Optional[ReplHelper]=None)->Optional[RRef]:
  global PYLIGHTNIX_REPL_HELPER
  if rh is None:
    rh=PYLIGHTNIX_REPL_HELPER
  assert rh is not None
  rrefs=repl_continueMany(rh, out_paths)
  if rrefs is None:
    return None
  assert len(rrefs)==1, f"Acturally {len(rrefs)}"
  return rrefs[0]

def repl_continueBuild(b:Optional[Build]=None, rh:Optional[ReplHelper]=None)->Optional[RRef]:
  if b is None:
    b=repl_build(rh)
  assert b is not None
  return repl_continue(out_paths=b.outpaths, rh=rh)

def repl_realize(closure:Closure, force_interrupt:Union[List[DRef],bool]=True)->ReplHelper:
  global PYLIGHTNIX_REPL_HELPER
  force_interrupt_:List[DRef]=[]
  if isinstance(force_interrupt,bool):
    if force_interrupt:
      force_interrupt_=[closure.dref]
  elif isinstance(force_interrupt,list):
    force_interrupt_=list(force_interrupt)
  else:
    assert False, "Invalid argument"
  rh=ReplHelper(realizeSeq(closure,force_interrupt_))
  PYLIGHTNIX_REPL_HELPER=rh
  assert rh.gen is not None
  try:
    rh.dref,rh.context,rh.drv=next(rh.gen)
  except StopIteration as e:
    rh.gen=None
    rh.build=None
    rh.rrefs=e.value
  return rh

def repl_rrefs(rh:ReplHelper)->Optional[List[RRef]]:
  return rh.rrefs

def repl_rref(rh:ReplHelper)->Optional[RRef]:
  rrefs=repl_rrefs(rh)
  if rrefs is None:
    return None
  assert len(rrefs)==1
  return rrefs[0]

def repl_build(rh:Optional[ReplHelper]=None, buildtime:bool=True)->Build:
  global PYLIGHTNIX_REPL_HELPER
  if rh is None:
    rh=PYLIGHTNIX_REPL_HELPER
  assert rh is not None
  assert rh.gen is not None
  assert rh.dref is not None
  assert rh.context is not None
  if rh.build is None:
    rh.build=mkbuild(rh.dref, rh.context, buildtime=buildtime)
  return rh.build

def repl_cancel(rh:Optional[ReplHelper]=None)->None:
  global PYLIGHTNIX_REPL_HELPER
  if rh is None:
    rh=PYLIGHTNIX_REPL_HELPER
  assert rh is not None
  try:
    assert rh.gen is not None
    rh.gen.send((None,True))
  except StopIteration as e:
    rh.gen=None
    rh.build=None

