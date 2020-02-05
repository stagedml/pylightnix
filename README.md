![coverage](https://codecov.io/gh/stagedml/pylightnix/branch/master/graph/badge.svg)

# Pylightnix

Pylightnix is a Python-based DSL library for manipulating
[Nix](https://nixos.org/nix)-style data storage.

Contents:

1. [Features](#Features)
2. [Build](#Build)
3. [Documentation](#Documentation)
4. [Quick start](#Quick-start)

## Features:

Compared to Nix:

* Like Nix, pylightnix offers purely-functional solution for data deployment problem.
* Like Nix, pylightnix allows user to describe and run two-phased build
  processes in a controllable and reproducible manner.
* Unlike Nix, pylightnix doesn't aim at building operating systems. It
  is more suitable for managing application-scale data storage.
* Unlike Nix, pylightnix doesn't provide things like interpreter for build
  expression language and build isolation. Here, both configuration and build
  phases are defined in Python.
* Unlike Nix, pylightnix is aware of non-deterministic builds, which allows
  it to cover a potentially larger set of use cases.

Implementation:

* Compact codebase
* Tested with [mypy static typechecker](http://mypy-lang.org/) and
  [hypothesis](https://hypothesis.works)
* Little-to-no non-standard Python dependencies (still we do require certain
  system packages, like `wget` and [atool](https://www.nongnu.org/atool/)).
* Alas, Pylightnix is not a production-ready yet! Nor parallelism, neither network
  synchronization are supported. Also, we didn't check it on any operating systems
  besides Linux.

## Build

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

* [API Reference](./docs/Reference.md)
* [HELLO demo](./docs/demos/HELLO.md)
* [MNIST demo](./docs/demos/MNIST.md)
* [Tests](./tests)

## Quick start

[HELLO demo](./docs/demos/HELLO.md) will contain a kind of deeper introduction.

1. Initialize the storage

   ```python
   from pylightnix import store_initialize
   store_initialize()
   ```

2. Use builtin `fetchurl` stage

   ```python
   from pylightnix import DRef, instantiate_inplace, fetchurl
   from pylightnix import RRef, realize_inplace

   hello_version = '2.10'

   hello_src:DRef = \
     instantiate_inplace(
       fetchurl,
       name='hello-src',
       url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
       sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b')

   hello_rref:RRef = realize_inplace(hello_src)
   print(hello_rref)
   ```

3. Define a custom stage

   ```python
   from pylightnix import Config, mkconfig
   from pylightnix import Path, Build, build_cattrs, build_outpath, build_path
   from pylightnix import mkdrv, build_wrapper, match_only

   def hello_config()->Config:
     name = 'hello-bin'
     src = [hello_src, f'hello-{hello_version}']
     return mkconfig(locals())

   def hello_realize(b:Build)->None:
     c:Any = build_cattrs(b)
     o:Path = build_outpath(b)
     with TemporaryDirectory() as tmp:
       copytree(build_path(b,c.src),join(tmp,'src'))
       chdir(join(tmp,'src'))
       system(f'./configure --prefix=/usr')
       system(f'make')
       system(f'make install DESTDIR={o}')

   hello_dref:DRef = \
       instantiate_inplace(mkdrv, hello_config, match_only(), build_wrapper(hello_realize))
   hello_rref:RRef = realize_inplace(hello_dref)


   from pylightnix import rref2path

   path=rref2path(hello_rref)
   system(join(path,'usr/bin/hello'))
   ```

   Output:
   ```
   Hello World!
   ```
