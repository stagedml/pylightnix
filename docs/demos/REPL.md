REPL Demo
=========

[Complete source of this demo](./REPL.py)

This demonstration re-uses the setting of [MNIST demo](./MNIST.md). Here we show
how to use the collection of `repl_` functions to debug arbitrary stages of
Pylightnix.

Consider the chain of subsequent stages `Stage1 -> Stage2 -> Stage3 -> Stage 4`.
Pylightnix effectively caches the results of Stages 1 and 2 so if Stage 3
require debugging, we could realize `Stage2` and then manually call the
constructor of Stage3 several times to find out the problem. But if our Stage3
is a long-running job, and the problem appears near to it's end, we may face
several difficulties:
- We need to run and wait the stage to reach the problem place. We can't benefit
  from it's possible internal modularity.
- We can't use powerful tools such as IPython shell to inspect the Python
  interpreter state during the run because all the computation is done inside
  the `realize`.

To aid the situation, Pylightnix offers `repl_` version of `realize` function.
`repl_realize` is expected to be called from REPL shells like IPython or Jupyter
notebook. This new function could be programmed to return while keeping the
computation state in a special Python object waiting to be resumed or canceled.

Users may inspect the state during the pause, execute arbitrary Python functions
and finally call `repl_continue` or `repl_cancel` to either continue or cancel
the normal realization process. The whole procedure resembles the one we see in
`git rebase --continue` workflow.

At the lower level, Pylightnix programs realization interrupts which
involve triggering core's internal Python generators. The generic functions like
`realize` and `realizeMany` do hide the communication details, but the
`repl_realize` of [pylightnix.repl module](./../../src/pylightnix/repl.py) does
allow us a closer access to this machinery.


Defining MNIST stages
---------------------

We repeat the MNIST definitions explained in the MNIST demo. First, the
necessary imports and initializations.


```python
import tensorflow as tf
assert tf.version.VERSION.startswith('2.1')

from os.path import join
from numpy import load as np_load
from tensorflow.keras.models import ( Sequential )
from tensorflow.keras.layers import ( Conv2D, MaxPool2D, Dropout, Flatten, Dense )
from tensorflow.keras.utils import ( to_categorical )
from tensorflow.keras.backend import image_data_format
from tensorflow.keras.callbacks import ModelCheckpoint

from pylightnix import ( Matcher, Build, Path, RefPath, Config, Manager, RRef,
    DRef, Context, build_path, build_outpath, build_cattrs, mkdrv, rref2path,
    mkconfig, mkbuild, match_best, build_wrapper_, tryread, fetchurl,
    store_initialize, realize, instantiate )

from typing import Any

store_initialize()
```

```
Initializing existing /workspace/_pylightnix/store-v0
```



Next, we define two stages required to train the MNIST classifier. Note, how do
we split the realization into two subroutines: `mnist_train` and `mnist_eval`.
We will use them to show how to track problems.


```python

def fetchmnist(m:Manager)->DRef:
  return \
    fetchurl(m, name='mnist',
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

def convnn_mnist(m:Manager)->DRef:
  mnist = fetchmnist(m)
  return mkdrv(m, mnist_config(mnist), match_best('accuracy.txt'),
    build_wrapper_(mnist_realize, Model))
```




Debugging convnn_mnist stage
----------------------------

The last definition of `convnn_mnist` introduces our desired stage for training
the MNIST classifier. Let's try to obtain it's realization:


```python
realize(instantiate(convnn_mnist), force_rebuild=True)   # Spoiler: will fail
```

```
x_train shape: (60000, 28, 28, 1)
60000 train samples
10000 test samples

Epoch 00001: val_accuracy improved from -inf to 0.98225, saving model
to
/workspace/_pylightnix/tmp/200509-00:22:13:749127+0300_out_d20f6e78_wq2h1z_n/checkpoint.ckpt
Build wrapper of dref:d20f6e78a3801f50d5df4872ca0c79b4-convnn_mnist
raised an exception. Remaining build directories are: [{'out':
'/workspace/_pylightnix/tmp/200509-00:22:13:749127+0300_out_d20f6e78_wq2h1z_n'}]
```

```
--------------------------------------------------------------AttributeError
Traceback (most recent call last)<ipython-input-1-9b8c69999b87> in
<module>
----> 1 realize(instantiate(convnn_mnist), force_rebuild=True)   #
Spoiler: will fail
~/3rdparty/pylightnix/src/pylightnix/core.py in realize(closure,
force_rebuild, assert_realized)
    662   """ A simplified version of
[realizeMany](#pylightnix.core.realizeMany).
    663   Expects only one output path. """
--> 664   rrefs=realizeMany(closure, force_rebuild, assert_realized)
    665   assert len(rrefs)==1, (
    666       f"`realize` is to be used with single-output
derivations. Derivation "
~/3rdparty/pylightnix/src/pylightnix/core.py in realizeMany(closure,
force_rebuild, assert_realized, realize_args)
    730     next(gen)
    731     while True:
--> 732       gen.send((None,False)) # Ask for default action
    733   except StopIteration as e:
    734     res=e.value
~/3rdparty/pylightnix/src/pylightnix/core.py in realizeSeq(closure,
force_interrupt, assert_realized, realize_args)
    770             f"{store_config(dref)}"
    771             )
--> 772
gpaths:List[Dict[Tag,Path]]=drv.realizer(dref,dref_context,realize_args.get(dref,{}))
    773
rrefgs_built=[store_realize_group(dref,dref_context,g) for g in
gpaths]
    774           rrefgs_matched=drv.matcher(dref,dref_context)
~/3rdparty/pylightnix/src/pylightnix/core.py in _realizer(dref, ctx,
rarg)
    591   def _promise_aware(realizer)->Realizer:
    592     def
_realizer(dref:DRef,ctx:Context,rarg:RealizeArg)->List[Dict[Tag,Path]]:
--> 593       outgroups=realizer(dref,ctx,rarg)
    594       for key,refpath in
config_promises(store_config_(dref),dref):
    595         for g in outgroups:
~/3rdparty/pylightnix/src/pylightnix/build.py in _wrapper(dref,
context, rarg)
     65     b=ctr(mkbuildargs(dref,context,timeprefix,{},rarg));
     66     try:
---> 67       f(b);
     68       build_markstop(b) # type:ignore
     69     except:
<ipython-input-1-f38c6dead39e> in mnist_realize(b)
     77 def mnist_realize(b:Model):
     78   mnist_train(b)
---> 79   mnist_eval(b)
     80
     81 def convnn_mnist(m:Manager)->DRef:
<ipython-input-1-f38c6dead39e> in mnist_eval(b)
     69 def mnist_eval(b:Model):
     70   o = build_outpath(b)
---> 71   b.model.load(join(o, "checkpoint.ckpt"))
     72   accuracy = b.model.evaluate(b.x_test, b.y_test, verbose =
0)[-1]
     73   print(accuracy)
AttributeError: 'Sequential' object has no attribute 'load'
```



Oh no!!!

We see a backtrace saying that TensorFlow model doesn't have `load` method. It
is not very intuitive, (note that `save` method does exist), but this is what we
have. Looking through the documentation shows us that the right method to call
is `load_weights`.

We may make this trivial fix in-place but for this document I have to define
a new funtion, containing the right call.


```python
def mnist_eval_correct(b:Model):
  o = build_outpath(b)
  b.model.load_weights(join(o, "checkpoint.ckpt"))
  accuracy = b.model.evaluate(b.x_test, b.y_test, verbose = 0)[-1]
  print(accuracy)
  with open(join(o,'accuracy.txt'),'w') as f:
    f.write(str(accuracy))
```



Now, we need to re-realize the derivation, but if this is not the last problem,
than we will have to run realizations 3 or more times. In order to check
everything carefully we want to be in a position to manually run `mnist_train`
and `mnist_eval`. In Pylightnix it is possible with it's `repl` helpers.

The most straightforward wat to debug stage is to:

1. Run IPython and load above definitions into it by e.g executing
`from REPL import *`. (Jupyther Notebooks would probably also work).
2. Manually run `repl_realize` to pause the computation before the appropriate
   place.
3. Run components of the stage one-by-one.
4. Call `repl_continue` or analog to resume the computation.

In contrast to normal `realize`, `repl_realize` pauses before the last
realization. Other interrupts may be programmed by passing a list of derivations
to pause via it's `force_interrupt=[...]` argument.


```python
from pylightnix import repl_realize, repl_buildargs, repl_continueBuild

repl_realize(instantiate(convnn_mnist))
```

```
<pylightnix.repl.ReplHelper at 0x7f62d0362470>
```



We see that Pylightnix returned `ReplHelper` object. This object holds the
paused state of Pylightnix. In particular, it contains all the information
required to let user create his `Build` object (or it's subtype). This
information may be received in form of `BuildArgs` object by calling
`repl_buildargs`. Below we show how to create stage-specific build subtype named
`Model` out of it.

Note, that all repl functions normally use global `ReplHelper` if called without
arguments. Global ReplHelper is a link to the last `ReplHelper` created.

Now we could call our `mnist_train` and `mnist_eval_correct` as many times as we
want.


```python
b=Model(repl_buildargs())
mnist_train(b)
```

```
x_train shape: (60000, 28, 28, 1)
60000 train samples
10000 test samples

Epoch 00001: val_accuracy improved from -inf to 0.98408, saving model to /workspace/_pylightnix/tmp/200509-00:22:36:479601+0300_out_d20f6e78_273pbadq/checkpoint.ckpt
```


```python
mnist_eval_correct(b)
```

```
0.9845
```



When we are done (it turns out that we don't have other errors), we could call
`repl_continue` or it's simpler equivalent `repl_continueBuild` to take the
Pylightnix state out of the ReplHelper and continue it's normal execution


```python
rref=repl_continueBuild(b)
assert rref is not None
print(rref)
```

```
rref:9cc59b8551bca5f12b02f0dd56ec4321-d20f6e78a3801f50d5df4872ca0c79b4-convnn_mnist
```



`repl_continueBuild` returns `RRef` if the build process is complete and None if
it was forced to make a new interrupt. Since we programmed only one interrupt,
we now should have our realization.

As a final note, one should understand that since the REPL shell is now a part
of the realization process, the output folder may be made to contain anything
besides the products of it's realizer. Pylightnix doesn't see any difference
between repl-tweaked and normal realizations.


[Complete source of this demo](./REPL.py)



