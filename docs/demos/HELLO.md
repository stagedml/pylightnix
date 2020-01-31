GNU Hello demo
==============

[Complete source of the demo](./HELLO.py)


```python
from os.path import join
from os import system, chdir, getcwd
from shutil import copytree
from tempfile import TemporaryDirectory
from typing import Any
from subprocess import Popen, PIPE
```



Pylightnix provides API for data deployment system right in your Python
application. Here we illustrate the concepts using [GNU
hello](https://www.gnu.org/software/hello) building problem as an example.

First things first, we should know that Pylightnix uses filesystem storage for
tracking immutable data object called nodes which could depend on each other.
This storage is the central part of library, all the magic happens there. So
let's initialize it:


```python
from shutil import rmtree
from pylightnix import store_initialize
rmtree('/tmp/pylightnix_hello_demo', ignore_errors=True)
store_initialize(custom_store='/tmp/pylightnix_hello_demo', custom_tmp='/tmp')
```



Location of the storage is kept in an internal global variable. It may be
changed either by passing arguments to this function or by other methods. Check
the [store_initialize docstring
reference](../Reference.md#pylightnix.core.store_initialize) for details.

Note that in real application we don't really need to initialize a separate
store, but could safely use the default one. To check that it does exist, just
call `store_initialize()` without arguments.

### Basic terms and builtins

In Pylightnix, we define, check and execute the data processing operations
called **stages**. We will define our stage later, for now we will use a
builtin stage `fetchurl` (hello, Nix).


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



What did we do? We created `hello_src` variable of type
[DRef](../Reference.md#pylightnix.types.DRef) which takes a reference to a
**Derivation** of fetchurl stage. It means several things: a) the configuration
of hello-stc stage does already exist in the storage and it doesn't contain
critical errors like invalid links. b) Pylighnix knows how to **Realize** this
stage, i.e. what Python function to call on it and which directory to
collect the output files from.

So what will we have when Realization of `hello_src` is complete? As [fetchurl's
comment](../Reference.md#pylightnix.stages.fetchurl.fetchurl)
suggests, we will see a downloaded and unpacked URL, in our case it is the
contents of `hello-2.10.tar.gz` archive. Let's check it:


```python
from pylightnix import RRef, realize_inplace

hello_rref:RRef = realize_inplace(hello_src)
print(hello_rref)
```

```
Unpacking /tmp/0128-19:51:57+0300_2f56e6f9_h46y60rb/hello-2.10.tar.gz..
Removing /tmp/0128-19:51:57+0300_2f56e6f9_h46y60rb/hello-2.10.tar.gz..
rref:3fce7614ca738e68d6ad5b8a2057c488-2f56e6f987a1da0271915894ca19e28f-hello-src
```



OK, now we should see the signs of actual work being done. Something was just
downloaded and we also see a string starting with 'rref:...' in _stdout_.  This
string is a **Realization reference** of type
[RRef](../Reference.md#pylightnix.types.RRef), it uniquely identifies some
data node in the Pylightnix storage.

### Custom stages

We want to build the GNU hello, so we need some code to do the job. Pylighnix
aims at providing only a generic minimalistic API, so it doesn't have a builtin
stage for compiling applications. Luckily, it is not hard to define it, as we
should see.

In Pylighnix, stages consist of three important components:
* The configuration, which is a JSON-Object of parameters and references
* The realizer, which is a Python function encoding the actual build process
* The matcher, which is another Python function for dealing with
    non-determenistic builds.

The matcher business is beyond the scope of this quick start. For now, we just
require only one realization, so let's deal with other two components. Firs, the
configuration:


```python
from pylightnix import Config, mkconfig

def hello_config()->Config:
  name = 'hello-bin'
  src = [hello_src, f'hello-{hello_version}']
  return mkconfig(locals())
```



Here, we define a name and a
[RefPath](../Reference.md#pylightnix.types.RefPath) which links our new stage
with a specific folder of the previous stage. We will access configurations of
our dependencies by dereferencing this RefPath, as we will see soon.

As a side note, `locals()` is a Python builtin which returns a `dict` of current
function's local variables, so as a result we will have a config with two
fields.

_Note, we should only use **Derivation references** in configurations.
Realization references become accessible either from global scope or from
realize functions_

So let's move to the realization of our Hello builder:


```python
from pylightnix import Path, Build, build_cattrs, build_outpath, build_path

def hello_realize(b:Build)->None:
  c:Any = build_cattrs(b)
  o:Path = build_outpath(b)
  with TemporaryDirectory() as tmp:
    copytree(build_path(b,c.src),join(tmp,'src'))
    cwd = getcwd()
    try:
      chdir(join(tmp,'src'))
      system(f'./configure --prefix=/usr')
      system(f'make')
      system(f'make install DESTDIR={o}')
    finally:
      chdir(cwd)
```



As we may see here, `hello_realize` function takes a
[Build](../Reference.md#pylightnix.types.Build) helper, which brings us two
important variables:
* `c:ConfigAttrs` is de-facto a config we defined earlier,
  with `name` and `src` attributes (there is also a `build_config` function
  which returns current stage's config as-is, i.e. as a Python dict).
* `o:Path` is the name of **output folder** where we should save the results of
  our build process.

Another interesting thing is the `build_path` function. It is the point
where we **Dereference refpaths** by converting them to system paths. Pylightnix
guarantees that referenced stages are already realized at the time of
dereferencing.

The rest is simple. We copy sources to the temp folder and perform the usual
configure-make-install on it.

Finally, we introduce our new stage to Pylightnix:


```python
from pylightnix import mkdrv, build_wrapper, only

hello:DRef = \
  instantiate_inplace(mkdrv, hello_config, only(), build_wrapper(hello_realize))

print(hello)
```

```
dref:53ccb94819ad4c9f55acb61460ec97ed-hello-bin
```



In this instantiation, [mkdrv](../Reference.md#pylightnix.core.mkdrv) (which
stands for 'make derivation') takes the place of `fetchurl`. As before, we get a
`DRef` and that means we now could do:


```python
rref:RRef=realize_inplace(hello)
print(rref)
```

```
rref:702d63a0ba2d69c4ae816fe7d8586a2a-53ccb94819ad4c9f55acb61460ec97ed-hello-bin
```



Once the realization is ready, we are free to [convert it to system
path](../Reference.md#pylightnix.core.rref2path) and do whatever we want:


```python
from pylightnix import rref2path

hello_bin=join(rref2path(rref),'usr/bin/hello')
print(Popen([hello_bin], stdout=PIPE, shell=True).stdout.read())
```

```
b'Hello, world!\n'
```


