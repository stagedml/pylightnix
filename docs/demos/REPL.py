
import tensorflow as tf
assert tf.version.VERSION.startswith('2.1')

from os.path import join
from numpy import load as np_load
from tensorflow.keras.models import ( Sequential )
from tensorflow.keras.layers import ( Conv2D, MaxPool2D, Dropout, Flatten, Dense )
from tensorflow.keras.utils import ( to_categorical )
from tensorflow.keras.backend import image_data_format
from tensorflow.keras.callbacks import ModelCheckpoint

from pylightnix import ( Matcher, Build, Path, RefPath, Config, Registry, RRef,
    DRef, Context, build_path, build_outpath, build_cattrs, mkdrv, rref2path,
    mkconfig, mkbuild, match_best, build_wrapper_, tryread, fetchurl,
    initialize, realize1, instantiate )

from typing import Any

initialize()


def fetchmnist(r:Registry)->DRef:
  return \
    fetchurl(r, name='mnist',
                mode='as-is',
                url='https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz',
                sha256='731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1')

class Model(Build):
  model:Sequential
  x_train:Any
  y_train:Any
  x_test:Any
  y_test:Any

def mnist_config(mnist:DRef)->Config:
  name = 'convnn_mnist'
  dataset:RefPath = [mnist, 'mnist.npz']
  learning_rate = 1e-3
  num_epoches = 1
  version = 7
  return mkconfig(locals())

def mnist_train(b:Model)->None:
  o = build_outpath(b)
  c = build_cattrs(b)

  with np_load(build_path(b, c.dataset), allow_pickle=True) as f:
    b.x_train, b.y_train = f['x_train'], f['y_train']
    b.x_test, b.y_test = f['x_test'], f['y_test']

  b.x_train = b.x_train.reshape(b.x_train.shape[0], 28, 28, 1).astype('float32') / 255
  b.y_train = to_categorical(b.y_train, 10)

  b.x_test = b.x_test.reshape(b.x_test.shape[0], 28, 28, 1).astype('float32') / 255
  b.y_test = to_categorical(b.y_test, 10)


  print('x_train shape:', b.x_train.shape)
  print(b.x_train.shape[0], 'train samples')
  print(b.x_test.shape[0], 'test samples')

  model = Sequential()
  b.model = model
  model.add(Conv2D(32, kernel_size=(3, 3), activation = 'relu', input_shape = (28,28,1)))
  model.add(Conv2D(64, (3, 3), activation = 'relu'))
  model.add(MaxPool2D(pool_size = (2,2)))
  model.add(Dropout(0.25))
  model.add(Flatten())
  model.add(Dense(128, activation = 'relu'))
  model.add(Dropout(0.5))
  model.add(Dense(10, activation = 'softmax'))

  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

  callbacks = [
    ModelCheckpoint(
      monitor='val_accuracy',
      filepath=join(o, "checkpoint.ckpt"),
      save_weights_only=True,
      save_best_only=True,
      verbose=True)]
  model.fit(b.x_train, b.y_train,
      batch_size=32,
      epochs=c.num_epoches,
      verbose=0,
      callbacks=callbacks,
      validation_split=0.2)

def mnist_eval(b:Model):
  o = build_outpath(b)
  b.model.load(join(o, "checkpoint.ckpt"))
  accuracy = b.model.evaluate(b.x_test, b.y_test, verbose = 0)[-1]
  print(accuracy)
  with open(join(o,'accuracy.txt'),'w') as f:
    f.write(str(accuracy))

def mnist_realize(b:Model):
  mnist_train(b)
  mnist_eval(b)

def convnn_mnist(r:Registry)->DRef:
  mnist = fetchmnist(r)
  return mkdrv(r, mnist_config(mnist), match_best('accuracy.txt'),
    build_wrapper_(mnist_realize, Model))

realize1(instantiate(convnn_mnist), force_rebuild=True)   # Spoiler: will fail

def mnist_eval_correct(b:Model):
  o = build_outpath(b)
  b.model.load_weights(join(o, "checkpoint.ckpt"))
  accuracy = b.model.evaluate(b.x_test, b.y_test, verbose = 0)[-1]
  print(accuracy)
  with open(join(o,'accuracy.txt'),'w') as f:
    f.write(str(accuracy))

from pylightnix import repl_realize, repl_buildargs, repl_continueBuild

repl_realize(instantiate(convnn_mnist))

b=Model(repl_buildargs())
mnist_train(b)
mnist_eval_correct(b)

rref=repl_continueBuild(b)
assert rref is not None
print(rref)
