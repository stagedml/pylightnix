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

""" This module defines inplace variants of `instantiate` and `realize`
functions. Inplace functions store closures in their own global dependency
resolution [Manager](#pylightnix.types.Manager) and thus offer a simpler API,
but add usual risks of using gloabl variables. """

from pylightnix.types import ( Any, DRef, Stage, Manager, Derivation, List,
    RRef, Closure )
from pylightnix.core import ( instantiate_, realize )


#: The Global [Derivation manager](#pylightnix.types.Manager) used by
#: `instantiate_inplace` and `realize_inplace` functions of this module.
PYLIGHTNIX_MANAGER = Manager()


def instantiate_inplace(stage:Any, *args, **kwargs)->DRef:
  """ Instantiate a `stage`, use `PYLIGHTNIX_MANAGER` for storing derivations.
  Return derivation reference of the top-level stage. """
  global PYLIGHTNIX_MANAGER
  closure = instantiate_(PYLIGHTNIX_MANAGER,
                         lambda m: stage(m, *args, **kwargs)
                         )
  return closure.dref


def realize_inplace(dref:DRef, force_rebuild:List[DRef]=[])->RRef:
  """ Realize the derivation pointed by `dref` by constructing it's
  [Closure](#pylightnix.types.Closure) based on the contents of the global
  dependency manager and [realizing](#pylightnix.core.realizeMany) this closure.
  """
  global PYLIGHTNIX_MANAGER
  return realize(Closure(dref,list(PYLIGHTNIX_MANAGER.builders.values())),
                 force_rebuild=force_rebuild)

