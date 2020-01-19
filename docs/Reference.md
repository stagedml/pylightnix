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

<a name="pylightnix.types"></a>
# `pylightnix.types`


<a name="Path"></a>
## `Path` Objects


<a name="Hash"></a>
## `Hash` Objects


<a name="HashPart"></a>
## `HashPart` Objects


<a name="DRef"></a>
## `DRef` Objects

Derivation Reference is a string containing a name of Derivation

<a name="RRef"></a>
## `RRef` Objects

Realization reference is a string containing a name of Derivation Instance

<a name="Name"></a>
## `Name` Objects

A stage's name is what you see in the last part of the reference

<a name="RefPath"></a>
## `RefPath` Objects

RefPath is a path referencing some file in some instance. It is
represented by a list of strings, where the first string is `RRef`

<a name="Config"></a>
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

<a name="\_\_init\_\_"></a>
### `Config.__init__()`

```python
def __init__(self, d: dict)
```


<a name="ConfigAttrs"></a>
## `ConfigAttrs` Objects

Helper object allowing to access dict fields as attributes

<a name="\_\_getattr\_\_"></a>
### `__getattr__`

```python
__getattr__ = dict.__getitem__
```


<a name="Closure"></a>
## `Closure`

```python
Closure = Dict[DRef,RRef]
```


<a name="Build"></a>
## `Build`

```python
Build = NamedTuple('Build', [('config',Config), ('closure',Closure), ('timeprefix',str), ('outpath',Path)])
```


<a name="Instantiator"></a>
## `Instantiator`

```python
Instantiator = Callable[[],Config]
```


<a name="Matcher"></a>
## `Matcher`

```python
Matcher = Callable[[DRef, Closure],Optional[RRef]]
```


<a name="Realizer"></a>
## `Realizer`

```python
Realizer = Callable[[DRef,Closure],Build]
```


<a name="Derivation"></a>
## `Derivation`

```python
Derivation = NamedTuple('Derivation', [('dref',DRef), ('matcher',Matcher), ('realizer',Realizer) ])
```


<a name="Manager"></a>
## `Manager` Objects

```python
def __init__(self)
```


<a name="\_\_init\_\_"></a>
### `Manager.__init__()`

```python
def __init__(self)
```


<a name="Stage"></a>
## `Stage`

```python
Stage = Callable[[Manager],DRef]
```


<a name="pylightnix.core"></a>
# `pylightnix.core`


<a name="PYLIGHTNIX\_STORE\_VERSION"></a>
## `PYLIGHTNIX_STORE_VERSION`

```python
PYLIGHTNIX_STORE_VERSION = 1
```


<a name="assert\_valid\_hash"></a>
## `assert_valid_hash()`

```python
def assert_valid_hash(h: Hash) -> None
```


<a name="trimhash"></a>
## `trimhash()`

```python
def trimhash(h: Hash) -> HashPart
```


<a name="assert\_valid\_hashpart"></a>
## `assert_valid_hashpart()`

```python
def assert_valid_hashpart(hp: HashPart) -> None
```


<a name="assert\_valid\_dref"></a>
## `assert_valid_dref()`

```python
def assert_valid_dref(ref: str) -> None
```


<a name="mkdref"></a>
## `mkdref()`

```python
def mkdref(dhash: HashPart, refname: Name) -> DRef
```


<a name="rref2dref"></a>
## `rref2dref()`

```python
def rref2dref(rref: RRef) -> DRef
```


<a name="undref"></a>
## `undref()`

```python
def undref(r: DRef) -> Tuple[HashPart, Name]
```


<a name="assert\_valid\_rref"></a>
## `assert_valid_rref()`

```python
def assert_valid_rref(ref: str) -> None
```


<a name="mkrref"></a>
## `mkrref()`

```python
def mkrref(rhash: HashPart, dhash: HashPart, refname: Name) -> RRef
```


<a name="unrref"></a>
## `unrref()`

```python
def unrref(r: RRef) -> Tuple[HashPart, HashPart, Name]
```


<a name="assert\_valid\_name"></a>
## `assert_valid_name()`

```python
def assert_valid_name(s: Name) -> None
```


<a name="mkname"></a>
## `mkname()`

```python
def mkname(s: str) -> Name
```


<a name="mkconfig"></a>
## `mkconfig()`

```python
def mkconfig(d: dict) -> Config
```


<a name="assert\_valid\_config"></a>
## `assert_valid_config()`

```python
def assert_valid_config(c: Config)
```


<a name="config\_dict"></a>
## `config_dict()`

```python
def config_dict(c: Config) -> dict
```


<a name="config\_ro"></a>
## `config_ro()`

```python
def config_ro(c: Config) -> Any
```


<a name="config\_serialize"></a>
## `config_serialize()`

```python
def config_serialize(c: Config) -> str
```


<a name="config\_hash"></a>
## `config_hash()`

```python
def config_hash(c: Config) -> Hash
```


<a name="config\_name"></a>
## `config_name()`

```python
def config_name(c: Config) -> Name
```

Return short human-readable name of a config

<a name="config\_deps"></a>
## `config_deps()`

```python
def config_deps(c: Config) -> List[DRef]
```


<a name="assert\_valid\_refpath"></a>
## `assert_valid_refpath()`

```python
def assert_valid_refpath(refpath: RefPath) -> None
```


<a name="assert\_store\_initialized"></a>
## `assert_store_initialized()`

```python
def assert_store_initialized() -> None
```


<a name="store\_initialize"></a>
## `store_initialize()`

```python
def store_initialize(exist_ok: bool = True)
```


<a name="store\_dref2path"></a>
## `store_dref2path()`

```python
def store_dref2path(r: DRef) -> Path
```


<a name="store\_rref2path"></a>
## `store_rref2path()`

```python
def store_rref2path(r: RRef) -> Path
```


<a name="mkrefpath"></a>
## `mkrefpath()`

```python
def mkrefpath(r: DRef, items: List[str] = []) -> RefPath
```

Constructs a RefPath out of a reference `ref` and a path within the node

<a name="store\_config"></a>
## `store_config()`

```python
def store_config(r: DRef) -> Config
```


<a name="store\_closure"></a>
## `store_closure()`

```python
def store_closure(r: RRef) -> Closure
```


<a name="store\_config\_ro"></a>
## `store_config_ro()`

```python
def store_config_ro(r: DRef) -> Any
```


<a name="store\_deps"></a>
## `store_deps()`

```python
def store_deps(refs: List[DRef]) -> List[DRef]
```

Return a list of reference's dependencies, that is all the references
found in current ref's `Config`

<a name="store\_deepdeps"></a>
## `store_deepdeps()`

```python
def store_deepdeps(roots: List[DRef]) -> List[DRef]
```

Return an exhaustive list of dependencies of the `roots`. `roots`
themselves are also included.

<a name="store\_link"></a>
## `store_link()`

```python
def store_link(ref: DRef, tgtpath: Path, name: str, withtime=True) -> None
```

Creates a link pointing to node `ref` into directory `tgtpath`

<a name="store\_drefs"></a>
## `store_drefs()`

```python
def store_drefs() -> Iterable[DRef]
```


<a name="store\_rrefs"></a>
## `store_rrefs()`

```python
def store_rrefs(dref: DRef) -> Iterable[RRef]
```


<a name="store\_deref"></a>
## `store_deref()`

```python
def store_deref(rref: RRef, dref: DRef) -> RRef
```


<a name="store\_gc"></a>
## `store_gc()`

```python
def store_gc(refs_in_use: List[DRef]) -> List[DRef]
```

Take roots which are in use and should not be removed. Return roots which
are not used and may be removed. Actual removing is to be done by user-defined
application.

<a name="mkbuild"></a>
## `mkbuild()`

```python
def mkbuild(dref: DRef, closure: Closure) -> Build
```


<a name="build\_config"></a>
## `build_config()`

```python
def build_config(b: Build) -> Config
```


<a name="build\_closure"></a>
## `build_closure()`

```python
def build_closure(b: Build) -> Closure
```


<a name="build\_config\_ro"></a>
## `build_config_ro()`

```python
def build_config_ro(m: Build) -> Any
```


<a name="build\_outpath"></a>
## `build_outpath()`

```python
def build_outpath(m: Build) -> Path
```


<a name="build\_name"></a>
## `build_name()`

```python
def build_name(b: Build) -> Name
```


<a name="build\_rref"></a>
## `build_rref()`

```python
def build_rref(b: Build, dref: DRef) -> RRef
```


<a name="build\_deref"></a>
## `build_deref()`

```python
def build_deref(b: Build, refpath: RefPath) -> Path
```


<a name="build\_instantiate"></a>
## `build_instantiate()`

```python
def build_instantiate(c: Config) -> DRef
```


<a name="build\_realize"></a>
## `build_realize()`

```python
def build_realize(dref: DRef, b: Build) -> RRef
```


<a name="mkclosure"></a>
## `mkclosure()`

```python
def mkclosure() -> Closure
```


<a name="assert\_valid\_closure"></a>
## `assert_valid_closure()`

```python
def assert_valid_closure(c: Closure) -> None
```


<a name="closure\_eq"></a>
## `closure_eq()`

```python
def closure_eq(a: Closure, b: Closure) -> bool
```


<a name="closure\_add"></a>
## `closure_add()`

```python
def closure_add(closure: Closure, dref: DRef, rref: RRef) -> Closure
```


<a name="closure\_serialize"></a>
## `closure_serialize()`

```python
def closure_serialize(c: Closure) -> str
```


<a name="manage"></a>
## `manage()`

```python
def manage(m: Manager, inst: Instantiator, matcher: Matcher, realizer: Realizer) -> DRef
```


<a name="instantiate"></a>
## `instantiate()`

```python
def instantiate(stage: Stage) -> List[Derivation]
```


<a name="realize"></a>
## `realize()`

```python
def realize(stage: Stage, force_rebuild: List[DRef] = []) -> RRef
```


<a name="only"></a>
## `only()`

```python
def only(dref: DRef, closure: Closure) -> Optional[RRef]
```


