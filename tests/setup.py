from pylightnix import ( Path, store_initialize )
from tests.imports import ( rmtree, join, makedirs, listdir,)

PYLIGHTNIX_TEST:str='/tmp/pylightnix_tests'

def setup_storage(tn:str)->str:
  import pylightnix.core
  storepath=f'/tmp/{tn}'
  rmtree(storepath, onerror=lambda a,b,c:())
  pylightnix.core.PYLIGHTNIX_STORE=storepath
  pylightnix.core.PYLIGHTNIX_TMP='/tmp'
  store_initialize(exist_ok=False)
  assert 0==len(listdir(storepath))
  return storepath

def setup_testpath(name:str)->Path:
  testpath=join(PYLIGHTNIX_TEST, name)
  rmtree(testpath, onerror=lambda a,b,c:())
  makedirs(testpath, exist_ok=False)
  return Path(testpath)

