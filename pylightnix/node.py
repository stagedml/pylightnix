from pylightnix.core import Ref, Config, Model, model_save, only, state, search

def mknode(d:dict)->Ref:
  """ Create a trivial store node consisiting only of a config `d`, with no
  artifacts """
  c=Config(d)
  refs=search(state(c))
  if len(refs)>0:
    return only(refs)
  else:
    return model_save(Model(c))

