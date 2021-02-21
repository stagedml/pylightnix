from pylightnix import ( instantiate, DRef, RRef, Path, mklogdir, dirhash,
                        assert_valid_dref, assert_valid_rref, store_deps,
                        store_deepdeps, store_gc, assert_valid_hash,
                        assert_valid_config, Manager, mkcontext,
                        mkrgroup, store_rrefs, mkdref, mkrref,
                        unrref, undref, realize, rref2dref, store_config,
                        mkconfig, Build, Context, build_outpath, match_only,
                        mkdrv, store_deref, store_rref2path, store_rrefs_,
                        config_cattrs, mksymlink, store_cattrs, build_deref,
                        build_path, mkrefpath, build_config, alldrefs,
                        store_rrefs, build_wrapper, build_cattrs, build_name,
                        match_best, tryread, trywrite, match, latest, best,
                        exact, Key, match_latest, match_all, match_some,
                        match_n, realizeMany, build_outpaths, scanref_dict,
                        config_dict, promise, mklens, isrref, Config, RConfig,
                        build_setoutpaths, partial, path2rref, Tag, Group,
                        RRefGroup, concat, linkrrefs, instantiate_,
                        store_dref2path, path2dref, linkdref )

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, islink, List, randint, sleep, rmtree, system,
                           S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen, PIPE)

from tests.generators import (
    rrefs, drefs, configs, dicts )

from tests.setup import (
    ShouldHaveFailed, setup_testpath, setup_storage,
    mktestnode_nondetermenistic, mktestnode, pipe_stdout )

from pylightnix.arch import pack


def test_pack()->None:
  with setup_storage('test_pack') as p:
    def _stage(m):
      s1=mktestnode(m, {'name':'1', 'promise':[promise,'artifact']})
      s2=mktestnode(m,{'name':'2', 'maman': s1,
                       'promise':[promise,'artifact']})
      s3=mktestnode(m,{'name':'3', 'maman': s2,
                       'promise':[promise,'artifact']})
      return s3
    rref3=realize(instantiate(_stage))

    arch_path=join(p,'archive.zip')
    pack([rref3], arch_path)
    assert isfile(arch_path)

