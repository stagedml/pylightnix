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
from pylightnix import Path, initialize, dirrm
dirrm(Path('/tmp/pylightnix_mnist_demo'))
initialize(custom_store='/tmp/pylightnix_mnist_demo', custom_tmp='/tmp')
```

```
Initializing non-existing /tmp/pylightnix_mnist_demo
```



Now we are ready to code.

### Stage 1: the dataset

MNIST is a well-known dataset, it is available in many places on the Internet.
We pick the closest one by downloading it into `mnist.npz` file.
Pylightnix has a built-in stage called `fetchurl` for that. Every stage has to
be `instantiated` and than `realized`.


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



By the above instructions we initialized is a `mnist_dataset` variable of type
[DRef](./../Reference.md#pylightnix.types.DRef). It contains a reference to a
**Derivation** of `fetchurl` builtin stage. The existance of DRefs means that:

* Configuration object does exist in the storage and it doesn't
  contain critical errors.
* Pylighnix knows how to **Realize** the stage, i.e. what Python function to
  call on it and which directory to collect the output files from.
* We could pass this link to subsequent stages to form dependencies or to
  `realize` to request the realization.

Since the MNIST dataset by itself has no practical meaning for us, we move on to
defining the second stage.

### Stage 2: the recognizer

In case of recognizer, we have no choice but to implement the stage from
scratch. In Pylightnix every stage includes of 3 important components:
[Config](./../Reference.md#pylightnix.types.Config),
[Matcher](./../Reference.md#pylightnix.types.Matcher) and
[Realizer](./../Reference.md#pylightnix.types.Realizer).

#### Config

Config is a natural place to include parameters required for training.  The more
parameters we could move to configuration, the better, because Pylightnix
executes all configurations during instantiation, that is **before** all
realizations. Thus we have an opportunity to check the build plan and catch
some errors early, which may become a big time-saver.


```python
from pylightnix import Config, RefPath, PromisePath, mkconfig, promise

def mnist_config()->Config:
  learning_rate = 1e-3
  num_epoches = 1
  dataset:RefPath = [mnist_dataset, 'mnist.npz']
  accuracy:PromisePath = [promise, 'accuracy.txt']
  return mkconfig(locals())
```



In the above code we actually wrap a certain python dictionary with a `Config`
marker object by calling `mkconfig` helper on the result of `locals` python
builtin magic function. `locals` collects local variables and `mkconfig` makes
some checks, including the check on JSON-serializability.

Some fileds of the configuration have a special meaning for Pylightnix:

* Note how do we use `mnist_dataset` reference, obtained from the previous
  stage.  We have added the **stage dependency**, just by including it into
  Config.  Pylightnix will handle dependencies and call stage realizers in the
  appropriate order.
* Note the list `[mnist_dataset, 'mnist.npz']`. It is a so-called **RefPath**
  expression. Pylightnix has a helper function `build_path` which translates
  lists of this kind into real system Paths at the time of realization.
* Accuracy attribute encodes a so called PromisePath. PromisePaths refer to
  not-yet-existing files or folders which we promise will be created by the
  current stage. PromisePaths may be converted by the same `build_path` function
  into writable system paths.

#### Matcher

Matchers allow us to deal with uncertainty when we work with non-deterministic
builders. ML training is often a non-deterministic process, because for any
configuration, we could get very different results. While we may attempt to fix
results by carefully setting random seeds, there are other factors which could
lead to uncertainty, like non-deterministic compilers or cluster/multithreading
issues.

Pylightnix tries to let us live with this fact by allowing multiple realizations
for every derivation. In order to keep dependency resolution stable in this
circumstances, we introduce the concept of **Matchers**. Matchers match with one
or more realizations (or ask the core to produce them) using user-defined
criteria. After the matching, The core 'freezes' it's results and use them as
current derivation's representation during dependency resolution.

Here we wouldn't go deep into the concept and just use the builtin `match_latest`
matcher which by default picks the latest realization we have built (Build-start
time is measured by a timer with platform-dependent sub-second resolution).


```python
from pylightnix import match_latest

def mnist_match():
  return match_latest()
```



#### Realizer

The third component of our Recognizer stage is `mnist_build` realizer defines
how to create new realizations if we need them. It's brief sequence of actions is
as follows:

1. We ask the core of `build_outpath` directory to put realization artifacts
   into.
2. We access the configuration parameters by calling `build_cattrs` function
   which returns an object containing config fields as attributes.
3. We dereference our `dataset` Refpath into system paths by calling
   `build_path(b, c.dataset)`
4. We start the training. When it is complete, we save the model
   checkpoint into `weights.h5` file and the accuracy into `accuracy.txt`
   artifacts.


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
  with open(build_path(b,c.accuracy),'w') as f:
    f.write(str(accuracy))
```



#### Putting it all together

##### Instantiate

Finally, we have to register our stage by calling `mkdrv` function. As before,
`instantiate` provides us with a derivation reference. This reference is a proof
that safety checks has been completed and a ticket to the `realize` action.


```python

from pylightnix import mkdrv, build_wrapper

def model(m)->DRef:
  return mkdrv(m, mnist_config(), mnist_match(), build_wrapper(mnist_build))

mnist_model = instantiate_inplace(model)
print(mnist_model)
```

```
dref:62bf4c470bd346d4b4431438958999eb-unnamed
```



##### Realize

Now we are ready to actually get our dataset  and start the training. (note that
we didn't access the network up to this moment).


```python
from pylightnix import RRef, realize_inplace

mnist1:RRef = realize_inplace(mnist_model)
print(mnist1)
```

```
x_train shape: (60000, 28, 28, 1)
60000 train samples
10000 test samples
rref:20ee736e35338c37a5f31da758e13a8c-62bf4c470bd346d4b4431438958999eb-unnamed
```



After some time, we get the `mnist1` value which is a **Realization reference**. One
good property of `RRefs` is the possibility to convert them into system paths.

##### Forced realize

By default, subsequent calls to `realize` will return the RRef of already
existing realization. But Pylightnix do supports multiple realizations, so we
could ask it to produce new realizations regardless of what Matcher thinks:


```python
from pylightnix import realize_inplace

mnist2 = realize_inplace(mnist_model, force_rebuild=[mnist_model])
print(mnist2)
```

```
x_train shape: (60000, 28, 28, 1)
60000 train samples
10000 test samples
rref:0d2c64e632b76b37f0c2604079b6e668-62bf4c470bd346d4b4431438958999eb-unnamed
```



Note, that if new realization turns out to be identical to the one which does
already exist, they will be merged into a single realization.

##### Best match

In our case MNIST training is (intentionally) non-deterministic, so we have 2
different realizations, called `mnist1` and `mnist2`. Lets see which one is
better. As every brave ML practitioner would do, we want to pick the model with
best accuracy. First, lets review the accuracies that we have. Pylightnix offers
simple bash-like functions for that:


```python
from pylightnix import lsref, catref

lsref(mnist1)
```

```
['context.json',
 '__buildtime__.txt',
 'accuracy.txt',
 'group.txt',
 '__buildstop__.txt',
 'weights.h5',
 'tag.txt']
```


```python
catref(mnist1,['accuracy.txt'])
```

```
['0.983']
```


```python
catref(mnist2,['accuracy.txt'])
```

```
['0.9846']
```



We prefer
'mnist2'
because it's accuracy is slightly better. This algorithm of choice could be
encoded with Pylightnix by using more appropriate builtin matcher. In our case
we stick with `match_best`. It takes one filename argument  and matches with the
realization, which has the biggest floating point number stored in a file with
this name.


```python
from pylightnix import match_best

def model_best(m)->DRef:
  return mkdrv(m, mnist_config(), match_best('accuracy.txt'), build_wrapper(mnist_build))

mnist_best = realize_inplace(instantiate_inplace(model_best))
```

```
Overwriting either the matcher or the realizer of 'dref:62bf4c470bd346d4b4431438958999eb-unnamed'. RConfig:
Config({'accuracy': ['__promise__', 'accuracy.txt'], 'dataset': ['dref:90531e2f6d210ae159c0100d59f50b2c-mnist', 'mnist.npz'], 'num_epoches': 1, 'learning_rate': 0.001})
```


```python
catref(mnist_best,['accuracy.txt'])
```

```
['0.9846']
```



In Python shells like IPython, we could also call `shellref(..)` function in
order to open the Linux shell and inspect the contents of corresponding storage
folders with standard command-line tools.

##### Garbage collection

TODO

See `rmref`.

### Stage 3: the application


(TODO)

