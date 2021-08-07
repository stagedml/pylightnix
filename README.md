![coverage](https://codecov.io/gh/stagedml/pylightnix/branch/master/graph/badge.svg)

Pylightnix
==========

Pylightnix is a minimalistic Python library for managing filesystem-based
immutable data objects, inspired by [Purely Functional Software Deployment Model
thesis by Eelco Dolstra](https://edolstra.github.io/pubs/phd-thesis.pdf) and the
[Nix](https://nixos.org) package manager.

The library may be thought as of low-level API for creating caching wrappers
for a subset of Python functions. In particular, Pylightnix allows user to

* Prepare (or, in our terms, **instantiate**) the computation plan aimed at
  creating a tree of linked immutable **stages** objects, stored in the
  filesystem.
* Implement (**realize**) the prepared computation plan, access the resulting
  artifacts. Pylightnix is able to handle possible **non-deterministic** results
  of the computation. As one example, it is possible to define a stage depending
  on best top-10 instances (in a user-defined sence) of prerequisite stages.
* Handle changes in the computation plan, re-use the existing artifacts
  whenever possible.
* Gain full control over all aspects of the cached data including the
  garbage-collection.

Documentation
-------------

QuickStart [[PDF]](https://raw.github.com/stagedml/pylightnix-docs/master/Pylightnix-QuickStart-latest.pdf) |
Manual [[PDF]](https://raw.github.com/stagedml/pylightnix-docs/master/Pylightnix-Manual-latest.pdf) |
API Referece [[MD]](./docs/Reference.md)

Demos:

* [Hello](./docs/demos/HELLO.md), building GNU Hello with a toy package manager.
* [Ultimatum tutorial](https://github.com/grwlf/ultimatum-game/blob/master/docs/Pylightnix.md),
  managing experiments.
* [MNIST demo](./docs/demos/MNIST.md) shows some machine learning specific.
* [REPL demo](./docs/demos/REPL.md) illustrates how to debug stage sequences.

