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

from pylightnix import (instantiate, DRef, RRef, Path, Build, Manager, mklens,
                        mkdrv, promise, match_only, build_wrapper, instantiate,
                        realize, isrref, isdref, store_cattrs, build_cattrs,
                        build_outpath, build_path, mkconfig, assert_valid_rref,
                        isrefpath, isclosure)

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, List, randint, sleep, rmtree, system,
                           S_IWRITE, S_IREAD, S_IEXEC, isdir)

from tests.generators import (rrefs, drefs, configs, dicts)

from tests.setup import (ShouldHaveFailed, setup_testpath, setup_storage,
                         mkstage)




def test_lens():
  with setup_storage('test_lens'):
    def _setting(m:Manager)->DRef:
      n1=mkstage(m, {'name':'1', 'promise':[promise,'artifact']})
      n2=mkstage(m, {'name':'2', 'promise':[promise,'artifact'],
                        'dict':{'d1':1} })

      def _realize(b:Build):
        o=build_outpath(b)
        c=build_cattrs(b)
        assert isrefpath(mklens(b).maman.promise.refpath)
        assert isfile(mklens(b).papa.promise.syspath)
        assert o in mklens(b).promise.syspath
        assert o == mklens(b).syspath
        assert mklens(b).papa.name.val == '2'
        assert mklens(b).papa.dref == c.papa

        with open(mklens(b).promise.syspath,'w') as f:
          f.write('chickenpoop')

      return mkdrv(m,
        mkconfig({'name':'3', 'maman':n1, 'papa':n2,
                  'promise':[promise,'artifact'],
                  }),
                 matcher=match_only(),
                 realizer=build_wrapper(_realize))

    clo=instantiate(_setting)
    assert isrefpath(mklens(clo.dref).maman.promise.refpath)
    assert isdir(mklens(clo.dref).syspath)
    rref=realize(clo)
    assert_valid_rref(rref)
    assert isrefpath(mklens(rref).maman.promise.refpath)
    assert isfile(mklens(rref).maman.promise.syspath)
    assert mklens(rref).rref == rref
    assert isrefpath(mklens(rref).papa.promise.refpath)
    assert mklens(rref).papa.dict.d1.val == 1
    assert mklens(rref).dref == clo.dref
    assert isdir(mklens(rref).syspath)

    try:
      print(mklens(clo.dref).maman.promise.syspath)
      raise ShouldHaveFailed()
    except AssertionError:
      pass

    try:
      print(mklens(rref).papa.dict.d1.get('xxx'))
      raise ShouldHaveFailed()
    except AssertionError:
      pass

    try:
      print(mklens(rref).papa.dict.d1.syspath)
      raise ShouldHaveFailed()
    except AssertionError:
      pass

    try:
      mklens(rref).papa.dict.d1.val=42 # can't mutate rref
      raise ShouldHaveFailed()
    except AssertionError:
      pass

    d={'foo':'foo','bar':'bar'}
    mklens(d).foo.val='zzz'
    assert d['foo']=='zzz'
    try:
      mklens(d).x.val=42 # can't set new values
      raise ShouldHaveFailed()
    except AssertionError:
      pass
    mklens(d).bar.val+='33'
    assert d['bar']=='bar33'


def test_lens_closures():
  with setup_storage('test_lens_closures'):
    def _setting(m:Manager)->DRef:
      n1=mkstage(m, {'name':'1', 'x':33, 'promise':[promise,'artifact']})
      n2=mkstage(m, {'name':'2', 'papa':n1, 'dict':{'d1':1} })
      n3=mkstage(m, {'name':'3', 'maman':n2 })
      return n3

    clo=instantiate(_setting)
    assert isclosure(clo)

    rref=realize(mklens(clo).maman.papa.closure)
    assert mklens(rref).x.val==33
    assert open(mklens(rref).promise.syspath).read()=='0'

