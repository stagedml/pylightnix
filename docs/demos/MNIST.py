
from pylightnix import Path, initialize, dirrm
dirrm(Path('/tmp/pylightnix_mnist_demo'))
initialize(custom_store='/tmp/pylightnix_mnist_demo', custom_tmp='/tmp')

from pylightnix import DRef, instantiate_inplace, fetchurl

mnist_dataset:DRef = \
  instantiate_inplace(
    fetchurl,
    name='mnist',
    mode='as-is',
    url='https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz',
    sha256='731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1')

print(mnist_dataset)

from pylightnix import Config, RefPath, PromisePath, mkconfig, promise

def mnist_config()->Config:
  learning_rate = 1e-3
  num_epoches = 1
  dataset:RefPath = [mnist_dataset, 'mnist.npz']
  accuracy:PromisePath = [promise, 'accuracy.txt']
  return mkconfig(locals())

from pylightnix import match_latest

def mnist_match():
  return match_latest()

from pylightnix import ( Build, build_outpath, build_cattrs, build_path )
from os.path import join
from numpy import load
from tensorflow.keras.models import ( Sequential )
from tensorflow.keras.layers import ( Conv2D, MaxPool2D, Dropout, Flatten, Dense )
from tensorflow.keras.utils import ( to_categorical )
from tensorflow.keras.backend import image_data_format


def mnist_build(b:Build)->None:
  o = build_outpath(b)
  c = build_cattrs(b)

  with load(build_path(b, c.dataset), allow_pickle=True) as f:
    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']

  x_train = x_train.reshape(x_train.shape[0], 28, 28, 1).astype('float32') / 255
  y_train = to_categorical(y_train, 10)

  x_test = x_test.reshape(x_test.shape[0], 28, 28, 1).astype('float32') / 255
  y_test = to_categorical(y_test, 10)


  print('x_train shape:', x_train.shape)
  print(x_train.shape[0], 'train samples')
  print(x_test.shape[0], 'test samples')

  model = Sequential()
  model.add(Conv2D(32, kernel_size=(3, 3), activation = 'relu', input_shape = (28,28,1)))
  model.add(Conv2D(64, (3, 3), activation = 'relu'))
  model.add(MaxPool2D(pool_size = (2,2)))
  model.add(Dropout(0.25))
  model.add(Flatten())
  model.add(Dense(128, activation = 'relu'))
  model.add(Dropout(0.5))
  model.add(Dense(10, activation = 'softmax'))

  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics = ['accuracy'])
  model.fit(x_train, y_train, batch_size = 32, epochs = c.num_epoches, verbose = 0)
  accuracy = model.evaluate(x_test, y_test, verbose = 0)[-1]
  model.save_weights(join(o, 'weights.h5'), save_format='h5')
  with open(build_path(b,c.accuracy),'w') as f:
    f.write(str(accuracy))


from pylightnix import mkdrv, build_wrapper

def model(m)->DRef:
  return mkdrv(m, mnist_config(), mnist_match(), build_wrapper(mnist_build))

mnist_model = instantiate_inplace(model)
print(mnist_model)

from pylightnix import RRef, realize_inplace

mnist1:RRef = realize_inplace(mnist_model)
print(mnist1)

from pylightnix import realize_inplace

mnist2 = realize_inplace(mnist_model, force_rebuild=[mnist_model])
print(mnist2)

from pylightnix import lsref, catref

lsref(mnist1)
catref(mnist1,['accuracy.txt'])
catref(mnist2,['accuracy.txt'])

from pylightnix import match_best

def model_best(m)->DRef:
  return mkdrv(m, mnist_config(), match_best('accuracy.txt'), build_wrapper(mnist_build))

mnist_best = realize_inplace(instantiate_inplace(model_best))

catref(mnist_best,['accuracy.txt'])
