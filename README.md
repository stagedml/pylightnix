![coverage](https://codecov.io/gh/stagedml/pylightnix/branch/master/graph/badge.svg)

Pylightnix
==========

Pylightnix is a minimalistic Python library for managing filesystem-based
immutable data objects, inspired by [Purely Functional Software Deployment Model
thesis by Eelco Dolstra](https://edolstra.github.io/pubs/phd-thesis.pdf) and the
[Nix](https://nixos.org) package manager.

The library may be thought as of low-level API for creating caching wrappers
for a subset of Python functions. In particular, Pylightnix allows user to

* Prepare (or, in our terms - **instantiate**) the computation plan aimed at
  creating a tree of linked immutable stage objects, stored in the filesystem.
* Implement (in our terms - **realize**) the prepared computation plan, access
  the resulting artifacts. Pylightnix is able to handle **non-deterministic**
  results of the computation. As one example, it is possible to define a stage
  depending on best top-10 instances (in a user-defined sense) of prerequisite
  stages.
* Handle changes in the computation plan, re-use the existing artifacts
  whenever possible.
* Gain full control over all aspects of the cached data including the
  garbage-collection.

Documentation
-------------

QuickStart [[PDF]](https://raw.github.com/stagedml/pylightnix-docs/master/Pylightnix-QuickStart-latest.pdf) |
API Referece [[MD]](./docs/Reference.md)

Demos:

* [GNU Hello](./docs/demos/HELLO.md), turns Pylightnix into a toy
  package manager to build the GNU Hello from sources.
* [MDRUN](./docs/demos/MDRUN.py), evaluates code sections of a Markdown document,
  cache the results between runs.

(Outdated)

Manual [[PDF]](https://raw.github.com/stagedml/pylightnix-docs/master/Pylightnix-Manual-latest.pdf)

* [Ultimatum tutorial](https://github.com/grwlf/ultimatum-game/blob/master/docs/Pylightnix.md),
  managing experiments.
* [MNIST demo](./docs/demos/MNIST.md) shows some machine learning specific.
* [REPL demo](./docs/demos/REPL.md) illustrates how to debug stage sequences.

