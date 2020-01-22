from pylightnix.types import ( Any, DRef, Stage, Manager, Derivation, List, RRef, Closure )
from pylightnix.core import ( instantiate_, realize )


PYLIGHTNIX_MANAGER = Manager()


def instantiate_inplace(stage:Any, *args, **kwargs)->DRef:
  global PYLIGHTNIX_MANAGER
  closure = instantiate_(lambda m: stage(m, *args, **kwargs),
                          PYLIGHTNIX_MANAGER)
  return closure.dref


def realize_inplace(dref:DRef) -> RRef:
  global PYLIGHTNIX_MANAGER
  return realize(Closure(dref,list(PYLIGHTNIX_MANAGER.builders.values())))

