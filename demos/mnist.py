from pylightnix import fetchurl, instantiate_inplace

mnist_dataset = instantiate_inplace(
    fetchurl,
    name='mnist',
    url='https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz',
    sha256='731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1')


from pylightnix import Config, mkconfig

def mnist_config()->Config:
  dataset = mnist_dataset
  learning_rate = 1e-5
  return mkconfig(locals())

from pylightnix import DRef, Context, Path, mkdtemp, join, PYLIGHTNIX_TMP

def mnist_build(dref:DRef, context:Context)->Path:
  o=Path(mkdtemp(dir=PYLIGHTNIX_TMP))
  with open(join(o,'accuracy'),'w') as f:
    f.write('0.99')
  return o

from pylightnix import mkdrv, only, realize_inplace

def mnist_match(dref, context):
  return only(dref, context)

def model(m)->DRef:
  return mkdrv(m, mnist_config, mnist_match, mnist_build)

mnist_model = instantiate_inplace(model)

mnist = realize_inplace(mnist_model)

