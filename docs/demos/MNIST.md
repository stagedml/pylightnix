MNIST Demo
==========

In this document we show how
[Pylightnix](https://github.com/stagedml/pylightnix) can be used in machine
learning applications. We focus on `inplace` subset of [Pylightnix
API](https://github.com/stagedml/pylightnix/blob/master/docs/Reference.md) which
is a bit simpler than it's default functional API, at the cost of relying on an
internal global state.

In this example, we apply Pylightnix in well-known MNIST classifier application.
We will use TensorFlow for machine learning specifics.

## The problem

In MNIST classifier problem, we generally have to get a MNIST dataset which is a
set of labeled images of handwritten digits, and write some code to process
those and other similar images. The result of image processing should be a label
saying what digit do we see on given image.

To solve this problem with a Deep Learning approach, we typically write an
application which relies on certain parameters. Some of them are pre-defined (we
call them just 'parameters'), others are initially unknown to us (we call them
*Weights*). We then adjust the weights in a process known as 'training', which
makes the classification work better and better. As a result, we get a snapshot
of weights which works best for our dataset and which we hope works well for
other similar images. Such a snapshot is often called a *Checkpoint*. We have to
save this checkpoint and use it in the 'production' of our application.

## Implementation

Lets plan the usage of data. As one may see, we need a place to keep the
*Dataset* during training and a place to put the final *Checkpoint* when it is
ready. Also it is often a good idea to save pre-defined *Parameters* somewhere
to be able to re-produce the training if needed. Let's see how does Pylightnix
help with that.


```python
from shutil import rmtree
from pylightnix import store_initialize
rmtree('/tmp/pylightnix_mnist_demo', ignore_errors=True)
store_initialize(custom_store='/tmp/pylightnix_mnist_demo', custom_tmp='/tmp')
```



### Stage 1: the dataset

The MNIST dataset is well-known and is available in many places on the Internet.
We




```python
from pylightnix import DRef, instantiate_inplace, fetchurl

mnist_dataset:DRef = \
  instantiate_inplace(
    fetchurl,
    name='mnist',
    mode='as-is',
    url='https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz',
    sha256='731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1')
```



### Stage 2: the recognizer

#### Stage configuration


```python
from pylightnix import Config, mkconfig

def mnist_config()->Config:
  dataset = [mnist_dataset, 'mnist.npz']
  learning_rate = 1e-3
  num_epoches = 1
  return mkconfig(locals())
```



#### Stage realization


```python
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
  accuracy = model.evaluate(x_test, y_test, verbose = 0)
  model.save_weights(join(o, 'weights.h5'), save_format='h5')
  with open(join(o,'accuracy.txt'),'w') as f:
    f.write(str(accuracy))
```



#### Stage matching


```python
from pylightnix import mkdrv, only, realize_inplace, build_wrapper

def mnist_match(dref, context):
  return only(dref, context)

def model(m)->DRef:
  return mkdrv(m, mnist_config, mnist_match, build_wrapper(mnist_build))

mnist_model = instantiate_inplace(model)
```



#### Putting it all together


```python

mnist = realize_inplace(mnist_model, force_rebuild=[mnist_model])
print(mnist)
```

```
x_train shape: (60000, 28, 28, 1)
60000 train samples
10000 test samples
rref:92f2e92f70f16a5eec5ecb86f25a9f76-ccbfe731c63564f99661e240c043aab0-unnamed
```



### Stage 3: the application


(TODO)

