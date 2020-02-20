REPL Demo
=========


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
    store_initialize, realize, instantiate, mapbuild )

from typing import Any

store_initialize()
```

```
Initializing existing /workspace/_pylightnix/store-v0
```





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
    build_wrapper_(mnist_realize, mapbuild(Model)))
```





```python
realize(instantiate(convnn_mnist), force_rebuild=True)
```

```
x_train shape: (60000, 28, 28, 1)
60000 train samples
10000 test samples

Epoch 00001: val_accuracy improved from -inf to 0.98317, saving model
to
/workspace/_pylightnix/tmp/200220-23:55:05:529142+0300_d20f6e78_abv8f3hc/checkpoint.ckpt
```

```
---------------------------------------------------------------------------AttributeError
Traceback (most recent call last)<ipython-input-1-cdc8dda3fa26> in
<module>
----> 1 realize(instantiate(convnn_mnist), force_rebuild=True)
~/3rdparty/pylightnix/src/pylightnix/core.py in realize(closure,
force_rebuild)
    564   """ A simplified version of
[realizeMany](#pylightnix.core.realizeMany).
    565   Expects only one result. """
--> 566   rrefs=realizeMany(closure, force_rebuild)
    567   assert len(rrefs)==1, (
    568       f"realize is to be used with single-output derivations,
but derivation "
~/3rdparty/pylightnix/src/pylightnix/core.py in realizeMany(closure,
force_rebuild)
    608     next(gen)
    609     while True:
--> 610       gen.send((None,False)) # Ask for default action
    611   except StopIteration as e:
    612     res=e.value
~/3rdparty/pylightnix/src/pylightnix/core.py in realizeSeq(closure,
force_interrupt)
    635           rrefs=drv.matcher(dref,dref_context)
    636         if rrefs is None:
--> 637           paths=drv.realizer(dref,context)
    638           rrefs_built=[store_realize(dref,context,path) for
path in paths]
    639           rrefs_matched=drv.matcher(dref,context)
~/3rdparty/pylightnix/src/pylightnix/core.py in _wrapper(dref,
context)
    373     buildtime:bool=True)->Realizer:
    374   def _wrapper(dref,context)->List[Path]:
--> 375     b=mapper(mkbuild(dref,context,buildtime)); f(b); return
list(getattr(b,'outpaths'))
    376   return _wrapper
    377
<ipython-input-1-ab2c31667718> in mnist_realize(b)
     77 def mnist_realize(b:Model):
     78   mnist_train(b)
---> 79   mnist_eval(b)
     80
     81 def convnn_mnist(m:Manager)->DRef:
<ipython-input-1-ab2c31667718> in mnist_eval(b)
     69 def mnist_eval(b:Model):
     70   o = build_outpath(b)
---> 71   b.model.load(join(o, "checkpoint.ckpt"))
     72   accuracy = b.model.evaluate(b.x_test, b.y_test, verbose =
0)[-1]
     73   print(accuracy)
AttributeError: 'Sequential' object has no attribute 'load'
```



Oh no!!!



```python
def mnist_eval_correct(b:Model):
  o = build_outpath(b)
  b.model.load_weights(join(o, "checkpoint.ckpt"))
  accuracy = b.model.evaluate(b.x_test, b.y_test, verbose = 0)[-1]
  print(accuracy)
  with open(join(o,'accuracy.txt'),'w') as f:
    f.write(str(accuracy))
```




```python
from pylightnix import repl_realize, repl_build, repl_continueBuild

repl_realize(instantiate(convnn_mnist))
```

```
<pylightnix.repl.ReplHelper at 0x7f32c0ada5f8>
```


```python
mnist_train(repl_build())
```

```
x_train shape: (60000, 28, 28, 1)
60000 train samples
10000 test samples

Epoch 00001: val_accuracy improved from -inf to 0.98225, saving model to /workspace/_pylightnix/tmp/200220-23:55:12:585081+0300_d20f6e78_917s2blt/checkpoint.ckpt
```


```python
mnist_eval_correct(repl_build())
```

```
0.9847
```


```python
repl_continueBuild()
```

```
'rref:b7148e9a0165a06414da54fd5891f28f-d20f6e78a3801f50d5df4872ca0c79b4-convnn_mnist'
```








