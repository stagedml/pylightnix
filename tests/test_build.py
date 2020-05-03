from pylightnix import ( instantiate, DRef, RRef, Path, mklogdir, dirhash,
    assert_valid_dref, assert_valid_rref, store_deps, store_deepdeps, store_gc,
    assert_valid_hash, assert_valid_config, Manager, mkcontext, store_rrefs,
    mkdref, mkrref, unrref, undref, realize, rref2dref, store_config, mkconfig,
    Build, Context, build_outpath, match_only, mkdrv, store_deref, rref2path,
    store_rrefs_, config_cattrs, mksymlink, store_cattrs, build_deref,
    build_path, mkrefpath, build_config, store_drefs, store_rrefs, store_rrefs_,
    build_wrapper, recursion_manager, build_cattrs, build_name, match_best,
    tryread, trywrite, assert_recursion_manager_empty, match, latest, best,
    exact, Key, match_latest, match_all, match_some, match_n, realizeMany,
    build_outpaths, scanref_dict, config_dict, promise, mklens, isrref, Config,
    RConfig, build_setoutpaths, partial, path2rref )

from tests.imports import ( given, Any, Callable, join, Optional, islink,
    isfile, List, randint, sleep, rmtree, system, S_IWRITE, S_IREAD, S_IEXEC,
    chmod, Popen, PIPE )

from tests.generators import (
    rrefs, drefs, configs, dicts )

from tests.setup import (
    ShouldHaveFailed, setup_testpath, setup_storage, mktestnode_nondetermenistic, mktestnode )



def test_build_deref()->None:
  with setup_storage('test_build_deref'):

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
      n1 = mktestnode_nondetermenistic(m, {'a':'1'}, lambda : 42)
      n2 = mktestnode(m, {'b':'2'})
      n3 = _depuser(m, {'maman':mkrefpath(n1,['artifact']), 'papa':n2})
      return n3

    rref = realize(instantiate(_setting))
    assert_valid_rref(rref)

def test_build_cattrs()->None:
  with setup_storage('test_build_cattrs'):
    def _setting(m:Manager)->DRef:
      def _instantiate()->Config:
        return mkconfig({'a':1,'b':2})
      def _realize(b)->None:
        c = build_cattrs(b)
        o = build_outpath(b)
        assert hasattr(c,'a')
        assert hasattr(c,'b')
        assert not hasattr(c,'c')
        c.c = 'foo'
        c2 = build_cattrs(b) # Should use the cache
        assert hasattr(c2,'c')
        return
      return mkdrv(m, _instantiate(), match_only(), build_wrapper(_realize))

    rref = realize(instantiate(_setting))
    assert_valid_rref(rref)

def test_build_name()->None:
  with setup_storage('test_build_name'):
    def _setting(m:Manager)->DRef:
      def _realize(b)->None:
        n=build_name(b)
        assert n=='foobar'
        o=build_outpath(b)
      return mkdrv(m, mkconfig({'name':'foobar'}), match_only(), build_wrapper(_realize))
    rref=realize(instantiate(_setting))
    assert isrref(rref)
    assert 'foobar' in rref

def test_build_exception()->None:
  with setup_storage('test_build_name'):
    def _setting(m:Manager)->DRef:
      def _realize(b)->None:
        raise ValueError('Oops')
      return mkdrv(m, mkconfig({}), match_only(), build_wrapper(_realize))
    try:
      rref=realize(instantiate(_setting))
      raise ShouldHaveFailed()
    except ValueError as e:
      assert 'Oops' in str(e)

