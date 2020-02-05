from pylightnix.imports import ( join, deepcopy )
from pylightnix.core import ( mkdrv, mkconfig, mkbuild, match_only,
    assert_valid_name, build_outpath, datahash )
from pylightnix.types import ( Manager, Config, Context, Build, Name, DRef,
    RRef, Any, Optional, Dict, Hash, Path, List )


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
  return mkdrv(m, _instantiate, match_only(), _realize)


def mkfile(m:Manager, name:Name, contents:bytes, filename:Optional[Name]=None)->DRef:
  filename_:Name=filename if filename is not None else name
  return mknode(m, sources={name:name}, artifacts={filename_:contents})

