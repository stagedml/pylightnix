![coverage](https://codecov.io/gh/stagedml/pylightnix/branch/master/graph/badge.svg)

# Pylightnix

Pylightnix is a Python-based DSL library for manipulating
[Nix](https://nixos.org/nix)-style data storage.

Contents:

1. [Features](#Features)
2. [Build](#Build)
3. [Quick start](#Quick_start)
4. [Documentation](#Documentation)

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
     Now you could import pylightnix from your application.

   - (b) Build and install pylightnix wheel.
     ```
     $ rm -rf build dist || true
     $ python3 setup.py sdist bdist_wheel
     $ sudo -H pip3 install --force dist/*whl
     ```
3. Optionally, run the tests
   ```
   $ make coverage
   ```

## Quick start

Pylightnix provides API for data deployment system right in your Python
application. Here we illustrate the concepts using [GNU
hello](https://www.gnu.org/software/hello) building problem as an example.

_Note: we'll omit non-pylighnix imports here. Check [the complete 
sources of Hello demo](./docs/demos/HELLO.py) for details_

First things first, we should know that Pylightnix uses filesystem storage for
tracking immutable data object called nodes which could depend on each other.
This storage is the central part of library, all the magic happens there. So
let's initialize it:

```python
from pylightnix import store_initialize
store_initialize()
```

Location of the storage is kept in an internal global variable. It may be
changed either by passing arguments to this function or by other methods. Check
the [Reference](./docs/Reference.md#pylightnix.core.store_initialize) for
details.

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
[DRef](./docs/Reference.md#pylightnix.types.DRef) which takes a reference to a
**Derivation** of fetchurl stage. It means several things: a) the configuration
of our stage does already exist in the storage and it doesn't contain critical
errors like invalid links. b) Pylighnix knows how to **Realize** this
derivation, i.e. what Python function to call on it and which directory to
collect the output from.

So what will we have when Realization of `hello_src` is complete? As [fetchurl's
documentation](./docs/Reference.md#pylightnix.stages.fetchurl.fetchurl)
suggests, we will see a downloaded and unpacked URL, in our case it is the
contents of `hello-2.10.tar.gz` archive. Let's check it:

```python
from pylightnix import RRef, realize_inplace

hello_rref:RRef = realize_inplace(hello_src)
print(hello_rref)
```

OK, now we should see signs of actual work being done. Something was just
downloaded and we also should see a string starting with 'rref:...' in our
_stdout_. This string is a **Realization reference** of type
[RRef](./docs/Reference.md#pylightnix.types.RRef) which uniquely identifies
some data node in the Pylightnix storage.

### Custom stages

We want to build the GNU hello, so we need some code to build it. Pylighnix aims
at providing only a generic minimalistic API, so it doesn't have a builtin stage for
compiling applications. Luckily, it is not hard to define it, as we should see.

In Pylighnix, stages consist of three important components:
* The configuration, which is a JSON-Object of parameters and references
* The realizer, which is a Python function encoding the actual build process
* The matcher, which is another Python function for dealing with
    non-determenistic builds.

The matcher business is beyound the scope of this quick start. For now, we just
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
[RefPath](#docs/Reference.md#pylightnix.types.RefPath) which links our new stage
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
    chdir(join(tmp,'src'))
    system(f'./configure --prefix=/usr')
    system(f'make')
    system(f'make install DESTDIR={o}')
```

As we may see here, `hello_realize` function takes a
[Build](#docs/Reference.md#pylightnix.types.Build) helper, which brings us two
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
  instantiate_inplace(mkdrv, hello_config, only, build_wrapper(hello_build))
```

In this instantiation, [mkdrv](#Reference.md#pylightnix.core.mkdrv) (which
stands for 'make derivation') takes the place of `fetchurl`. As before, we get a
`DRev` and that means we could:

```python
rref:RRef=realize_inplace(hello)
```

Once the realization is ready, we could [convert it to
system path](#Reference.md#pylightnix.core.rref2path) directly:

```python
from pylightnix import rref2path

path=rref2path(rref)
system(join(path,'usr/bin/hello'))
```

The last call should greet us with

```
Hello World!
```

## Documentation

* [HELLO demo](./docs/demos/HELLO.md)
* [MNIST demo](./docs/demos/MNIST.md)
* [API Reference](./docs/Reference.md)
* [A bunch of tests](./tests)


