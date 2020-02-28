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

from pylightnix.imports import ( join, deepcopy, dirname, makedirs, isfile,
    isdir, defaultdict )
from pylightnix.core import ( mkdrv, mkconfig, mkbuild, match_only,
    assert_valid_name, build_outpath, datahash, config_dict, store_config,
    build_outpaths, match_some, assert_valid_refpath, build_paths, rref2path,
    build_deref_, build_cattrs, build_wrapper )
from pylightnix.types import ( RefPath, Manager, Config, Context, Build, Name,
    DRef, RRef, Any, Optional, Dict, Hash, Path, List )
from pylightnix.utils import ( forcelink, isrefpath, traverse_dict )


def mknode(m:Manager, sources:dict, artifacts:Dict[Name,bytes]={})->DRef:
  def _instantiate()->Config:
    d=deepcopy(sources)
    assert '__artifacts__' not in d, "config shouldn't contain reserved field '__artifacts__'"
    d.update({'__artifacts__':{an:Hash(datahash([av])) for (an,av) in artifacts.items()}})
    return mkconfig(d)
  def _realize(dref:DRef, context:Context)->List[Path]:
    b=mkbuild(dref, context)
    for an,av in artifacts.items():
      with open(join(build_outpath(b),an),'wb') as f:
        f.write(av)
    return [build_outpath(b)]
  return mkdrv(m, _instantiate(), match_only(), _realize)


def mkfile(m:Manager, name:Name, contents:bytes, filename:Optional[Name]=None)->DRef:
  filename_:Name=filename if filename is not None else name
  return mknode(m, sources={name:name}, artifacts={filename_:contents})


def checkpaths(m:Manager, promises:dict, name:str="checkpaths")->DRef:
  def _promises()->Dict[DRef,List[RefPath]]:
    refpaths:Dict[DRef,List[RefPath]]=defaultdict(list)
    def _mut(k,v):
      nonlocal refpaths
      if isrefpath(v):
        refpaths[v[0]].append(v)
      return v
    traverse_dict(promises,_mut)
    return refpaths

  def _config()->Config:
    assert len(promises.keys())>0
    d:Dict[str,Any]={'name':name}
    for dref,rpaths in _promises().items():
      for rp in rpaths:
        assert_valid_refpath(rp)
      d[str(dref)]=config_dict(store_config(dref))
    d.update(promises)
    return mkconfig(d)

  def _realize(b:Build)->None:
    c=build_cattrs(b)
    promises=_promises()
    rrefs={dref:build_deref_(b,dref) for dref in promises.keys()}
    os=build_outpaths(b, sum([len(v) for v in rrefs.values()]))
    index=0
    for dref,refpaths in promises.items():
      for rref in rrefs[dref]:
        for refpath in refpaths:
          o=os[index]
          assert refpath[0]==dref
          path=Path(join(rref2path(rref),*refpath[1:]))
          assert isdir(path) or isfile(path), \
            f"promise failed: {path} doesn't exist"
          opath=Path(join(o,*refpath[1:]))
          forcelink(path,opath)
          index+=1
  return mkdrv(m, _config(), match_some(), build_wrapper(_realize))




