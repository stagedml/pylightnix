![coverage](https://codecov.io/gh/stagedml/pylightnix/branch/master/graph/badge.svg)

Pylightnix
==========

Pylightnix is a minimalistic Python library for managing filesystem-based
immutable data, inspired by [Purely Functional Software Deployment Model thesis
by Eelco Dolstra](https://edolstra.github.io/pubs/phd-thesis.pdf) and the
[Nix](https://nixos.org) package manager.

The library may be thought as of low-level API for creating caching wrappers for
a subset of Python functions. In particular, Pylightnix allows user to

- Prepare (or, in our terms - **instantiate**) the computation plan aimed at
  creating a tree of linked immutable stage objects, stored in the filesystem.
- Implement (in our terms - **realize**) the prepared computation plan, access
  the resulting artifacts. Pylightnix is able to handle **non-deterministic**
  results of the computation.
- Handle changes in the computation plan, re-use the existing artifacts whenever
  possible.
- Gain full control over the cached data by inspecting the storage

``` python
import numpy as np
from pylightnix import *

fsinit('_pylightnix')

@autostage
def stage_dataset(A=100, file=[selfref, 'dataset.npy']):
  np.save(file, np.arange(0, A))

@autostage(nouts=10)
def stage_train(rindex:int, dataset=stage_dataset, model=[selfref, 'model.npy']):
  ds = np.load(dataset.file.val)
  np.save(model, rindex)

rrefs=realizeMany(instantiate(stage_train))
assert len(rrefs)>=10
```

## Documentation

QuickStart
[\[PDF\]](https://raw.github.com/stagedml/pylightnix-docs/master/Pylightnix-QuickStart-latest.pdf)
\| API Referece [\[MD\]](./docs/Reference.md)

Demos:

- [GNU Hello](./docs/demos/HELLO.md), turn Pylightnix into a toy
  package manager to build the GNU Hello from sources.
- [MDRUN](./docs/demos/MDRUN.py), evaluate code sections of a Markdown
  document, cache the results between runs.

