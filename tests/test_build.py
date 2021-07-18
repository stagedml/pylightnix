from pylightnix import (instantiate, DRef, RRef, Path, mklogdir, dirhash,
                        assert_valid_dref, assert_valid_rref, store_gc,
                        assert_valid_hash, assert_valid_config, Manager,
                        mkcontext, mkdref, mkrref, unrref, undref, realize,
                        rref2dref, drefcfg, mkconfig, Build, Context,
                        build_outpath, mkdrv, rref2path, config_cattrs,
                        build_deref, build_path, mkrefpath, build_wrapper,
                        build_cattrs, build_name, tryread, trywrite, match_only,
                        realizeMany, build_outpaths, scanref_dict, config_dict,
                        mklens, isrref, Config, partial,
                        path2rref, BuildError)

from tests.imports import ( given, Any, Callable, join, Optional, islink,
    isfile, List, randint, sleep, rmtree, system, S_IWRITE, S_IREAD, S_IEXEC,
    chmod, Popen, PIPE )

from tests.generators import (
    rrefs, drefs, configs, dicts )

from tests.setup import ( ShouldHaveFailed, setup_storage2, mkstage, mkstage )



def test_build_deref()->None:
  with setup_storage2('test_build_deref') as S:

    def _depuser(m:Manager, sources:dict)->DRef:
      def _instantiate()->Config:
        return mkconfig(sources)
      def _realize(b)->None:
        o = build_outpath(b)
        c = build_cattrs(b)
        with open(join(o,'proof_papa'),'w') as f:
          f.write(str(build_deref(b, c.papa)))
        with open(join(o,'proof_maman'),'w') as d:
          with open(build_path(b, c.maman),'r') as s:
            d.write(s.read())
        return
      return mkdrv(m, _instantiate(), match_only(), build_wrapper(_realize))

    def _setting(m:Manager)->DRef:
      n1 = mkstage(m, {'a':'1'}, lambda i:42)
      n2 = mkstage(m, {'b':'2'})
      n3 = _depuser(m, {'maman':mkrefpath(n1,['artifact']), 'papa':n2})
      return n3

    rref = realize(instantiate(_setting,S=S))
    assert_valid_rref(rref)

def test_build_cattrs()->None:
  with setup_storage2('test_build_cattrs') as S:
    def _setting(m:Manager)->DRef:
      def _instantiate()->Config:
        return mkconfig({'a':1,'b':2})
      def _realize(b)->None:
        c = build_cattrs(b)
        _ = build_outpath(b)
        assert hasattr(c,'a')
        assert hasattr(c,'b')
        assert not hasattr(c,'c')
        c.c = 'foo'
        c2 = build_cattrs(b) # Should use the cache
        assert hasattr(c2,'c')
        return
      return mkdrv(m, _instantiate(), match_only(), build_wrapper(_realize))

    rref = realize(instantiate(_setting,S=S))
    assert_valid_rref(rref)

def test_build_name()->None:
  with setup_storage2('test_build_name') as S:
    def _setting(m:Manager)->DRef:
      def _realize(b)->None:
        n=build_name(b)
        assert n=='foobar'
        _=build_outpath(b)
      return mkdrv(m, mkconfig({'name':'foobar'}), match_only(),
                   build_wrapper(_realize))
    rref=realize(instantiate(_setting,S=S))
    assert isrref(rref)
    assert 'foobar' in rref

def test_build_exception()->None:
  with setup_storage2('test_build_name') as S:
    def _setting(m:Manager)->DRef:
      def _realize(b)->None:
        raise ValueError('Oops')
      return mkdrv(m, mkconfig({}), match_only(), build_wrapper(_realize))
    clo=instantiate(_setting,S=S)
    try:
      realize(clo)
      raise ShouldHaveFailed()
    except BuildError as e:
      assert isinstance(e.exception, ValueError)
      assert e.dref==clo.dref
      assert str(e.exception)=='Oops'

