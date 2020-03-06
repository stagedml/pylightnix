![coverage](https://codecov.io/gh/stagedml/pylightnix/branch/master/graph/badge.svg)

Pylightnix
==========

Pylightnix is a Python-based DSL library for manipulating filesystem-based
immutable data objects, inspired by the [Nix](https://nixos.org) package
manager.

Pylightnix provides a generic Python API, allowing programmers to:

* Define linked immutable data objects by specifying how to create them
  and how to operate on them.
* Actually create (build) such objects in a filesystem-based storage, access
  their data, inspect dependencies, and remove them as needed.
* Special attention is paid to the support of non-deterministic build processes.

Pylightnix originally appeared as a core module of
[StagedML](https://github.com/stagedml/stagedml) library, later it was moved
into a separate project.

Contents
--------

1. [Features](#Features)
2. [Related work](#Related-work)
3. [Install](#Install)
4. [Documentation](#Documentation)
5. [Quick start](#Quick-start)
6. [Rational](#Rational)


Features
--------

Logic:

* Pylightnix allows us to Create, query and maintain linked objects, called here
  **stages**.
* Creation of stages includes two passes: At the **instantiation** pass we check
  configurations of the whole graph of linked objects. At the **realization**
  pass we decide whether to take existing realization or to run the constructors
  to get new ones.
* Pylightnix is focused on non-deterministic build processes such as machine
  learning. We formalize comparison and selection of competing results of such
  processes.
* The possible applications of Pylightnix include:
  - Data science / Machine learning experiments (see [StagedML](https://github.com/stagedml/stagedml))
  - Domain-specific package managers
  - Other applications which fit into blackboard design pattern
    ([wiki](https://en.wikipedia.org/wiki/Blackboard_design_pattern)).

Implementation:

* Written in Python 3.6, [mypy](http://mypy-lang.org/) typing information is
  provided.
* Tested with Pytest and [hypothesis](https://hypothesis.works).
* No non-standard Python dependencies. We do require
  [wget](https://www.gnu.org/software/wget/) and
  [atool](https://www.nongnu.org/atool/) system packages.
* Alas, Pylightnix is not a production-ready yet! Nor parallelism, neither
  network synchronization are supported out of the box. Also, we didn't check it
  on any operating system besides Linux.
  - We tried our best to make base Pylightnix operations atomic. This
    allows running several instances of the library on a single storage.
  - As a consequence, stage synchronization of different machines should be
    possible by exclusively running `rsync` tool on their storages.


Related work
------------

* [Nix](https://nixos.org) ([repo](https://github.com/nixos/nix), [comparison](./docs/Comparison.md#Pylightnix-vs-Nix))
* [Spack](https://spack.io) ([repo](https://github.com/spack/spack))
* [Popper](https://falsifiable.us) ([repo](https://github.com/systemslab/popper))
* [CK](https://cknowledge.org) ([repo](https://github.com/ctuning/ck))


Install
-------

#### Install with Pip

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

Documentation
-------------

Demos:

* [Hello](./docs/demos/HELLO.md), building GNU Hello with a toy package manager.
* [Ultimatum tutorial](https://github.com/grwlf/ultimatum-game/blob/master/docs/Pylightnix.md), managing experiments.
* [MNIST demo](./docs/demos/MNIST.md) shows machine learning specifics.
* [REPL demo](./docs/demos/REPL.md) illustrates how to debug stages
  using Read-Eval-Print-friendly routines [(wiki)](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop).

Reference:

* [API Reference](./docs/Reference.md)
* [Tests](./tests)


Quick start
-----------

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
   from pylightnix import mkdrv, build_wrapper, match_latest, dirrw

   def hello_config()->Config:
     name:str = 'hello-bin'
     src:RefPath = [hello_src, f'hello-{hello_version}']
     return mkconfig(locals())

   def hello_realize(b:Build)->None:
     c:Any = build_cattrs(b)
     o:Path = build_outpath(b)
     with TemporaryDirectory() as tmp:
       copytree(build_path(b,c.src),join(tmp,'src'))
       dirrw(Path(join(tmp,'src')))
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

6. Pylightnix provides a set of bash-like functions for inspecting the storage.

   ```python
   from pylightnix import lsref, catref, shellref, rmref, du
   ```

   We could list the contents of the realization, cat some of it's text files,
   open an interactive Unix shell as set by the `SHELL` environment variable.
   `rmref` may be used to completely remove the realization or derivation from
   the storage (safety checks are up to the user for now). `du` stands for
   'disk usage' and calculates the size of realizations stored.


Rational
--------

* Q: Why based on Nix ideas?
* A: There are many solutions in the area of software deployment. Besides Nix,
  we know all the traditional package managers, Docker, AppImage, VirtualBox,
  other virtualizers. One property of Nix we want to highlight is it's low
  system requirements. Basically, Nix' core may work on a system which has only
  a filestorage and symlinks. Here we try to follow this trend by keeping the
  number of dependencies low while providing a competitive set of features.



* Q: Why does the API contain mostly functions and almost no classes?
* A: Several reasones: a) This would allow us to keep users informed about the
  API changes. We are trying to avoid changes in functions which are already
  published. By importing functions explicitly, users will notice such changes
  quickly. b) Typical class-based APIs of Python often let users think that they
  could extend it by sub-classing. Here we don't want to misinform users. c)
  Class-based wrapper API may be created as a standalone module, see
  [Lens](./docs/Reference.md#pylightnix.lens.Lens).


( TODO )



