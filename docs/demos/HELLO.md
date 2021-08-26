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

First things first, Pylightnix uses filesystem storage for tracking
immutable data object (or stages) which could depend on each other. This
storage is global, it is the central part of library. In order to check
or create it, we call `initialize`:

``` python
from os import environ
from pylightnix import fsinit

environ['PYLIGHTNIX_ROOT']='/tmp/pylightnix_hello_demo'
fsinit(remove_existing=True)
```

### Fetchurl and Unpack stages

Pylightnix allows us to define, check and execute data processing
operations called **Stages**. Stages may be defined by writing Python
functions (as we will do later) or imported from a small builtin
collection.

Here we import stages `fetchurl2` and `unpack`, along with other
Pylightnix API functions.

``` python
from pylightnix import (fetchurl2, unpack, DRef, RRef, instantiate_inplace,
                        realize_inplace, mklens, selfref)
```

Our goal is to prepare stages for execution by **instantiating** them.
`fetchurl2` is the curl-based web downloader, which accepts the URL
address, the hash and the expected `out` path. We call
`instantiate_inplace` API function on it and get the `tarball`
derivation reference, which identifies both the stage and its parameters
in the Pylightnix storage. No actual work is performed yet.

``` python
hello_version = '2.10'

tarball:DRef = \
  instantiate_inplace(
    fetchurl2,
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b',
    out=[selfref, f'hello-{hello_version}.tar.gz'])
```

Next we pass the path to the tarball to the `unpack` stage by
dereferencing its `out` attribute using the
[mklens](../Reference.md#pylightnix.lens.mklens) helper function.
Pylightnix notes the fact that `unpack` has a reference to `tarball` in
its configuration.

``` python
hello_src:DRef = \
  instantiate_inplace(
    unpack,
    name='unpack-hello',
    refpath=mklens(tarball).out.refpath,
    aunpack_args=['-q'],
    src=[selfref, f'hello-{hello_version}'])
```

Now, we ask Pylightnix to give us the artifacts of `unpack` stage by
**realizing** it. Pylightnix does the dependency handling and decides to
execute both fetchurl and unpack. The results of realization is
available via realization reference `hello_rref`.

``` python
hello_rref:RRef = realize_inplace(hello_src)
print(hello_rref)
```

``` stdout
rref:b557aecd2a8cc4615100d8b4a5129874-43323fae07b9e30f65ed0a1b6213b6f0-unpack-hello
```

``` stderr
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
 30  708k   30  213k    0     0   295k      0  0:00:02 --:--:--  0:00:02  295k
100  708k  100  708k    0     0   819k      0 --:--:-- --:--:-- --:--:--  818k
hello-2.10.tar.gz: extracted to `hello-2.10'
```

Any RRef could be converted to the system path by calling
[rref2path](../Reference.md#pylightnix.core.rref2path) function or by
using a more feature-rich `mklens`:

``` python
from pylightnix import rref2path

print(rref2path(hello_rref))
print(mklens(hello_rref).val)
print(mklens(hello_rref).syspath)
print(mklens(hello_rref).src.syspath)
```

``` stdout
/tmp/pylightnix_hello_demo/store-v0/43323fae07b9e30f65ed0a1b6213b6f0-unpack-hello/b557aecd2a8cc4615100d8b4a5129874
rref:b557aecd2a8cc4615100d8b4a5129874-43323fae07b9e30f65ed0a1b6213b6f0-unpack-hello
/tmp/pylightnix_hello_demo/store-v0/43323fae07b9e30f65ed0a1b6213b6f0-unpack-hello/b557aecd2a8cc4615100d8b4a5129874
/tmp/pylightnix_hello_demo/store-v0/43323fae07b9e30f65ed0a1b6213b6f0-unpack-hello/b557aecd2a8cc4615100d8b4a5129874/hello-2.10
```

Pylightnix offers a number of other shell-like helper functions for
accessing realization, like `lsref`:

``` python
from pylightnix import lsref, catref

print(lsref(hello_rref))
```

``` stdout
['context.json', '__buildstart__.txt', 'hello-2.10', '__buildstop__.txt']
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
  src = mklens(hello_src).src.refpath
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

hello:DRef = \
  instantiate_inplace(mkdrv, hello_config(), match_only(), build_wrapper(hello_realize))

print(hello)
```

``` stdout
dref:e48878b9f7760fe0972eb6863775045f-hello-bin
```

As before, we get a `DRef`, which means that basic checks were passed,
and then call a `realize` on it:

``` python
rref:RRef=realize_inplace(hello)
print(rref)
```

``` stdout
rref:1dc4d015ec5e1fa826aabfdb09969375-e48878b9f7760fe0972eb6863775045f-hello-bin
```

### Accessing the results

Lets print the last few lines of the build log:

``` python
for line in open(mklens(rref).out_log.syspath).readlines()[-10:]:
  print(line.strip())
```

``` stdout
fi
/nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/mkdir -p '/tmp/pylightnix_hello_demo/tmp/210827-00:11:23:182473+0300_2b29fe60_sers7__6/usr/share/info'
/nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/install -c -m 644 ./doc/hello.info '/tmp/pylightnix_hello_demo/tmp/210827-00:11:23:182473+0300_2b29fe60_sers7__6/usr/share/info'
install-info --info-dir='/tmp/pylightnix_hello_demo/tmp/210827-00:11:23:182473+0300_2b29fe60_sers7__6/usr/share/info' '/tmp/pylightnix_hello_demo/tmp/210827-00:11:23:182473+0300_2b29fe60_sers7__6/usr/share/info/hello.info'
/nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/mkdir -p '/tmp/pylightnix_hello_demo/tmp/210827-00:11:23:182473+0300_2b29fe60_sers7__6/usr/share/man/man1'
/nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/install -c -m 644 hello.1 '/tmp/pylightnix_hello_demo/tmp/210827-00:11:23:182473+0300_2b29fe60_sers7__6/usr/share/man/man1'
make[4]: Leaving directory '/run/user/1000/tmp6potc48c/src'
make[3]: Leaving directory '/run/user/1000/tmp6potc48c/src'
make[2]: Leaving directory '/run/user/1000/tmp6potc48c/src'
make[1]: выход из каталога «/run/user/1000/tmp6potc48c/src»
```

Finally, we convert RRef to the system path and run the GNU Hello
binary.

``` python
print(Popen([mklens(rref).out_hello.syspath],
            stdout=PIPE, shell=True).stdout.read()) # type:ignore
```

``` stdout
b'Hello, world!\n'
```
