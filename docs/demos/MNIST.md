MNIST Demo
==========

[Complete source of the demo](./MNIST.py)

In this document we show how
[Pylightnix](https://github.com/stagedml/pylightnix) can be used in machine
learning applications. We focus on `inplace` subset of [Pylightnix
API](https://github.com/stagedml/pylightnix/blob/master/docs/Reference.md) which
is a bit simpler than it's default functional API, at the cost of relying on an
internal global state.

We will use Pylightnix in well-known MNIST classifier application. [TensorFlow
2.0](https://www.tensorflow.org) framework is required to run this demo.

## The problem

In MNIST problem, we generally have to write an application performing image
classification. The format of input images is defined by the [MNIST
dataset](http://yann.lecun.com/exdb/mnist/). It is a set of 28x28-sized images
of handwritten digits, part of them are labaled, labels say what digit do we see
on given image. Our classifier needs to label the unlabeled part of the dataset.

To solve this problem with a Deep Learning approach, we typically write an
application which relies on certain parameters. Some of them are pre-defined (we
call them just 'parameters'), others are initially unknown to us (we call them
*Weights*). We then adjust the weights with an algorithm known as 'training',
using existing labels as an input data. This process makes the classification
work better and better. Eventually, we get a snapshot of weights which work best
for our dataset and which we hope will work well for other similar images. This
snapshot is called a *Checkpoint*. We have to save the checkpoint to use it in
the imaginary 'production' of our application.

## Implementation

Lets plan the usage of data. As one may see, we need a place to keep the
*Dataset* during training and a place to put the final *Checkpoint* when it is
ready. Also it is often a good idea to save pre-defined *Parameters* somewhere
to be able to re-produce the training if needed. Let's see how does Pylightnix
help with that.

First, let's prepare a separate storage for this demo.


```python
from shutil import rmtree
from pylightnix import store_initialize
rmtree('/tmp/pylightnix_mnist_demo', ignore_errors=True)
store_initialize(custom_store='/tmp/pylightnix_mnist_demo', custom_tmp='/tmp')
```

```
Initializing non-existing /tmp/pylightnix_mnist_demo
```



Now we are ready to code.

### Stage 1: the dataset

MNIST is a well-known dataset, it is available in many places on the Internet.
We need to pick the closest one by downloading it into `mnist.npz` file.
Pylightnix has a built-in stage called `fetchurl` for that.


```python
from pylightnix import DRef, instantiate_inplace, fetchurl

mnist_dataset:DRef = \
  instantiate_inplace(
    fetchurl,
    name='mnist',
    mode='as-is',
    url='https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz',
    sha256='731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1')

print(mnist_dataset)
```

```
dref:90531e2f6d210ae159c0100d59f50b2c-mnist
```



What we just created is a `mnist_dataset` variable of type
[DRef](./../Reference.md#pylightnix.types.DRef). It contains a reference to a
**Derivation** of `fetchurl` builtin stage. The existance of DRefs means that:

* The configuration of it's stage does exist in the storage and it doesn't
  contain critical errors.
* Pylighnix knows how to **Realize** this stage, i.e. what Python function to
  call on it and which directory to collect the output files from.


### Stage 2: the recognizer

In case of recognizer, we have no choice but to implement the stage from
scratch. In Pylightnix every stage consists of 3 parts:
[Config](./../Reference.md#pylightnix.types.Config),
[Matcher](./../Reference.md#pylightnix.types.Matcher) and
[Realizer](./../Reference.md#pylightnix.types.Realizer).

#### Config

We need some parameters to run the training. A natural place for them is the
stage configuration. The more parameters we move to configuration, the better,
because Pylightnix executes all configurations **before** all realizations. This
gives us an opportunity to check the build plan and catch some errors early,
which may become a big time-saver for long dependency chains.


```python
from pylightnix import Config, RefPath, mkconfig

def mnist_config()->Config:
  dataset:RefPath = [mnist_dataset, 'mnist.npz']
  learning_rate = 1e-3
  num_epoches = 1
  return mkconfig(locals())
```



All we need is actually to wrap some dict with a `Config` marker object, but
above we use `mkconfig` helper which makes checks on JSON-serializability and
`locals` python magic to collect local variables into a dict.

Note how do we use `mnist_dataset` reference, obtained from the previous stage.
By including it into Config, we added the **stage dependency**. Pylightnix will
scan such dependencies and call stage realizers in the appropriate order.

Note also the list form `[mnist_dataset, 'mnist.npz']`. It is a so-called
RefPath expression. Pylightnix has a helper function `build_path` which knows
how to conver RefPath into real system Path at the time of realization.

#### Matcher

Matchers allow us to deal with uncertainty when we work with non-deterministic
builders. ML training is often a non-deterministic process (for any
configuration, we could get very different results after different runs because
of e.g. true-random initialization).

Pylightnix attempts to let us live with this fact by allowing multiple
realizations for every derivation. In order to keep dependency resolution
stable, we introduce the concept of **Matcher** which is a component of every
Pylightnix derivation. Matcher match with one or more realizations (or ask the
core to produce them). The core then 'freeze' matched realizations and use them
as current derivation's representatives.

Here we don't want to go deep into the concept and just use the `match_latest`
matcher which by default picks the realization we have built last (Build-start
time is measured by a timer with platform-dependent sub-second resolution).


```python
from pylightnix import match_latest

def mnist_match():
  return match_latest()
```



#### Realizer

The third component of our Recognizer stage is `mnist_build` realizer which
does the training of our MNIST model. The brief sequence of actions is follows:

1. We ask `build_outpath` directory to put realization artifacts into.
2. We access the configuration by calling `build_cattrs` function which returns an
   object containing our config fields as attributes.
3. We also dereference our `dataset` Refpath by calling `build_path(b, c.dataset)`
4. When training is complete, we save model checkpoint into `weights.h5` file
   and the accuracy into `accuracy.txt` artifacts.


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
  accuracy = model.evaluate(x_test, y_test, verbose = 0)[-1]
  model.save_weights(join(o, 'weights.h5'), save_format='h5')
  with open(join(o,'accuracy.txt'),'w') as f:
    f.write(str(accuracy))
```



#### Putting it all together

##### Instantiate

Finally, we register our stage by calling `mkdrv` function. As before,
`instantiate` provides us with a derivation reference. This reference is a proof
that safety checkes has been completed.


```python

from pylightnix import mkdrv, build_wrapper

def model(m)->DRef:
  return mkdrv(m, mnist_config(), mnist_match(), build_wrapper(mnist_build))

mnist_model = instantiate_inplace(model)
print(mnist_model)
```

```
dref:5cd9248aabb529c207a20b8b9fc576ce-unnamed
```



##### Realize

Now we are ready to actually get our dataset (note that we didn't access the
network up to this moment) and start the training.


```python
from pylightnix import RRef, realize_inplace

mnist1:RRef = realize_inplace(mnist_model)
print(mnist1)
```

```
x_train shape: (60000, 28, 28, 1)
60000 train samples
10000 test samples
rref:5f904b93b238fdc040b15fe2abe360af-5cd9248aabb529c207a20b8b9fc576ce-unnamed
```



After some time, we get the `mnist1` value which is a realization reference. One
good property of `RRefs` is that we could always convert them into system paths.

##### Forced realize

By default, subsequent calls to `realize` will return RRef which is already
exists. But since Pylightnix supports multiple realizations, we could ask it to
produce new realizations regardless of what Matcher thinks:


```python
from pylightnix import realize_inplace

mnist2 = realize_inplace(mnist_model, force_rebuild=[mnist_model])
print(mnist2)
```

```
x_train shape: (60000, 28, 28, 1)
60000 train samples
10000 test samples
rref:6b6d7166758aa2af654d1ddb0be7514a-5cd9248aabb529c207a20b8b9fc576ce-unnamed
```



##### Best match

Now we have 2 realizations of our model, `mnist1` and `mnist2`. Lets see which
one is better. As good ML practitioners, let's just pick the model with higher
accuracy:) First, lets review the accuracies we have. Pylightnix offers simple
bash-like functions to quickly examine references, we could use them as follows:


```python
from pylightnix import lsref, catref

lsref(mnist1)
```

```
['context.json', '__buildtime__.txt', 'accuracy.txt', 'weights.h5']
```


```python
catref(mnist1,['accuracy.txt'])
```

```
['0.9853']
```


```python
catref(mnist2,['accuracy.txt'])
```

```
['0.9861']
```



We prefer
'mnist2'
because it's accuracy is slightly better. This choice could be
encoded in Pylightnix by using appropriate matcher. In our case we could use a
standard matcher called `match_best`. It takes one filename argument  and
matches with the realization, which has the biggest floating point number
stored in a file with this name.


```python
from pylightnix import match_best

def model_best(m)->DRef:
  return mkdrv(m, mnist_config(), match_best('accuracy.txt'), build_wrapper(mnist_build))

mnist_best = realize_inplace(instantiate_inplace(model_best))
```

```
Overwriting matcher or realizer of derivation dref:5cd9248aabb529c207a20b8b9fc576ce-unnamed, configured as:
{'num_epoches': 1, 'learning_rate': 0.001, 'dataset': ['dref:90531e2f6d210ae159c0100d59f50b2c-mnist', 'mnist.npz']}
```


```python
catref(mnist_best,['accuracy.txt'])
```

```
['0.9861']
```



##### Garbage collection

TODO

See `rmref`.

### Stage 3: the application


(TODO)

