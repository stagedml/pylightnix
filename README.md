# Pylightnix

Pylightnix is a Python-based DSL library for manipulating
[Nix](https://nixos.org/nix)-style data storage.

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

## API Reference

[Link](./docs/Reference.md)
