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

# from pylightnix.types import (Any, DRef, Stage, Manager, Derivation, List,
#                               RRef, Closure, SPath, TypeVar, Callable, Optional,
#                               Dict, RealizeArg, Context, Union, Tuple)
# from pylightnix.core import (instantiateM, realize, realizeCtx)
# from pylightnix.utils import (scanref_dict)


#: The Global [Derivation manager](#pylightnix.types.Manager) used by
#: `instantiate_inplace` and `realize_inplace` functions of this module.
# PYLIGHTNIX_MANAGER = Manager(None)


# def instantiate_inplace(stage:Callable[[Manager,Any,Any],Any],
#                         *args:Any,
#                         m:Optional[Manager]=None,
#                         **kwargs:Any)->Closure:
#   """ Instantiate a `stage`, use `PYLIGHTNIX_MANAGER` for storing derivations.
#   Return derivation reference of the top-level stage. """
#   global PYLIGHTNIX_MANAGER
#   m=m if m is not None else PYLIGHTNIX_MANAGER
#   return instantiateM(m, stage)

# def realizeAll_inplace(result:Any,
#                        force_rebuild:List[DRef]=[],
#                        assert_realized:List[DRef]=[],
#                        realize_args:Dict[DRef,RealizeArg]={}
#                        )->Tuple[Any,Context]:
#   """ Realize the derivation pointed by `dref` by constructing it's
#   [Closure](#pylightnix.types.Closure) based on the contents of the global
#   dependency manager and [realizing](#pylightnix.core.realizeMany) this closure.
#   """
#   global PYLIGHTNIX_MANAGER
#   drefs,_=scanref_dict({'foo':result})
#   clo=Closure(result,drefs,list(PYLIGHTNIX_MANAGER.builders.values()),
#               S=PYLIGHTNIX_MANAGER.S)
#   return realizeCtx(clo,force_rebuild,assert_realized,realize_args)


# def realize_inplace(dref:DRef,
#                     force_rebuild:List[DRef]=[],
#                     assert_realized:List[DRef]=[],
#                     realize_args:Dict[DRef,RealizeArg]={})->RRef:
#   _,ctx=realizeAll_inplace([dref], force_rebuild, assert_realized,
#                            realize_args)
#   assert len(ctx[dref])==1
#   return ctx[dref][0]


