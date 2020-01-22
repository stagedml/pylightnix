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
from pylightnix import fetchurl, instantiate_inplace

mnist_dataset = instantiate_inplace(
    fetchurl,
    name='mnist',
    url='https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz',
    sha256='731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1')

```

```python
from pylightnix import Config, mkconfig

def mnist_config()->Config:
  dataset = mnist_dataset
  learning_rate = 1e-5
  return mkconfig(locals())
```

```python
from pylightnix import DRef, Context, Path, mkdtemp, join

def mnist_build(dref:DRef, context:Context)->Path:
  o=Path(mkdtemp(dir='/tmp'))
  with open(join(o,'accuracy'),'w') as f:
    f.write('0.99')
  # TODO: implement MNIST classifier here
  return o

```

```python
from pylightnix import mkdrv, only, realize_inplace

def mnist_match(dref, context):
  return only(dref, context)

def model(m)->DRef:
  return mkdrv(m, mnist_config, mnist_match, mnist_build)

mnist_model = instantiate_inplace(model)
```



```python

mnist = realize_inplace(mnist_model)

```

