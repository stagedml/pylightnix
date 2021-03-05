from pylightnix import ( instantiate, DRef, RRef, Path, mklogdir, dirhash,
                        assert_valid_dref, assert_valid_rref, store_deps,
                        store_deepdeps, store_gc, assert_valid_hash,
                        assert_valid_config, Manager, mkcontext, mkrgroup,
                        store_rrefs, mkdref, mkrref, unrref, undref, realize,
                        rref2dref, store_config, mkconfig, Build, Context,
                        build_outpath, match_only, mkdrv, store_deref,
                        store_rref2path, store_rrefs_, config_cattrs,
                        mksymlink, store_cattrs, build_deref, build_path,
                        mkrefpath, build_config, alldrefs, store_rrefs,
                        build_wrapper, build_cattrs, build_name, match_best,
                        tryread, trywrite, match, latest, best, exact, Key,
                        match_latest, match_all, match_some, match_n,
                        realizeMany, build_outpaths, scanref_dict, config_dict,
                        promise, mklens, isrref, Config, RConfig,
                        build_setoutpaths, partial, path2rref, Tag, Group,
                        RRefGroup, concat, linkrrefs, instantiate_,
                        store_dref2path, path2dref, linkdref, realizeGroups,
                        groups2rrefs, allrrefs )

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, islink, List, randint, sleep, rmtree,
                           system, S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen,
                           PIPE, settings, reproduce_failure, Phase)

from tests.generators import (
    rrefs, drefs, configs, dicts, rootstages )

from tests.setup import ( ShouldHaveFailed, setup_storage2, mkstage, mkstage,
                         pipe_stdout )

from pylightnix.arch import (pack,unpack)


from time import sleep

from pdb import set_trace

def test_pack1()->None:
  with setup_storage2('test_pack1') as (T,S):
    def _stage(m):
      s1=mkstage(m, {'name':'1', 'promise':[promise,'artifact']})
      s2=mkstage(m,{'name':'2', 'maman': s1,
                       'promise':[promise,'artifact']})
      s3=mkstage(m,{'name':'3', 'papa': s2,
                       'promise':[promise,'artifact']})
      return s3

    rref3=realize(instantiate(_stage,S=S))
    arch_path=Path(join(T,'archive.zip'))
    pack([rref3], arch_path, S=S)
    unpack(arch_path, S=S)
    assert isfile(arch_path)


# @reproduce_failure('5.30.0', b'AAAAAAA=')
# @reproduce_failure('5.30.0', b'AAEBAAAAAAAAAA==')
# @reproduce_failure('5.30.0', b'AXicJUwJDsAwCOJw7f7/4oGLBCMCrwBKpAURWeEfhkWDnSNODtcKFyEMZ+XhfSod6ibGZjdnueaWCFuaVF8fMEIAwQ==')
# @reproduce_failure('5.30.0', b'AXicFYlJDgAxDMIw1rTH/v+3k4hFAr+TxDLNTfkiYPbBVsK4GTl7sShdMMkPENwAbg==')
@settings(max_examples=10, print_blob=True, deadline=None, phases=[Phase.generate])
@given(stages=rootstages())
def test_pack2(stages)->None:
  archives=[]
  with setup_storage2('test_pack_src') as (T1,S1):
    for nstage,stage in enumerate(stages):
      rgs=realizeGroups(instantiate(stage,S=S1))
      for ngroup,rg in enumerate(rgs):
        ap=Path(join(T1,f'archive_{nstage:02d}_{ngroup:02d}.zip'))
        print(f'Packing {ap}')
        pack(groups2rrefs([rg]), ap, S=S1)
        archives.append(ap)

  print('PACK done')
  # set_trace()

  with setup_storage2('test_pack_dst') as (T2,S2):
    for ap in archives:
      print(f'Unpacking {ap}')
      unpack(Path(ap), S=S2)

  assert set(alldrefs(S=S1)) == set(alldrefs(S=S2))
  assert set(allrrefs(S=S1)) == set(allrrefs(S=S2))
  print('OK!')

