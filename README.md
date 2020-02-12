![coverage](https://codecov.io/gh/stagedml/pylightnix/branch/master/graph/badge.svg)


# Pylightnix

Pylightnix is a Python-based DSL library for manipulating filesystem-based
immutable data objects, inspired by the [Nix](https://nixos.org) package
manager.

Pylightnix provides a generic Python API, allowing programmers to:
* Define linked immutable data objects by specifying how to create them
  and how to operate on them.
* Actually create (build) such objects in a filesystem-based storage, access
  their data, inspect dependencies, and remove them as needed.
* Special attention is paid to the support of non-deterministic build processes.


## Contents

1. [Features](#Features)
2. [Related work](#Related-work)
2. [Install](#Install)
3. [Documentation](#Documentation)
4. [Quick start](#Quick-start)


## Features

Functions:

* Two-staged build process allows users to check the build plan before executing
  it.
* Focused on non-deterministic build processes, formalizing comparison and selection
  of build results.
* Clean and compact implementation:
  - Suitable for Data science / Machine learning experiments
  - Match applications which fit into [blackboard design
    pattern](https://en.wikipedia.org/wiki/Blackboard_design_pattern).

Implementation:

* Written in Python 3.6, [mypy](http://mypy-lang.org/) typing information is
  provided.
* Tested with Pytest and [hypothesis](https://hypothesis.works).
* No non-standard Python dependencies. We do require
  [wget](https://www.gnu.org/software/wget/) and
  [atool](https://www.nongnu.org/atool/) system packages.
* Alas, Pylightnix is not a production-ready yet! Nor parallelism, neither network
  synchronization are supported. Also, we didn't check it on any operating system
  besides Linux.


## Related work

* [Nix](https://nixos.org) ([repo](https://github.com/nixos/nix))
* [Spack](https://spack.io) ([repo](https://github.com/spack/spack))
* [Popper](https://falsifiable.us) ([repo](https://github.com/systemslab/popper))
* [CK](https://cknowledge.org) ([repo](https://github.com/ctuning/ck))


## Install

#### Using Pip

Pylightnix is not yet released on Pypi, the only way to install it with pip
is to use the git link:

 ```shell
 $ pip3 install git+https://github.com/stagedml/pylightnix
 ```

#### Build from source

1. Clone the repo
   ```
   $ git clone https://github.com/stagedml/pylightnix
   $ cd pylightnix
   ```
2. Either
   - (a) Setup `PYTHONPATH` to point to the sources.
     ```
     export PYTHONPATH="`pwd`/src:$PYTHONPATH"
     ```
     Now you could import pylightnix from your applications.

   - (b) Build and install pylightnix wheel.
     ```
     $ make wheels
     $ sudo -H pip3 install --force dist/*whl
     ```
   - (c) Nix users may refer to [default.nix](./default.nix) and
     [shell.nix](./shell.nix) expressions.
3. (Optional) Run the tests and make docs
   ```
   $ make coverage
   $ make docs
   ```
4. (Optional) Demos require `pweave` package.
   ```
   $ make demos
   ```

## Documentation

Demos:

* [Hello](./docs/demos/HELLO.md), building GNU Hello with a toy package manager.
* [Ultimatum tutorial](https://github.com/grwlf/ultimatum-game/blob/master/docs/Pylightnix.md), managing experiments.
* [MNIST demo](./docs/demos/MNIST.md), running machine learning models.

Reference:

* [API Reference](./docs/Reference.md)
* [Tests](./tests)

## Quick start

Pylightnix could be used as a lightweight build system (but rather unsafe,
because of the lack of built-in build isolation). This quick start illustrates
this use-case by defining a couple of objects ("stages") required to build the
GNU Hello program.

The below operations require pure Python environment with Pylightnix library
installed.

1. Install the development version of pylightnix and run IPython.

   ```shell
   $ pip install ipython git+https://github.com/stagedml/pylightnix
   $ ipython
   ```

   Subsequent steps may be copypasted into the IPython shell

2. Make sure that the storage is initialized

   ```python
   from pylightnix import store_initialize
   store_initialize()
   ```

3. Define the process of  `fetchurl` stage. We use `_inplace` subset of
   Pylightnix API for simplicity. It relies on a single global variable for
   storing tracking the build plan.

   ```python
   from pylightnix import DRef, instantiate_inplace, fetchurl
   from pylightnix import RRef, realize_inplace

   hello_version = '2.10'

   # Phase 1, create the derivation
   hello_src:DRef = \
     instantiate_inplace(
       fetchurl,
       name='hello-src',
       url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
       sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b')

   # Phase 2, realize the derivation into actual object
   hello_rref:RRef = realize_inplace(hello_src)
   print(hello_rref)
   ```

4. Define how to create an object containing GNU Hello binary, that is, a
   Hello-builder stage

   ```python
   from tempfile import TemporaryDirectory
   from shutil import copytree
   from os import getcwd, chdir, system
   from os.path import join
   from pylightnix import Config, mkconfig
   from pylightnix import Path, Build, build_cattrs, build_outpath, build_path
   from pylightnix import mkdrv, build_wrapper, match_latest

   def hello_config()->Config:
     name:str = 'hello-bin'
     src:RefPath = [hello_src, f'hello-{hello_version}']
     return mkconfig(locals())

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

   # Phase 1, create the derivation. Note, we reference previous stage's
   # derivation in the configuration of this derivation.
   hello_dref:DRef = \
       instantiate_inplace(mkdrv, hello_config(), match_latest(), build_wrapper(hello_realize))

   # Phase 2, realize the derivation
   hello_rref:RRef = realize_inplace(hello_dref)

   print(hello_rref)
   ```

   We now have a [realization
   reference](./docs/Reference.md#pylightnix.types.RRef) which describes the
   concrete folder in the filesystem storage, which contains the binary
   artifacts we put there during the realization. Next calls to `realize` would
   simply return the same reference unless we ask it to produce another
   realization by passing `force_rebuild=[hello_dref]` argument (and unless the
   build process really produces a different data).

5. We now access our hello-binary object, and run the GNU Hello program it
   contains.

   ```python
   from pylightnix import rref2path

   path=rref2path(hello_rref)
   system(join(path,'usr/bin/hello'))
   ```

   Output:

   ```
   Hello World!
   ```


