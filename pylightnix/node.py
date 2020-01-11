from pylightnix.core import Ref, Config, Model, model_save, state, search

def mknode(d:dict)->Ref:
  """ Create a trivial store node consisiting only of a config `d`, with no
  artifacts """
  c=Config(d)
  refs=search(state(c))
  if len(refs)==0:
    return model_save(Model(c))
  elif len(refs)==1:
    return refs[0]
  else:
    assert False, f"mknode: multiple results ({refs})"

