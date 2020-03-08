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

""" Repl module defines variants of `instantiate` and `realize` functions, which
are suitable for REPL shells. Repl-friendly wrappers (see `repl_realize`) could
pause the computation, save the Pylightnix state into a variable and return to
the REPL's main loop. At this point user could alter the state of the whole
system.  Finally, `repl_continue` or `repl_cancel` could be called to either
continue or cancel the realization.
"""

from pylightnix.utils import ( dirrm, timestring )

from pylightnix.types import ( Dict, Closure, Context, Derivation, RRef, DRef,
    List, Tuple, Optional, Generator, Path, Build, Union, Any, BuildArgs,
    RealizeArg  )

from pylightnix.core import ( realizeSeq, store_realize, RealizeSeqGen,
    mkbuildargs, build_outpaths )

class ReplHelper:
  def __init__(self, gen:RealizeSeqGen)->None:
    self.gen:Optional[RealizeSeqGen]=gen
    self.dref:Optional[DRef]=None
    self.context:Optional[Context]=None
    self.drv:Optional[Derivation]=None
    self.rrefs:Optional[List[RRef]]=None
    self.rarg:Optional[RealizeArg]=None

ERR_INVALID_RH="Neither global, nor user-defined ReplHelper is valid"
ERR_INACTIVE_RH="REPL session is not paused or was already unpaused"

PYLIGHTNIX_REPL_HELPER:Optional[ReplHelper]=None

def repl_continueMany(out_paths:Optional[List[Path]]=None,
                      out_rrefs:Optional[List[RRef]]=None,
                      rh:Optional[ReplHelper]=None)->Optional[List[RRef]]:
  global PYLIGHTNIX_REPL_HELPER
  if rh is None:
    rh=PYLIGHTNIX_REPL_HELPER
  assert rh is not None, ERR_INVALID_RH
  assert rh.gen is not None, ERR_INACTIVE_RH
  assert rh.dref is not None, ERR_INACTIVE_RH
  assert rh.context is not None, ERR_INACTIVE_RH
  assert rh.drv is not None, ERR_INACTIVE_RH
  try:
    rrefs:Optional[List[RRef]]
    if out_paths is not None:
      assert out_rrefs is None
      rrefs=[store_realize(rh.dref,rh.context,out_path) for out_path in out_paths]
    elif out_rrefs is not None:
      assert out_paths is None
      rrefs=out_rrefs
    else:
      rrefs=None
    rh.dref,rh.context,rh.drv,rh.rarg=rh.gen.send((rrefs,False))
  except StopIteration as e:
    rh.gen=None
    rh.rrefs=e.value
  return rh.rrefs

def repl_continue(out_paths:Optional[List[Path]]=None,
                  out_rrefs:Optional[List[RRef]]=None,
                  rh:Optional[ReplHelper]=None)->Optional[RRef]:
  rrefs=repl_continueMany(out_paths,out_rrefs,rh)
  if rrefs is None:
    return None
  assert len(rrefs)==1, f"Acturally {len(rrefs)}"
  return rrefs[0]

def repl_continueBuild(b:Build, rh:Optional[ReplHelper]=None)->Optional[RRef]:
  return repl_continue(out_paths=b.outpaths, rh=rh)

def repl_realize(closure:Closure,
                 force_interrupt:Union[List[DRef],bool]=True,
                 realize_args:Dict[DRef,RealizeArg]={})->ReplHelper:
  """
  TODO

  Example:
  ```python
  rh=repl_realize(instantiate(mystage), force_interrupt=True)
  # ^^^ `repl_realize` returnes the `ReplHelper` object which holds the state of
  # incomplete realization
  b:Build=repl_build()
  # ^^^ Access it's build object. Now we may think that we are inside the
  # realization function. Lets do some hacks.
  with open(join(build_outpath(b),'artifact.txt'), 'w') as f:
    f.write("Fooo")
  repl_continueBuild(b)
  rref=repl_rref(rh)
  # ^^^ Since we didn't program any other pasues, we should get the usual RRef
  # holding the result of our hacks.
  ```
  """
  global PYLIGHTNIX_REPL_HELPER
  force_interrupt_:List[DRef]=[]
  if isinstance(force_interrupt,bool):
    if force_interrupt:
      force_interrupt_=[closure.dref]
  elif isinstance(force_interrupt,list):
    force_interrupt_=list(force_interrupt)
  else:
    assert False, "Invalid argument"
  rh=ReplHelper(realizeSeq(closure,force_interrupt_,realize_args=realize_args))
  PYLIGHTNIX_REPL_HELPER=rh
  assert rh.gen is not None, ERR_INACTIVE_RH
  try:
    rh.dref,rh.context,rh.drv,rh.rarg=next(rh.gen)
  except StopIteration as e:
    rh.gen=None
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

def repl_buildargs(rh:Optional[ReplHelper]=None, buildtime:bool=True)->BuildArgs:
  global PYLIGHTNIX_REPL_HELPER
  if rh is None:
    rh=PYLIGHTNIX_REPL_HELPER
  assert rh is not None, ERR_INVALID_RH
  assert rh.context is not None, ERR_INACTIVE_RH
  assert rh.dref is not None, ERR_INACTIVE_RH
  assert rh.rarg is not None, ERR_INACTIVE_RH
  timeprefix=timestring() if buildtime else None
  return mkbuildargs(rh.dref, rh.context, timeprefix, {}, rh.rarg)

def repl_build(rh:Optional[ReplHelper]=None, buildtime:bool=True)->Build:
  return Build(repl_buildargs(rh, buildtime))

def repl_cancel(rh:Optional[ReplHelper]=None)->None:
  global PYLIGHTNIX_REPL_HELPER
  if rh is None:
    rh=PYLIGHTNIX_REPL_HELPER
  assert rh is not None, ERR_INVALID_RH
  try:
    assert rh.gen is not None
    while True:
      rh.gen.send((None,True))
  except StopIteration as e:
    rh.gen=None

def repl_cancelBuild(b:Build, rh:Optional[ReplHelper]=None)->None:
  repl_cancel(rh)
  for o in b.outpaths:
    dirrm(o)

