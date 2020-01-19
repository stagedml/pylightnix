# Table of Contents

  * [pylightnix.types](#pylightnix.types)
    * [Path](#pylightnix.types.Path)
    * [Hash](#pylightnix.types.Hash)
    * [HashPart](#pylightnix.types.HashPart)
    * [DRef](#pylightnix.types.DRef)
    * [RRef](#pylightnix.types.RRef)
    * [Name](#pylightnix.types.Name)
    * [RefPath](#pylightnix.types.RefPath)
    * [Config](#pylightnix.types.Config)
    * [ConfigAttrs](#pylightnix.types.ConfigAttrs)
    * [Closure](#pylightnix.types.Closure)
    * [Build](#pylightnix.types.Build)
    * [Instantiator](#pylightnix.types.Instantiator)
    * [Matcher](#pylightnix.types.Matcher)
    * [Realizer](#pylightnix.types.Realizer)
    * [Derivation](#pylightnix.types.Derivation)
    * [Manager](#pylightnix.types.Manager)
    * [Stage](#pylightnix.types.Stage)
  * [pylightnix.core](#pylightnix.core)
    * [PYLIGHTNIX\_STORE\_VERSION](#pylightnix.core.PYLIGHTNIX_STORE_VERSION)
    * [assert\_valid\_hash](#pylightnix.core.assert_valid_hash)
    * [trimhash](#pylightnix.core.trimhash)
    * [assert\_valid\_hashpart](#pylightnix.core.assert_valid_hashpart)
    * [assert\_valid\_dref](#pylightnix.core.assert_valid_dref)
    * [mkdref](#pylightnix.core.mkdref)
    * [rref2dref](#pylightnix.core.rref2dref)
    * [undref](#pylightnix.core.undref)
    * [assert\_valid\_rref](#pylightnix.core.assert_valid_rref)
    * [mkrref](#pylightnix.core.mkrref)
    * [unrref](#pylightnix.core.unrref)
    * [assert\_valid\_name](#pylightnix.core.assert_valid_name)
    * [mkname](#pylightnix.core.mkname)
    * [mkconfig](#pylightnix.core.mkconfig)
    * [assert\_valid\_config](#pylightnix.core.assert_valid_config)
    * [config\_dict](#pylightnix.core.config_dict)
    * [config\_ro](#pylightnix.core.config_ro)
    * [config\_serialize](#pylightnix.core.config_serialize)
    * [config\_hash](#pylightnix.core.config_hash)
    * [config\_name](#pylightnix.core.config_name)
    * [config\_deps](#pylightnix.core.config_deps)
    * [assert\_valid\_refpath](#pylightnix.core.assert_valid_refpath)
    * [assert\_store\_initialized](#pylightnix.core.assert_store_initialized)
    * [store\_initialize](#pylightnix.core.store_initialize)
    * [store\_dref2path](#pylightnix.core.store_dref2path)
    * [store\_rref2path](#pylightnix.core.store_rref2path)
    * [mkrefpath](#pylightnix.core.mkrefpath)
    * [store\_config](#pylightnix.core.store_config)
    * [store\_closure](#pylightnix.core.store_closure)
    * [store\_config\_ro](#pylightnix.core.store_config_ro)
    * [store\_deps](#pylightnix.core.store_deps)
    * [store\_deepdeps](#pylightnix.core.store_deepdeps)
    * [store\_link](#pylightnix.core.store_link)
    * [store\_drefs](#pylightnix.core.store_drefs)
    * [store\_rrefs](#pylightnix.core.store_rrefs)
    * [store\_deref](#pylightnix.core.store_deref)
    * [store\_gc](#pylightnix.core.store_gc)
    * [mkbuild](#pylightnix.core.mkbuild)
    * [build\_config](#pylightnix.core.build_config)
    * [build\_closure](#pylightnix.core.build_closure)
    * [build\_config\_ro](#pylightnix.core.build_config_ro)
    * [build\_outpath](#pylightnix.core.build_outpath)
    * [build\_name](#pylightnix.core.build_name)
    * [build\_rref](#pylightnix.core.build_rref)
    * [build\_deref](#pylightnix.core.build_deref)
    * [build\_instantiate](#pylightnix.core.build_instantiate)
    * [build\_realize](#pylightnix.core.build_realize)
    * [mkclosure](#pylightnix.core.mkclosure)
    * [assert\_valid\_closure](#pylightnix.core.assert_valid_closure)
    * [closure\_eq](#pylightnix.core.closure_eq)
    * [closure\_add](#pylightnix.core.closure_add)
    * [closure\_serialize](#pylightnix.core.closure_serialize)
    * [manage](#pylightnix.core.manage)
    * [instantiate](#pylightnix.core.instantiate)
    * [realize](#pylightnix.core.realize)
    * [only](#pylightnix.core.only)

# `pylightnix.types`


## `Path` Objects


## `Hash` Objects


## `HashPart` Objects


## `DRef` Objects

Derivation Reference is a string containing a name of Derivation

## `RRef` Objects

Realization reference is a string containing a name of Derivation Instance

## `Name` Objects

A stage's name is what you see in the last part of the reference

## `RefPath` Objects

RefPath is a path referencing some file in some instance. It is
represented by a list of strings, where the first string is `RRef`

## `Config` Objects

```python
def __init__(self, d: dict)
```

Config is a JSON-serializable configuration object. It should match the
requirements of `assert_valid_config`. Tupically, it's __dict__ should
contain only either simple Python types (strings, bool, ints, floats), lists
or dicts. No tuples, no `np.float32`, no functions. Fields with names
starting from '_' are may be added after construction, but they are not
preserved during the serialization.

### `Config.__init__()`

```python
def __init__(self, d: dict)
```


## `ConfigAttrs` Objects

Helper object allowing to access dict fields as attributes

### `__getattr__`

```python
__getattr__ = dict.__getitem__
```


## `Closure`

```python
Closure = Dict[DRef,RRef]
```


## `Build`

```python
Build = NamedTuple('Build', [('config',Config),
                             ('closure',Closure),
           ...
```


## `Instantiator`

```python
Instantiator = Callable[[],Config]
```


## `Matcher`

```python
Matcher = Callable[[DRef, Closure],Optional[RRef]]
```


## `Realizer`

```python
Realizer = Callable[[DRef,Closure],Build]
```


## `Derivation`

```python
Derivation = NamedTuple('Derivation', [('dref',DRef),
                                       ('matcher',Matcher), ...
```


## `Manager` Objects

```python
def __init__(self)
```


### `Manager.__init__()`

```python
def __init__(self)
```


## `Stage`

```python
Stage = Callable[[Manager],DRef]
```


# `pylightnix.core`


## `PYLIGHTNIX_STORE_VERSION`

```python
PYLIGHTNIX_STORE_VERSION = 1
```


## `assert_valid_hash()`

```python
def assert_valid_hash(h: Hash) -> None
```


## `trimhash()`

```python
def trimhash(h: Hash) -> HashPart
```


## `assert_valid_hashpart()`

```python
def assert_valid_hashpart(hp: HashPart) -> None
```


## `assert_valid_dref()`

```python
def assert_valid_dref(ref: str) -> None
```


## `mkdref()`

```python
def mkdref(dhash: HashPart, refname: Name) -> DRef
```


## `rref2dref()`

```python
def rref2dref(rref: RRef) -> DRef
```


## `undref()`

```python
def undref(r: DRef) -> Tuple[HashPart, Name]
```


## `assert_valid_rref()`

```python
def assert_valid_rref(ref: str) -> None
```


## `mkrref()`

```python
def mkrref(rhash: HashPart, dhash: HashPart, refname: Name) -> RRef
```


## `unrref()`

```python
def unrref(r: RRef) -> Tuple[HashPart, HashPart, Name]
```


## `assert_valid_name()`

```python
def assert_valid_name(s: Name) -> None
```


## `mkname()`

```python
def mkname(s: str) -> Name
```


## `mkconfig()`

```python
def mkconfig(d: dict) -> Config
```


## `assert_valid_config()`

```python
def assert_valid_config(c: Config)
```


## `config_dict()`

```python
def config_dict(c: Config) -> dict
```


## `config_ro()`

```python
def config_ro(c: Config) -> Any
```


## `config_serialize()`

```python
def config_serialize(c: Config) -> str
```


## `config_hash()`

```python
def config_hash(c: Config) -> Hash
```


## `config_name()`

```python
def config_name(c: Config) -> Name
```

Return short human-readable name of a config

## `config_deps()`

```python
def config_deps(c: Config) -> List[DRef]
```


## `assert_valid_refpath()`

```python
def assert_valid_refpath(refpath: RefPath) -> None
```


## `assert_store_initialized()`

```python
def assert_store_initialized() -> None
```


## `store_initialize()`

```python
def store_initialize(exist_ok: bool = True)
```


## `store_dref2path()`

```python
def store_dref2path(r: DRef) -> Path
```


## `store_rref2path()`

```python
def store_rref2path(r: RRef) -> Path
```


## `mkrefpath()`

```python
def mkrefpath(r: DRef, items: List[str] = []) -> RefPath
```

Constructs a RefPath out of a reference `ref` and a path within the node

## `store_config()`

```python
def store_config(r: DRef) -> Config
```


## `store_closure()`

```python
def store_closure(r: RRef) -> Closure
```


## `store_config_ro()`

```python
def store_config_ro(r: DRef) -> Any
```


## `store_deps()`

```python
def store_deps(refs: List[DRef]) -> List[DRef]
```

Return a list of reference's dependencies, that is all the references
found in current ref's `Config`

## `store_deepdeps()`

```python
def store_deepdeps(roots: List[DRef]) -> List[DRef]
```

Return an exhaustive list of dependencies of the `roots`. `roots`
themselves are also included.

## `store_link()`

```python
def store_link(ref: DRef, tgtpath: Path, name: str, withtime=True) -> None
```

Creates a link pointing to node `ref` into directory `tgtpath`

## `store_drefs()`

```python
def store_drefs() -> Iterable[DRef]
```


## `store_rrefs()`

```python
def store_rrefs(dref: DRef) -> Iterable[RRef]
```


## `store_deref()`

```python
def store_deref(rref: RRef, dref: DRef) -> RRef
```


## `store_gc()`

```python
def store_gc(refs_in_use: List[DRef]) -> List[DRef]
```

Take roots which are in use and should not be removed. Return roots which
are not used and may be removed. Actual removing is to be done by user-defined
application.

## `mkbuild()`

```python
def mkbuild(dref: DRef, closure: Closure) -> Build
```


## `build_config()`

```python
def build_config(b: Build) -> Config
```


## `build_closure()`

```python
def build_closure(b: Build) -> Closure
```


## `build_config_ro()`

```python
def build_config_ro(m: Build) -> Any
```


## `build_outpath()`

```python
def build_outpath(m: Build) -> Path
```


## `build_name()`

```python
def build_name(b: Build) -> Name
```


## `build_rref()`

```python
def build_rref(b: Build, dref: DRef) -> RRef
```


## `build_deref()`

```python
def build_deref(b: Build, refpath: RefPath) -> Path
```


## `build_instantiate()`

```python
def build_instantiate(c: Config) -> DRef
```


## `build_realize()`

```python
def build_realize(dref: DRef, b: Build) -> RRef
```


## `mkclosure()`

```python
def mkclosure() -> Closure
```


## `assert_valid_closure()`

```python
def assert_valid_closure(c: Closure) -> None
```


## `closure_eq()`

```python
def closure_eq(a: Closure, b: Closure) -> bool
```


## `closure_add()`

```python
def closure_add(closure: Closure, dref: DRef, rref: RRef) -> Closure
```


## `closure_serialize()`

```python
def closure_serialize(c: Closure) -> str
```


## `manage()`

```python
def manage(m: Manager, inst: Instantiator, matcher: Matcher, realizer: Realizer) -> DRef
```


## `instantiate()`

```python
def instantiate(stage: Stage) -> List[Derivation]
```


## `realize()`

```python
def realize(stage: Stage, force_rebuild: List[DRef] = []) -> RRef
```


## `only()`

```python
def only(dref: DRef, closure: Closure) -> Optional[RRef]
```


