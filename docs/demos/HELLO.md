GNU Hello demo
==============

[Complete source of the demo](./HELLO.py)

Pylightnix is a library for manipulating immutable data objects. It provides
core API for checking, creating and querying such objects using files and
folders as a data sotrage. One kind of applications which could benefit from
this API is package managers.

Task
----

Here we illustrate basic concepts by designing a toy build script for compiling
and running [GNU hello](https://www.gnu.org/software/hello) program. Note, that
this script will miss an important feature of package managers, namely build
isolation, which is out of the Pylightnix' scope.

GNU Hello is a demo application which prints 'Hello world!' on its standard
output. It's purpose is to demonstrate the usage of Automake tools. We will see
how Pylighnix could help us to solve this quest. We assume that the host system
provides an access to the GNU Automake toolchain, that is, Autoconf, Automake,
gcc, etc.

We go through the following plan of actions:

1. Define a rule for downloading GNU Hello sources, using builtin `fetchurl`
   stage.
2. Define a custom rule for compiling GNU Hello from sources.
3. Interact with the storage.

Implementation
--------------

Pylightnix offers functions which form a kind of domain-specific language,
embedded in Python language. Our program is a Python script, which could be
executed by a common `python3` interpreter. In this demo we will need certain
standard Python functions. Later we will import Pylightnix functions as needed.


```python
from os.path import join
from os import system, chdir, getcwd
from shutil import copytree
from tempfile import TemporaryDirectory
from typing import Any
from subprocess import Popen, PIPE
```



First things first, Pylightnix uses filesystem storage for tracking immutable
data object (or stages) which could depend on each other. This storage is
global, it is the central part of library. In order to check or create it, we
call `store_initialize`:


```python
from shutil import rmtree
from pylightnix import store_initialize
rmtree('/tmp/pylightnix_hello_demo', ignore_errors=True) # Optional
store_initialize(custom_store='/tmp/pylightnix_hello_demo', custom_tmp='/tmp')
```

```
Initializing non-existing /tmp/pylightnix_hello_demo
```



Location of the storage is kept in an internal global variable and normally
shouldn't be changed during the work, but since Pylightnix doesnt run any
background services, it is totally up ot you. Read the [store_initialize
docstring reference](../Reference.md#pylightnix.core.store_initialize) for
details.

Note that in most applications we don't really need to initialize a separate
storage, but could safely use the default one. To check or initialize default
storage, just call `store_initialize()` without arguments.

### Basic terms

Pylightnix allows us to define, check and execute data processing operations
called **stages**. We will define a custom stage later, for now we use a
builtin stage `fetchurl` (which is an analog of `fetchurl` expression of Nix
package manager).


```python
from pylightnix import DRef, instantiate_inplace, fetchurl

hello_version = '2.10'

hello_src:DRef = \
  instantiate_inplace(
    fetchurl,
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b')
```



By this definition we created `hello_src` variable of type
[DRef](../Reference.md#pylightnix.types.DRef) which holds a reference to a
**Derivation** of fetchurl stage.

Having a derivation reference means several things:

* (a) Configuration of the corresponding stage has passed certain checks and
  does exist in the storage as a JSON object.
* (b) Pylighnix knows how to **Realize** this stage, i.e. it has a Python function
  to produce some data (files) to put them in storage.

For [fetchurl](../Reference.md#pylightnix.stages.fetchurl.fetchurl), the
output data will contain the contents of URL, after downloading and
unpacking. In this case, we expect to see `hello-2.10` folder, containing the
hello's sources. Let's check it:


```python
from pylightnix import RRef, realize_inplace

hello_rref:RRef = realize_inplace(hello_src)
print(hello_rref)
```

```
Unpacking /tmp/200216-15:06:05:292405+0300_2f56e6f9_c3uz3v2t/hello-2.10.tar.gz..
Removing /tmp/200216-15:06:05:292405+0300_2f56e6f9_c3uz3v2t/hello-2.10.tar.gz..
rref:3fce7614ca738e68d6ad5b8a2057c488-2f56e6f987a1da0271915894ca19e28f-hello-src
```



OK, now we should see the signs of actual work being done. Something was just
downloaded and we also see a string starting with 'rref:...' in _stdout_.  This
string is a **Realization reference** of type
[RRef](../Reference.md#pylightnix.types.RRef), it uniquely identifies some
data in the Pylightnix filesystem storage.

Any RRef could be converted to system by calling
[rref2path](../Reference.md#pylightnix.core.rref2path) function:


```python
from pylightnix import rref2path

print(rref2path(hello_rref))
```

```
/tmp/pylightnix_hello_demo/2f56e6f987a1da0271915894ca19e28f-hello-
src/3fce7614ca738e68d6ad5b8a2057c488
```



Also, Pylightnix offers a shell-like helper functions to quickly examine the
content of references. One of them is `lsref`:


```python
from pylightnix import lsref

print(lsref(hello_rref))
```

```
['context.json', '__buildtime__.txt', 'hello-2.10']
```



### Custom stages

We want to build the GNU hello, so we need some code to do this job. Pylighnix
aims at providing only a generic minimalistic API, so it doesn't have a builtin
stage for compiling applications. Luckily, it is not hard to define it, as we
should see.

All Pylighnix stages consist of three important components:

* The configuration, which is a JSON-Object of parameters and references
* The matcher, which is a Python function for dealing with non-determenistic builds.
* The realizer, which is a Python function encoding the actual build process

The matcher business is beyond the scope of this tutorial. We will use trivial
`match_only` matcher which asks the core to build the stage and then returns
build result.


#### Configuration

Let's deal with other two components. We start by defining a configuration:


```python
from pylightnix import Config, mkconfig

def hello_config()->Config:
  name = 'hello-bin'
  src = [hello_src, f'hello-{hello_version}']
  return mkconfig(locals())
```



Here, we specify a name and a
[RefPath](../Reference.md#pylightnix.types.RefPath) which links our new stage
with some realization of the previous stage. We will access files of
our dependencies by dereferencing RefPaths, as we will see soon.

As a side note, `locals()` is a Python builtin function which returns a `dict`
of current function's local variables.

_Note, we should only use **Derivation references** in configurations.
Realization references are accessible either from global scope or from
realize functions_

#### Realization

Let's now move to the realization part of our Hello builder stage:


```python
from pylightnix import ( Path, Build, build_cattrs, build_outpath, build_path, dirchmod )

def hello_realize(b:Build)->None:
  c:Any = build_cattrs(b)
  o:Path = build_outpath(b)
  with TemporaryDirectory() as tmp:
    copytree(build_path(b,c.src),join(tmp,'src'))
    dirchmod(join(tmp,'src'),'rw')
    cwd = getcwd()
    try:
      chdir(join(tmp,'src'))
      system(f'./configure --prefix=/usr')
      system(f'make')
      system(f'make install DESTDIR={o}')
    finally:
      chdir(cwd)
```



As we may see here, `hello_realize` function accepts a
[Build](../Reference.md#pylightnix.types.Build) helper object. It brings to us
two important variables:
* `c:ConfigAttrs` is a copy of configuration that we defined earlier. It has
  `name` and `src` attributes that could be accessed with Python dot-operator.
  Note, that there is a `build_config` function which returns current
  stage's config as-is, i.e. as a Python dictionary.
* `o:Path` is the name of **output folder** where we should save the results of
  our build process.

Another interesting thing is the call to `build_path` function. It is the point
where we **Dereference refpaths** by converting them into system paths.
Pylightnix guarantees that referenced stages are already realized at the time of
dereferencing.

The rest is simple. We copy sources to the temp folder and perform the usual
configure-make-install on it.

#### Running the stage

Finally, we introduce our new stage to Pylightnix:


```python
from pylightnix import mkdrv, build_wrapper, match_only

hello:DRef = \
  instantiate_inplace(mkdrv, hello_config(), match_only(), build_wrapper(hello_realize))

print(hello)
```

```
dref:53ccb94819ad4c9f55acb61460ec97ed-hello-bin
```



In this instantiation, [mkdrv](../Reference.md#pylightnix.core.mkdrv) (which
stands for 'make derivation') plays the role of `fetchurl` from the previous
stage. As before, we first get a `DRef`, which means that basic checks were
passed, and then call `realize`:


```python
rref:RRef=realize_inplace(hello)
print(rref)
```

```
rref:eb14eaa937ffa45013f1a4c5ea525a53-53ccb94819ad4c9f55acb61460ec97ed-hello-bin
```



Now we could convert RRef to the system path and run the GNU Hello binary.


```python

hello_bin=join(rref2path(rref),'usr/bin/hello')
print(Popen([hello_bin], stdout=PIPE, shell=True).stdout.read())
```

```
b'Hello, world!\n'
```




