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

""" Simple functions imitating unix shell tools.  """

from pylightnix import (DRef, RRef, Path, Build, Registry, mklens, mkdrv,
                        selfref, match_some, build_wrapper, instantiate,
                        realize1, isrref, isdref, build_cattrs, build_outpath,
                        build_path, mkconfig, assert_valid_rref, isrefpath,
                        isclosure, match_only)

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, List, randint, sleep, rmtree, system,
                           S_IWRITE, S_IREAD, S_IEXEC, isdir, note)

from tests.generators import (rrefs, drefs, configs, dicts)

from tests.setup import (ShouldHaveFailed, setup_storage2, mkstage)




def test_lens():
  with setup_storage2('test_lens') as S:
    def _setting(r:Registry)->DRef:
      n1=mkstage({'name':'1', 'selfref':[selfref,'artifact']},r)
      n2=mkstage({'name':'2', 'selfref':[selfref,'artifact'],
                        'dict':{'d1':1} },r)

      def _realize(b:Build):
        o=build_outpath(b)
        c=build_cattrs(b)
        assert isrefpath(mklens(b).maman.selfref.refpath)
        assert isfile(mklens(b).papa.selfref.syspath)
        assert o in mklens(b).selfref.syspath
        assert o == mklens(b).syspath
        assert mklens(b).papa.name.val == '2'
        assert mklens(b).papa.dref == c.papa

        with open(mklens(b).selfref.syspath,'w') as f:
          f.write('chickenpoop')

      return mkdrv(
        mkconfig({'name':'3', 'maman':n1, 'papa':n2,
                  'selfref':[selfref,'artifact'],
                  }),
                 matcher=match_only(),
                 realizer=build_wrapper(_realize), r=r)

    _,clo=instantiate(_setting, S=S)
    assert isrefpath(mklens(clo.targets[0],S=S).maman.selfref.refpath)
    assert isdir(mklens(clo.targets[0],S=S).syspath)
    rref=realize1(clo)
    assert_valid_rref(rref)
    assert isrefpath(mklens(rref,S=S).maman.selfref.refpath)
    assert isfile(mklens(rref,S=S).maman.selfref.syspath)
    assert mklens(rref,S=S).rref == rref
    assert isrefpath(mklens(rref,S=S).papa.selfref.refpath)
    assert mklens(rref,S=S).papa.dict.d1.val == 1
    assert mklens(rref,S=S).dref == clo.targets[0]
    assert isdir(mklens(rref,S=S).syspath)

    try:
      print(mklens(clo.targets[0],S=S).maman.selfref.syspath)
      raise ShouldHaveFailed()
    except AssertionError:
      pass

    try:
      print(mklens(rref,S=S).papa.dict.d1.get('xxx'))
      raise ShouldHaveFailed()
    except AssertionError:
      pass

    try:
      print(mklens(rref,S=S).papa.dict.d1.syspath)
      raise ShouldHaveFailed()
    except AssertionError:
      pass

    try:
      mklens(rref,S=S).papa.dict.d1.val=42 # can't mutate rref
      raise ShouldHaveFailed()
    except AssertionError:
      pass

    d={'foo':'foo','bar':'bar'}
    mklens(d,S=S).foo.val='zzz'
    assert d['foo']=='zzz'
    try:
      mklens(d,S=S).x.val=42 # can't set new values
      raise ShouldHaveFailed()
    except AssertionError:
      pass
    mklens(d).bar.val+='33'
    assert d['bar']=='bar33'


def test_lens_closures():
  with setup_storage2('test_lens_closures') as S:
    def _stage(r:Registry)->DRef:
      n1=mkstage({'name':'1', 'x':33, 'selfref':[selfref,'artifact']},r)
      n2=mkstage({'name':'2', 'papa':n1, 'dict':{'d1':1} },r)
      n3=mkstage({'name':'3', 'maman':n2 },r)
      return n3

    _,clo=instantiate(_stage, S=S)
    assert isclosure(clo)
    print(f"{clo.targets}")

    rref=realize1(mklens(clo,S=S).maman.papa.closure)
    assert mklens(rref,S=S).x.val==33
    assert open(mklens(rref,S=S).selfref.syspath).read()=='0'

