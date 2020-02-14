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


def realize_inplace(dref:DRef, force_rebuild:List[DRef]=[])->RRef:
  global PYLIGHTNIX_MANAGER
  return realize(Closure(dref,list(PYLIGHTNIX_MANAGER.builders.values())),
                 force_rebuild=force_rebuild)

