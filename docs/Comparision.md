
Pylightnix vs Nix
-----------------

* Like Nix, Pylightnix offers purely-functional solution for data deployment problem.
* Like Nix, Pylightnix allows user to describe and run two-phased build
  processes in a controllable and reproducible manner.
* Unlike Nix, pylightnix doesn't aim at providing operating system-wide package
  manager. Instead it tries to provide a reliable API for application-wide
  storage for immutable objects, which could be a backbone for some package
  manager, but also could be used for other tasks, such as data science
  experiment management.
* Unlike Nix, Pylightnix doesn't provide neither interpeter for separate
  configuration language, nor build isolation. Both instantiation and
  realization phases are to be defined in Python. There are certain mechanisms
  to increase safety, like the recursion checker, but in general, users are
  to take their responsibility of not breaking the concepts.
* Unlike Nix, Pylightnix is aware of non-deterministic builds, which allows
  it to cover a potentially larger set of use cases.

