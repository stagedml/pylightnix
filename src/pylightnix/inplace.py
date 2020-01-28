from pylightnix.types import ( Any, DRef, Stage, Manager, Derivation, List, RRef, Closure )
from pylightnix.core import ( instantiate_, realize )


#: Global Derivation manager used for Inplace mode of operation
PYLIGHTNIX_MANAGER = Manager()


def instantiate_inplace(stage:Any, *args, **kwargs)->DRef:
  global PYLIGHTNIX_MANAGER
  closure = instantiate_(PYLIGHTNIX_MANAGER,
                         lambda m: stage(m, *args, **kwargs)
                         )
  return closure.dref


def realize_inplace(dref:DRef, force_rebuild:List[DRef]=[]) -> RRef:
  global PYLIGHTNIX_MANAGER
  return realize(Closure(dref,list(PYLIGHTNIX_MANAGER.builders.values())),
                 force_rebuild=force_rebuild)

