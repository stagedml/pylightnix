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

""" Trivial builtin stages """

from pylightnix.imports import (join, deepcopy, dirname, makedirs, isfile,
                                isdir, defaultdict)
from pylightnix.core import (mkdrv, mkconfig, assert_valid_name,
                             datahash, cfgdict,
                             assert_valid_refpath, rref2path,
                             drefcfg_, match_only)
from pylightnix.build import (build_outpath,
                              build_paths, build_deref_, build_wrapper)
from pylightnix.types import (RefPath, Registry, Context, Build, Name, DRef,
                              RRef, Any, Optional, Dict, Hash, Path, List,
                              Callable, Matcher, Realizer, Stage, Config,
                              RealizeArg, SPath, Output, StorageSettings)
from pylightnix.utils import (forcelink, isrefpath, traverse_dict)


def mknode(r:Registry,
           cfgdict:dict,
           artifacts:Dict[Name,bytes]={},
           name:str='mknode')->DRef:
  config=deepcopy(cfgdict)
  config['name']=name
  assert '__artifacts__' not in config, \
      "config shouldn't contain reserved field '__artifacts__'"
  config.update({'__artifacts__':{an:Hash(datahash([('artifact',av)]))
                 for (an,av) in artifacts.items()}})
  def _realize(b:Build)->None:
    o=build_outpath(b)
    for an,av in artifacts.items():
      with open(join(o,an),'wb') as f:
        f.write(av)
  return mkdrv(mkconfig(config), match_only(), build_wrapper(_realize), r)

# def mkfile(r:Registry,
#            name:Name,
#            contents:bytes,
#            filename:Optional[Name]=None)->DRef:
#   filename_:Name=filename if filename is not None else name
#   return mknode(r, config_dict={'output':[promise,filename_]},
#                    artifacts={filename_:contents})

def redefine(stage:Any,
             new_config:Callable[[dict],None]=lambda x:None,
             new_matcher:Optional[Matcher]=None,
             new_realizer:Optional[Realizer]=None)->Any:
  """ Define a new Derivation based on the existing one, by updating it's
  config, optionally re-writing it's matcher, or it's realizer.

  Arguments:
  - `stage:Any` a `Stage` function, accepting arbitrary keyword arguments
  - `new_config:Callable[[dict],None]` A function to update the `dref`'s config.
    Default varsion makes no changes.
  - `new_matcher:Optional[Matcher]=None` Optional new matcher (defaults to the
    existing matcher)
  - `new_realizer:Optional[Realizer]=None` Optional new realizer (defaults to
    the existing realizer)

  Return:
  A callable `Stage`, accepting pass-through arguments

  Example:
  ```python
  def _new_config(old_config):
    old_config['learning_rate'] = 1e-5
    return mkconfig(old_config)
  realize1(instantiate(redefine(myMLmodel, _new_config)))
  ```

  FIXME: Updating configs is dangerous: it changes its dref and thus breaks
  dependencies. Only top-level stages should use `new_confid` currently.
  """
  def _new_stage(*args,r=None,**kwargs)->DRef:
    dref=stage(*args,r=r,**kwargs) # type:ignore
    d=cfgdict(drefcfg_(dref,S=r.S))
    new_config(d)
    new_matcher_=new_matcher if new_matcher is not None\
                             else r.builders[dref].matcher
    new_realizer_=new_realizer if new_realizer is not None\
                               else r.builders[dref].realizer
    del r.builders[dref] # Pretend that it did not exist
    return mkdrv(mkconfig(d), new_matcher_, new_realizer_, r)
  return _new_stage

def realized(stage:Any)->Stage:
  """ Asserts that the stage doesn't requre running its realizer.
  [Re-defines](#pylightnix.stages.trivial.redefine) stage realizer with a dummy
  realizer triggering an assertion.

  Example:
  ```python
  rref:RRef=realize1(instantiate(realized(my_long_running_stage, arg="bla")))
  # ^^^ Fail if `my_long_running_stage` is not yet realized.
  ```
  """
  def _no_realizer(S:Optional[StorageSettings],dref:DRef,
                   context:Context,rarg:RealizeArg)->List[Path]:
    assert False, (
      f"Stage '{dref}' was assumed to be already realized. "
      f"Unfortunately, it seens to be not the case because it's matcher "
      f"has just instructed the core to call the realizer.\n"
      f"Context:\n{context}")
  return redefine(stage, new_realizer=_no_realizer)


