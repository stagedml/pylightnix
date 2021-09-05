from pylightnix import (instantiate, DRef, RRef, Path, mklogdir, dirhash,
                        assert_valid_dref, assert_valid_rref, store_gc,
                        assert_valid_hash, assert_valid_config, Registry,
                        mkcontext, mkdref, mkrref, unrref, undref, realize1,
                        rref2dref, drefcfg, mkconfig, Build, Context,
                        build_outpath, mkdrv, rref2path, cfgcattrs,
                        build_deref, build_path, mkrefpath, build_wrapper,
                        build_cattrs, build_name, tryread, trywrite, match_only,
                        realizeMany, build_outpaths, scanref_dict, cfgdict,
                        mklens, isrref, Config, partial,
                        path2rref, BuildError)

from tests.imports import ( given, Any, Callable, join, Optional, islink,
    isfile, List, randint, sleep, rmtree, system, S_IWRITE, S_IREAD, S_IEXEC,
    chmod, Popen, PIPE )

from tests.generators import (
    rrefs, drefs, configs, dicts )

from tests.setup import ( ShouldHaveFailed, setup_storage2, mkstage )



def test_build_deref()->None:
  with setup_storage2('test_build_deref') as S:

    def _depuser(r:Registry, sources:dict)->DRef:
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
      return mkdrv(_instantiate(), match_only(), build_wrapper(_realize), r)

    def _setting(r:Registry)->DRef:
      n1 = mkstage({'a':'1'},r,lambda i:42)
      n2 = mkstage({'b':'2'},r)
      n3 = _depuser(r, {'maman':mkrefpath(n1,['artifact']), 'papa':n2})
      return n3

    rref = realize1(instantiate(_setting,S=S))
    assert_valid_rref(rref)

def test_build_cattrs()->None:
  with setup_storage2('test_build_cattrs') as S:
    def _setting(r:Registry)->DRef:
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
      return mkdrv(_instantiate(), match_only(), build_wrapper(_realize), r)

    rref = realize1(instantiate(_setting,S=S))
    assert_valid_rref(rref)

def test_build_name()->None:
  with setup_storage2('test_build_name') as S:
    def _setting(r:Registry)->DRef:
      def _realize(b)->None:
        n=build_name(b)
        assert n=='foobar'
        _=build_outpath(b)
      return mkdrv(mkconfig({'name':'foobar'}), match_only(),
                   build_wrapper(_realize), r)
    rref=realize1(instantiate(_setting,S=S))
    assert isrref(rref)
    assert 'foobar' in rref

def test_build_exception()->None:
  with setup_storage2('test_build_name') as S:
    def _setting(r:Optional[Registry])->DRef:
      def _realize(b)->None:
        raise ValueError("An intended failure")
      return mkdrv(mkconfig({}), match_only(), build_wrapper(_realize), r)
    res:DRef
    res,clo=instantiate(_setting,S=S)
    try:
      realize1(clo)
      raise ShouldHaveFailed()
    except BuildError as e:
      assert isinstance(e.exception, ValueError)
      assert e.dref==clo.targets[0]
      assert str(e.exception)=='An intended failure'

