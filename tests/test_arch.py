from pylightnix import (instantiate, DRef, RRef, Path, mklogdir, dirhash,
                        assert_valid_dref, assert_valid_rref, drefdeps1,
                        drefdeps, assert_valid_hash, assert_valid_config,
                        Manager, mkcontext, mkdref, mkrref, unrref, undref,
                        realize, rref2dref, mkconfig, Build, Context,
                        build_outpath, mkdrv, rref2path, alldrefs,
                        selfref, allrrefs, realizeMany)

from tests.imports import (given, Any, Callable, join, Optional, islink,
                           isfile, islink, List, randint, sleep, rmtree,
                           system, S_IWRITE, S_IREAD, S_IEXEC, chmod, Popen,
                           PIPE, settings, reproduce_failure, Phase, note)

from tests.generators import (
    rrefs, drefs, configs, dicts, rootstages )

from tests.setup import ( ShouldHaveFailed, setup_storage2, mkstage, mkstage,
                         pipe_stdout )

from pylightnix.arch import (pack,unpack)




def test_pack1()->None:
  with setup_storage2('test_pack1') as S:
    def _stage(m):
      s1=mkstage(m, {'name':'n1',
                     'promise':[selfref,'artifact']})
      s2=mkstage(m, {'name':'n2',
                     'maman':s1,
                     'promise':[selfref,'artifact']})
      s3=mkstage(m, {'name':'n3',
                     'papa':s2,
                     'promise':[selfref,'artifact']})
      return s3

    rref3=realize(instantiate(_stage,S=S))
    print('===================')
    print(list(allrrefs(S)))
    print('===================')
    arch_path=Path(join(S.tmpdir,'archive.zip'))
    pack([rref3], arch_path, S=S)
    unpack(arch_path, S=S)
    assert isfile(arch_path)


# # @reproduce_failure('5.30.0', b'AAAAAAA=')
# # @reproduce_failure('5.30.0', b'AAEBAAAAAAAAAA==')
# # @reproduce_failure('5.30.0', b'AXicJUwJDsAwCOJw7f7/4oGLBCMCrwBKpAURWeEfhkWDnSNODtcKFyEMZ+XhfSod6ibGZjdnueaWCFuaVF8fMEIAwQ==')
# # @reproduce_failure('5.30.0', b'AXicFYlJDgAxDMIw1rTH/v+3k4hFAr+TxDLNTfkiYPbBVsK4GTl7sShdMMkPENwAbg==')
# @reproduce_failure('4.41.0', b'AAAAAA==')
# @reproduce_failure('4.41.0', b'AA4NApYAAwADAgEBBAMFBgIAAQA=')
# @reproduce_failure('4.41.0', b'AAAAAA==')
@settings(max_examples=10, phases=[Phase.generate])
@given(stages=rootstages())
def test_pack2(stages)->None:
  archives=[]
  with setup_storage2('test_pack_src') as S1:
    for nstage,stage in enumerate(stages):
      rrefs=realizeMany(instantiate(stage,S=S1))
      for nrref,rref in enumerate(rrefs):
        ap=Path(join(S1.tmpdir,f'archive_{nstage:02d}_{nrref:02d}.zip'))
        note(f'Packing {ap}:{rref}')
        pack([rref], ap, S=S1)
        archives.append(ap)

  note('PACK done')

  with setup_storage2('test_pack_dst') as S2:
    for ap in archives:
      note(f'Unpacking {ap}')
      unpack(Path(ap), S=S2)

  assert set(alldrefs(S=S1)) == set(alldrefs(S=S2))
  assert set(allrrefs(S=S1)) == set(allrrefs(S=S2))
  note('OK!')

