-   [GNU Hello demo](#gnu-hello-demo)
    -   [The task](#the-task)
    -   [Implementation](#implementation)
        -   [Fetchurl and Unpack stages](#fetchurl-and-unpack-stages)
        -   [A custom compile stage](#a-custom-compile-stage)
        -   [Accessing the results](#accessing-the-results)

GNU Hello demo
==============

[Complete source of the demo](./HELLO.py)

Pylightnix is a library for manipulating immutable data objects. It
provides core API for checking, creating and querying such objects using
files and folders as a data sotrage. One kind of applications which
could benefit from this API is package managers.

The task
--------

We illustrate the basic concepts by designing a toy package manager able
to compile and run the [GNU hello](https://www.gnu.org/software/hello)
program.

GNU Hello is a demo application which prints ‘Hello world!’ on its
standard output. It’s purpose is to demonstrate the usage of Automake
tools. We will see how Pylighnix could help us to solve this quest. We
assume that the host system provides an access to the GNU Automake
toolchain, that is, paths to Autoconf, Automake, gcc, etc should present
in system PATH variable.

We go through the following plan of actions:

1.  Use built-in rules to download and unpack the GNU Hello sources.
2.  Define a custom rule for compiling the GNU Hello from sources.
3.  Run the application by querying the Pylightnix artifact storage.

Implementation
--------------

Pylightnix offers functions which form a kind of domain-specific
language, embedded in Python language. Our program is a Python script,
which could be executed by a common `python3` interpreter. In this demo
we will need certain standard Python functions. Later we will import
Pylightnix functions as needed.

``` python
from os.path import join
from os import system, chdir, getcwd
from shutil import copytree
from tempfile import TemporaryDirectory
from typing import Any
from subprocess import Popen, PIPE
```

First things first, Pylightnix uses filesystem for tracking immutable
data objects which could depend on each other. Objects reside partly in
the filesystem, partly in memory as a Python objects. We initialize the
filesystem part by calling
[fsinit](../Reference.md#pylightnix.core.fsinit) on
[StorageSettings](../Reference.md#pylightnix.types.StorageSettings) and
then create the global
[Registry](../Reference.md#pylightnix.types.Registry). The Registry and
the part of filesystem described by StorageSettings are the only mutable
objects that we will operate on.

``` python
from os import environ
from pylightnix import Registry, StorageSettings, mkSS, fsinit

S:StorageSettings=mkSS('/tmp/pylightnix_hello_demo')
fsinit(S,remove_existing=True)
M=Registry(S)

hello_version = '2.10'
```

### Fetchurl and Unpack stages

Pylightnix manages data processing operations called Derivations. The
toolbox provides a generic constructor
[mkdrv](../Reference.md#pylightnix.core.mkdrv) and a set of pre-defined
**Stages** which wraps it with problem-specific parameters.

In this tutorial we will need
[fetchurl2](../Reference.md#pylightnix.stages.fetch2.fetchurl2) and
[unpack](../Reference.md#pylightnix.stages.fetch2.unpack) stages. The
first one knows how to download URLs from the Internet, the second one
knows how to unpack archives. We import both functions, along with other
Pylightnix APIs.

``` python
from pylightnix import (Registry, DRef, RRef, fetchurl2, unpack, mklens, selfref)
```

Our first goal is to make derivations ready for realization by
registering them in the Registry `M`. We call `fetchurl2` with the
appropriate parameters and get an unique
[DRef](../Reference.md#pylightnix.types.DRef) reference back. Every
`DRef` value proofs to us that the Registry is aware of our new
derivation.

``` python
tarball:DRef = fetchurl2(
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b',
    out=[selfref, f'hello-{hello_version}.tar.gz'], m=M)
```

In order to link derivations into a chain we should put the derivation
reference of a prerequisite derivation somewhere into the config of a
child derivaiton.

``` python
hello_src:DRef = unpack(
    name='unpack-hello',
    refpath=mklens(tarball,m=M).out.refpath,
    aunpack_args=['-q'],
    src=[selfref, f'hello-{hello_version}'],m=M)
```

The `selfref` path is our promise to Pylightnix that the said path would
appear after the derivation is realized. Pylightnix checks such promises
and raises in case they are not fulfilled.

Now we are done with registrations and going to obtain our objects. We
call [instantiate](../Reference.md#pylightnix.core.instantiate) to
compute the dependency closure of the target object and pass it to
[realize1](../Reference.md#pylightnix.core.realize1) which runs the
show. As a result, we obtain a reference of another kind
[RRef](../Reference.md#pylightnix.types.RRef)

``` python
from pylightnix import instantiate, realize1
hello_rref:RRef = realize1(instantiate(hello_src, m=M))
print(hello_rref)
```

``` stdout
rref:29eaa2c8e74cbc939dfdd8e43f3987eb-43323fae07b9e30f65ed0a1b6213b6f0-unpack-hello
```

``` stderr
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
 80  708k   80  572k    0     0   546k      0  0:00:01  0:00:01 --:--:--  545k
100  708k  100  708k    0     0   631k      0  0:00:01  0:00:01 --:--:--  631k
hello-2.10.tar.gz: extracted to `hello-2.10'
```

RRefs could be converted to system paths by calling an
[mklens](../Reference.md#pylightnix.lens.mklens) the swiss-army-knife
data accessor of Pylightnix:

``` python
from pylightnix import current_storage

with current_storage(S):
  print(mklens(hello_rref).val)
  print(mklens(hello_rref).syspath)
  print(mklens(hello_rref).src.syspath)
```

``` stdout
rref:29eaa2c8e74cbc939dfdd8e43f3987eb-43323fae07b9e30f65ed0a1b6213b6f0-unpack-hello
/tmp/pylightnix_hello_demo/store-v0/43323fae07b9e30f65ed0a1b6213b6f0-unpack-hello/29eaa2c8e74cbc939dfdd8e43f3987eb
/tmp/pylightnix_hello_demo/store-v0/43323fae07b9e30f65ed0a1b6213b6f0-unpack-hello/29eaa2c8e74cbc939dfdd8e43f3987eb/hello-2.10
```

Pylightnix offers a number of other shell-like helper functions for
accessing realization, like `lsref`:

``` python
from pylightnix import lsref, catref

print(lsref(hello_rref, S))
```

``` stdout
['__buildstop__.txt', '__buildstart__.txt', 'hello-2.10', 'context.json']
```

### A custom compile stage

In this section we define a custom stage to build the newly obtained
sources of GNU Hello application.

Defining Pylighnix stages requires us to provide Pylightnix with the
following components:

-   The JSON-like configuration object.
-   The matcher Python function, dealing with non-determenistic builds.
-   The realizer Python function which specifies the actual build
    process.

The matcher business is beyond the scope of this tutorial. We will use a
trivial `match_only` matcher which instructs Pylightnix to expect no
more than one realization of a stage in its storage.

We produce a `Config` object by reading local variables of a helper
function `hello_config`. We could have just call `mkconfig` on a dict.

``` python
from pylightnix import Config, mkconfig, mklens, selfref

def hello_config()->Config:
  name = 'hello-bin'
  src = mklens(hello_src,m=M).src.refpath
  out_hello = [selfref, 'usr', 'bin', 'hello']
  out_log = [selfref, 'build.log']
  return mkconfig(locals())
```

To specify Realizer we write another Python function which accepts the
`Build` context. We use `mklens` to query the parameters of the
derivation being built just as we used it for querying parameters of
completed realizations. The `selfref` paths is initialized to paths
inside the build temporary folder where we must put the build artifacts.
Here we produce the GNU hello binary and a build log as a side-product.

``` python
from pylightnix import (Path, Build, build_cattrs, build_outpath, build_path,
                        dirrw )

def hello_realize(b:Build)->None:
  with TemporaryDirectory() as tmp:
    copytree(mklens(b).src.syspath,join(tmp,'src'))
    dirrw(Path(join(tmp,'src')))
    cwd = getcwd()
    try:
      chdir(join(tmp,'src'))
      system(f'( ./configure --prefix=/usr && '
             f'  make &&'
             f'  make install DESTDIR={mklens(b).syspath}'
             f')>{mklens(b).out_log.syspath} 2>&1')
    finally:
      chdir(cwd)
```

Finally, we introduce a new stage to Pylightnix by instantiating a
generic [mkdrv](../Reference.md#pylightnix.core.mkdrv) stage:

``` python
from pylightnix import mkdrv, build_wrapper, match_only

hello:DRef = mkdrv(hello_config(),match_only(),build_wrapper(hello_realize),M)

print(hello)
```

``` stdout
dref:e48878b9f7760fe0972eb6863775045f-hello-bin
```

As before, we get a `DRef` promise pass it through `instantiate` and
`realize1` pipeline:

``` python
rref:RRef=realize1(instantiate(hello,m=M))
print(rref)
```

``` stdout
rref:136a30c899f36f832f45f6ed352d9ba9-e48878b9f7760fe0972eb6863775045f-hello-bin
```

### Accessing the results

Lets print the last few lines of the build log:

``` python
for line in open(mklens(rref,m=M).out_log.syspath).readlines()[-10:]:
  print(line.strip())
```

``` stdout
fi
/nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/mkdir -p '/tmp/pylightnix_hello_demo/tmp/210905-21:39:47:054952+0300_2b29fe60_q12v8sva/usr/share/info'
/nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/install -c -m 644 ./doc/hello.info '/tmp/pylightnix_hello_demo/tmp/210905-21:39:47:054952+0300_2b29fe60_q12v8sva/usr/share/info'
install-info --info-dir='/tmp/pylightnix_hello_demo/tmp/210905-21:39:47:054952+0300_2b29fe60_q12v8sva/usr/share/info' '/tmp/pylightnix_hello_demo/tmp/210905-21:39:47:054952+0300_2b29fe60_q12v8sva/usr/share/info/hello.info'
/nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/mkdir -p '/tmp/pylightnix_hello_demo/tmp/210905-21:39:47:054952+0300_2b29fe60_q12v8sva/usr/share/man/man1'
/nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/install -c -m 644 hello.1 '/tmp/pylightnix_hello_demo/tmp/210905-21:39:47:054952+0300_2b29fe60_q12v8sva/usr/share/man/man1'
make[4]: Leaving directory '/run/user/1000/tmpfs_1gkev/src'
make[3]: Leaving directory '/run/user/1000/tmpfs_1gkev/src'
make[2]: Leaving directory '/run/user/1000/tmpfs_1gkev/src'
make[1]: выход из каталога «/run/user/1000/tmpfs_1gkev/src»
```

Finally, we convert RRef to the system path and run the GNU Hello
binary.

``` python
print(Popen([mklens(rref,m=M).out_hello.syspath],
            stdout=PIPE, shell=True).stdout.read()) # type:ignore
```

``` stdout
b'Hello, world!\n'
```
