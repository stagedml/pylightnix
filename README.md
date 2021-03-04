![coverage](https://codecov.io/gh/stagedml/pylightnix/branch/master/graph/badge.svg)

Pylightnix
==========

Pylightnix is a Python domain specific language library for managing
filesystem-based immutable data objects, inspired by
[Purely Functional Software Deployment Model thesis by Eelco Dolstra](https://edolstra.github.io/pubs/phd-thesis.pdf) and the [Nix](https://nixos.org) package manager. In contrast to Nix, Pylightnix
is primarily focused on managing the data for computer science experiments.
Traditional use case of domain-specific package management, as well as other
[blackboard application use cases](https://en.wikipedia.org/wiki/Blackboard_design_pattern) are also supported.

With the help of Pylightnix API, applications
* Store the data in form of linked immutable filesystem objects here
  called **stages**.
* Create (in our terms, **realize**) such objects, access its
  data, navigate through dependencies.
* Re-run realization algorithms whenever inputs change. Pylightnix
  may decide to re-create either a whole or a part of the stage object
  collection according to the changes in prerequisites.
* Manage the outcomes of **non-deterministic** stage realizations.
  As one example, users may define a Pylightnix stage to depend on top-10 (in
  a user-defined sense) random instances of a trained machine learning model.

Documentation
-------------

QuickStart [[PDF]](https://raw.github.com/stagedml/pylightnix-docs/master/Pylightnix-QuickStart-latest.pdf) |
Manual [[PDF]](https://raw.github.com/stagedml/pylightnix-docs/master/Pylightnix-Manual-latest.pdf) |
API Referece [[MD]](./docs/Reference.md)

Demos:

* [Hello](./docs/demos/HELLO.md), building GNU Hello with a toy package manager.
* [Ultimatum tutorial](https://github.com/grwlf/ultimatum-game/blob/master/docs/Pylightnix.md),
  managing experiments.
* [MNIST demo](./docs/demos/MNIST.md) shows machine learning specifics.
* [REPL demo](./docs/demos/REPL.md) illustrates how to debug stages using

