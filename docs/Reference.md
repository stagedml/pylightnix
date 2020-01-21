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
    * [Context](#pylightnix.types.Context)
    * [Build](#pylightnix.types.Build)
    * [Instantiator](#pylightnix.types.Instantiator)
    * [Matcher](#pylightnix.types.Matcher)
    * [Realizer](#pylightnix.types.Realizer)
    * [Derivation](#pylightnix.types.Derivation)
    * [Closure](#pylightnix.types.Closure)
    * [Manager](#pylightnix.types.Manager)
    * [Stage](#pylightnix.types.Stage)
  * [pylightnix.core](#pylightnix.core)
    * [PYLIGHTNIX\_STORE\_VERSION](#pylightnix.core.PYLIGHTNIX_STORE_VERSION)
    * [PYLIGHTNIX\_ROOT](#pylightnix.core.PYLIGHTNIX_ROOT)
    * [PYLIGHTNIX\_TMP](#pylightnix.core.PYLIGHTNIX_TMP)
    * [PYLIGHTNIX\_STORE](#pylightnix.core.PYLIGHTNIX_STORE)
    * [PYLIGHTNIX\_NAMEPAT](#pylightnix.core.PYLIGHTNIX_NAMEPAT)
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
    * [store\_context](#pylightnix.core.store_context)
    * [store\_config\_ro](#pylightnix.core.store_config_ro)
    * [store\_deps](#pylightnix.core.store_deps)
    * [store\_deepdeps](#pylightnix.core.store_deepdeps)
    * [store\_drefs](#pylightnix.core.store_drefs)
    * [store\_rrefs\_](#pylightnix.core.store_rrefs_)
    * [store\_rrefs](#pylightnix.core.store_rrefs)
    * [store\_deref](#pylightnix.core.store_deref)
    * [store\_gc](#pylightnix.core.store_gc)
    * [mkbuild](#pylightnix.core.mkbuild)
    * [build\_config](#pylightnix.core.build_config)
    * [build\_context](#pylightnix.core.build_context)
    * [build\_config\_ro](#pylightnix.core.build_config_ro)
    * [build\_outpath](#pylightnix.core.build_outpath)
    * [build\_name](#pylightnix.core.build_name)
    * [build\_deref](#pylightnix.core.build_deref)
    * [build\_deref\_path](#pylightnix.core.build_deref_path)
    * [build\_instantiate](#pylightnix.core.build_instantiate)
    * [build\_realize](#pylightnix.core.build_realize)
    * [mkcontext](#pylightnix.core.mkcontext)
    * [assert\_valid\_context](#pylightnix.core.assert_valid_context)
    * [context\_eq](#pylightnix.core.context_eq)
    * [context\_add](#pylightnix.core.context_add)
    * [context\_serialize](#pylightnix.core.context_serialize)
    * [mkdrv](#pylightnix.core.mkdrv)
    * [recursion\_manager](#pylightnix.core.recursion_manager)
    * [instantiate\_](#pylightnix.core.instantiate_)
    * [instantiate](#pylightnix.core.instantiate)
    * [realize](#pylightnix.core.realize)
    * [only](#pylightnix.core.only)
    * [mksymlink](#pylightnix.core.mksymlink)
    * [assert\_valid\_closure](#pylightnix.core.assert_valid_closure)
  * [pylightnix.stages](#pylightnix.stages)
  * [pylightnix.stages.trivial](#pylightnix.stages.trivial)
    * [mknode](#pylightnix.stages.trivial.mknode)
    * [mkfile](#pylightnix.stages.trivial.mkfile)
  * [pylightnix.stages.fetchurl](#pylightnix.stages.fetchurl)
    * [WGET](#pylightnix.stages.fetchurl.WGET)
    * [AUNPACK](#pylightnix.stages.fetchurl.AUNPACK)
    * [config](#pylightnix.stages.fetchurl.config)
    * [download](#pylightnix.stages.fetchurl.download)
    * [fetchurl](#pylightnix.stages.fetchurl.fetchurl)

<a name="pylightnix.types"></a>
# `pylightnix.types`


<a name="pylightnix.types.Path"></a>
## `Path` Objects

`Path` is an alias for string. It is used in pylightnix to
tell the typechecker that a given string contains a filesystem path.

<a name="pylightnix.types.Hash"></a>
## `Hash` Objects

`Hash` is an alias for string. It is used in pylightnix to
tell the typechecker that a given string contains sha256 hash digest.

<a name="pylightnix.types.HashPart"></a>
## `HashPart` Objects

`HashPart` is an alias for string. It is used in pylightnix to
tell the typechecker that a given string contains first 32 characters of
sha256 hash digest.

<a name="pylightnix.types.DRef"></a>
## `DRef` Objects

`DRef` is an alias for string. It is used in pylightnix to tell the
typechecker that a given string refers to some derivation.

The format of *derivation reference* is `<HashPart>-<Name>`, where:
- `<HashPart>` contains first 32 characters of derivation `Config`'s sha256
  hash digest.
- `<Name>` object contains the name of derivation.

Derivation reference 'points to' derivation object in pylightnix filesystem
storage. For any valid DRef, `$PYLIGHTNIX_STORE/<HashPart>-<Name>/` does
exist and is a directory which contains `config.json` file.

Derivation reference is normally a result of successful
[instantiation](#pylightnix.core.instantiate).

Derivation reference may be converted to a realization reference, by call
either of:
- [build_deref](#pylightnix.core.build_deref) at build time.
- [store_deref](#pylightnix.core.store_deref) to get the existing realization.
- [realize](#pylightnix.core.realize) to get new realization

<a name="pylightnix.types.RRef"></a>
## `RRef` Objects

`RRef` is an alias for string. It is used in pylightnix to tell the
typechecker that a given string refers to a particular realization of a
derivation.

The format of *realization reference* is `<HashPart0>-<HashPart1>-<Name>`,
where:
- `<HashPart0>` is calculated over realization's
  [Context](#pylightnix.types.Context) and build artifacts.
- `<HashPart1>-<Name>` forms valid [DRef](#pylightnix.types.DRef) which
  this realizaion was [realized](#pylightnix.core.realize) from.

Realization reference describes realization object in pylightnix filesystem
storage.  For valid references, `$PYLIGHTNIX_STORE/<HashPart1>-<Name>/<HashPart0>`
folder does exist and contains `context.json` file together with
stage-specific *build artifacts*

Realization reference is obtained from the process called
[realization](#pylightnix.core.realize).

Valid realization references may be dereferenced down to system paths of
*build artifacts* by calling
[store_rref2path](#pylightnix.core.store_rref2path).

<a name="pylightnix.types.Name"></a>
## `Name` Objects

`Name` is an alias for string. It is used in pylightnix to tell the
typechecker that a given string contains name of a pylightnix storage object.

Names are restircted to contain charaters matching `PYLIGHTNIX_NAMEPAT`.

See also `mkname`

<a name="pylightnix.types.RefPath"></a>
## `RefPath` Objects

RefPath is an alias for Python list (of strings). The first item of
`RefPath` is a [derivation reference](#pylightnix.types.DRef). Other elements
represent path (names of folders and optionally a filename). The path is
relative to unspecified realization of this derivation.

To convert `RefPath` into [system path](#pylightnix.types.Path), one generally
have to perform the following elementary actions:
1. Get the reference to realization of current derivation, see
   [store_deref](#pylightnix.core.store_deref) or
   [build_deref](#pylightnix.core.build_deref).
2. Convert the realization reference into system path with
   [store_rref2path](#pylightnix.core.store_rref2path)
3. Join the system path with 'relative' part of RRefPath

The above algorithm is implemented as
[build_deref_path](#pylightnix.core.build_deref_path) helper function

<a name="pylightnix.types.Config"></a>
## `Config` Objects

```python
def __init__(self, d: dict)
```

`Config` is a JSON-serializable dictionary. Configs are required by
definintion of Stages and should determine the realization process.

`Config` should match the requirements of `assert_valid_config`. Typically,
it's `__dict__` should contain JSON-serializable types only: strings, string
aliases such as [DRefs](#pylightnix.types.DRef), bools, ints, floats, lists or
other dicts. No bytes, `numpy.float32` or lambdas are allowed. Tuples are also
forbidden because they are not preserved (decoded into lists).

Use [mkconfig](#pylightnix.core.mkconfig) to create Configs from dicts.

<a name="pylightnix.types.Config.__init__"></a>
### `Config.__init__()`

```python
def __init__(self, d: dict)
```


<a name="pylightnix.types.ConfigAttrs"></a>
## `ConfigAttrs` Objects

`ConfigAttrs` is a helper object for providing a read-only access to
[Config](#pylightnix.types.Config) fields as to Python object attributes

<a name="pylightnix.types.ConfigAttrs.__getattr__"></a>
### `__getattr__`

```python
__getattr__ = dict.__getitem__
```


<a name="pylightnix.types.Context"></a>
## `Context`

```python
Context = Dict[DRef,RRef]
```

Context type is an alias for Python dict which maps
[DRefs](#pylightnix.types.DRef) into [RRefs](#pylightnix.types.RRef).

For any node grouped with it's dependencies, pylightnix forces a property of
unique realization, which means that no two nodes of a group which depend on
same derivation may resolve it to different realizations.

<a name="pylightnix.types.Build"></a>
## `Build`

```python
Build = NamedTuple('Build', [('dref',DRef), ('context',Context), ('timeprefix',str), ('outpath',Path)])
```

`Build` objects tracks the process of [realization](#pylightnix.core.realize).
As may be seen from it's signature, it stores timeprefix, the Context, and the output
path. Output path contains the path to existing temporary folder for placing *build artifacts*.

Users may access fields of a `Build` object by calling:
- [build_config](#pylightnix.core.build_config)
- [build_deref](#pylightnix.core.build_deref)
- [build_outpath](#pylightnix.core.build_outpath)

<a name="pylightnix.types.Instantiator"></a>
## `Instantiator`

```python
Instantiator = Callable[[],Config]
```


<a name="pylightnix.types.Matcher"></a>
## `Matcher`

```python
Matcher = Callable[[DRef, Context],Optional[RRef]]
```


<a name="pylightnix.types.Realizer"></a>
## `Realizer`

```python
Realizer = Callable[[DRef,Context],Path]
```


<a name="pylightnix.types.Derivation"></a>
## `Derivation`

```python
Derivation = NamedTuple('Derivation', [('dref',DRef), ('matcher',Matcher), ('realizer',Realizer) ])
```


<a name="pylightnix.types.Closure"></a>
## `Closure`

```python
Closure = NamedTuple('Closure', [('dref',DRef),('derivations',List[Derivation])])
```


<a name="pylightnix.types.Manager"></a>
## `Manager` Objects

```python
def __init__(self)
```


<a name="pylightnix.types.Manager.__init__"></a>
### `Manager.__init__()`

```python
def __init__(self)
```


<a name="pylightnix.types.Stage"></a>
## `Stage`

```python
Stage = Callable[[Manager],DRef]
```


<a name="pylightnix.core"></a>
# `pylightnix.core`


<a name="pylightnix.core.PYLIGHTNIX_STORE_VERSION"></a>
## `PYLIGHTNIX_STORE_VERSION`

```python
PYLIGHTNIX_STORE_VERSION = 1
```

*Do not change!*
Tracks the version of pylightnix storage

<a name="pylightnix.core.PYLIGHTNIX_ROOT"></a>
## `PYLIGHTNIX_ROOT`

```python
PYLIGHTNIX_ROOT = environ.get('PYLIGHTNIX_ROOT', join(environ.get('HOME','/var/run'),'_pylightnix'))
```

`PYLIGHTNIX_ROOT` contains the path to the root of pylightnix shared data folder.

Default is `~/_pylightnix` or `/var/run/_pylightnix` if no `$HOME` is available.
Setting `PYLIGHTNIX_ROOT` environment variable overwrites the defaults.

<a name="pylightnix.core.PYLIGHTNIX_TMP"></a>
## `PYLIGHTNIX_TMP`

```python
PYLIGHTNIX_TMP = environ.get('PYLIGHTNIX_TMP', join(PYLIGHTNIX_ROOT,'tmp'))
```

`PYLIGHTNIX_TMP` contains the path to the root of temporary folders.
Setting `PYLIGHTNIX_TMP` environment variable overwrites the default value of
`$PYLIGHTNIX_ROOT/tmp`.

<a name="pylightnix.core.PYLIGHTNIX_STORE"></a>
## `PYLIGHTNIX_STORE`

```python
PYLIGHTNIX_STORE = join(PYLIGHTNIX_ROOT, f'store-v{PYLIGHTNIX_STORE_VERSION}')
```

`PYLIGHTNIX_STORE` contains the path to the main pylightnix store folder.

By default, the store is located in `$PYLIGHTNIX_ROOT/store-vXX` folder.
Setting `PYLIGHTNIX_STORE` environment variable overwrites the defaults.

<a name="pylightnix.core.PYLIGHTNIX_NAMEPAT"></a>
## `PYLIGHTNIX_NAMEPAT`

```python
PYLIGHTNIX_NAMEPAT = "[a-zA-Z0-9_-]"
```

Set the regular expression pattern for valid name characters.

<a name="pylightnix.core.assert_valid_hash"></a>
## `assert_valid_hash()`

```python
def assert_valid_hash(h: Hash) -> None
```

Asserts if it's `Hash` argument is ill-formed.

<a name="pylightnix.core.trimhash"></a>
## `trimhash()`

```python
def trimhash(h: Hash) -> HashPart
```

Trim a hash to get `HashPart` objects which are used in referencing

<a name="pylightnix.core.assert_valid_hashpart"></a>
## `assert_valid_hashpart()`

```python
def assert_valid_hashpart(hp: HashPart) -> None
```


<a name="pylightnix.core.assert_valid_dref"></a>
## `assert_valid_dref()`

```python
def assert_valid_dref(ref: str) -> None
```


<a name="pylightnix.core.mkdref"></a>
## `mkdref()`

```python
def mkdref(dhash: HashPart, refname: Name) -> DRef
```


<a name="pylightnix.core.rref2dref"></a>
## `rref2dref()`

```python
def rref2dref(rref: RRef) -> DRef
```


<a name="pylightnix.core.undref"></a>
## `undref()`

```python
def undref(r: DRef) -> Tuple[HashPart, Name]
```


<a name="pylightnix.core.assert_valid_rref"></a>
## `assert_valid_rref()`

```python
def assert_valid_rref(ref: str) -> None
```


<a name="pylightnix.core.mkrref"></a>
## `mkrref()`

```python
def mkrref(rhash: HashPart, dhash: HashPart, refname: Name) -> RRef
```


<a name="pylightnix.core.unrref"></a>
## `unrref()`

```python
def unrref(r: RRef) -> Tuple[HashPart, HashPart, Name]
```


<a name="pylightnix.core.assert_valid_name"></a>
## `assert_valid_name()`

```python
def assert_valid_name(s: Name) -> None
```


<a name="pylightnix.core.mkname"></a>
## `mkname()`

```python
def mkname(s: str) -> Name
```


<a name="pylightnix.core.mkconfig"></a>
## `mkconfig()`

```python
def mkconfig(d: dict) -> Config
```


<a name="pylightnix.core.assert_valid_config"></a>
## `assert_valid_config()`

```python
def assert_valid_config(c: Config)
```


<a name="pylightnix.core.config_dict"></a>
## `config_dict()`

```python
def config_dict(c: Config) -> dict
```


<a name="pylightnix.core.config_ro"></a>
## `config_ro()`

```python
def config_ro(c: Config) -> Any
```


<a name="pylightnix.core.config_serialize"></a>
## `config_serialize()`

```python
def config_serialize(c: Config) -> str
```


<a name="pylightnix.core.config_hash"></a>
## `config_hash()`

```python
def config_hash(c: Config) -> Hash
```


<a name="pylightnix.core.config_name"></a>
## `config_name()`

```python
def config_name(c: Config) -> Name
```

Return short human-readable name of a config

<a name="pylightnix.core.config_deps"></a>
## `config_deps()`

```python
def config_deps(c: Config) -> List[DRef]
```


<a name="pylightnix.core.assert_valid_refpath"></a>
## `assert_valid_refpath()`

```python
def assert_valid_refpath(refpath: RefPath) -> None
```


<a name="pylightnix.core.assert_store_initialized"></a>
## `assert_store_initialized()`

```python
def assert_store_initialized() -> None
```


<a name="pylightnix.core.store_initialize"></a>
## `store_initialize()`

```python
def store_initialize(exist_ok: bool = True)
```


<a name="pylightnix.core.store_dref2path"></a>
## `store_dref2path()`

```python
def store_dref2path(r: DRef) -> Path
```


<a name="pylightnix.core.store_rref2path"></a>
## `store_rref2path()`

```python
def store_rref2path(r: RRef) -> Path
```


<a name="pylightnix.core.mkrefpath"></a>
## `mkrefpath()`

```python
def mkrefpath(r: DRef, items: List[str] = []) -> RefPath
```

Constructs a RefPath out of a reference `ref` and a path within the node

<a name="pylightnix.core.store_config"></a>
## `store_config()`

```python
def store_config(r: DRef) -> Config
```


<a name="pylightnix.core.store_context"></a>
## `store_context()`

```python
def store_context(r: RRef) -> Context
```


<a name="pylightnix.core.store_config_ro"></a>
## `store_config_ro()`

```python
def store_config_ro(r: DRef) -> Any
```


<a name="pylightnix.core.store_deps"></a>
## `store_deps()`

```python
def store_deps(refs: List[DRef]) -> List[DRef]
```

Return a list of reference's immediate dependencies, not including `refs`
themselves.

<a name="pylightnix.core.store_deepdeps"></a>
## `store_deepdeps()`

```python
def store_deepdeps(roots: List[DRef]) -> Set[DRef]
```

Return an exhaustive list of `roots`'s dependencies, not including `roots`
themselves.

<a name="pylightnix.core.store_drefs"></a>
## `store_drefs()`

```python
def store_drefs() -> Iterable[DRef]
```

Iterates over all derivations of the storage

<a name="pylightnix.core.store_rrefs_"></a>
## `store_rrefs_()`

```python
def store_rrefs_(dref: DRef) -> Iterable[RRef]
```


<a name="pylightnix.core.store_rrefs"></a>
## `store_rrefs()`

```python
def store_rrefs(dref: DRef, context: Context) -> Iterable[RRef]
```

`store_rrefs` iterates over those ralizations of a derivation `dref`,
that fit into particular [context]($pylightnix.types.Context).

<a name="pylightnix.core.store_deref"></a>
## `store_deref()`

```python
def store_deref(rref: RRef, dref: DRef) -> RRef
```

For any realization `rref` and it's dependency `dref`, `store_deref`
queryies the realization reference of this dependency.

See also [build_deref](#pylightnix.core.build_deref)

<a name="pylightnix.core.store_gc"></a>
## `store_gc()`

```python
def store_gc(refs_in_use: List[DRef]) -> List[DRef]
```

Take roots which are in use and should not be removed. Return roots which
are not used and may be removed. Actual removing is to be done by user-defined
application.

<a name="pylightnix.core.mkbuild"></a>
## `mkbuild()`

```python
def mkbuild(dref: DRef, context: Context) -> Build
```


<a name="pylightnix.core.build_config"></a>
## `build_config()`

```python
def build_config(b: Build) -> Config
```

Return the [Config](#pylightnix.types.Config) object of the realization
being built.

<a name="pylightnix.core.build_context"></a>
## `build_context()`

```python
def build_context(b: Build) -> Context
```

Return the [Context](#pylightnix.types.Context) object of the realization
being built.

<a name="pylightnix.core.build_config_ro"></a>
## `build_config_ro()`

```python
def build_config_ro(m: Build) -> Any
```


<a name="pylightnix.core.build_outpath"></a>
## `build_outpath()`

```python
def build_outpath(m: Build) -> Path
```

Return the output path of the realization being built. Output path is a
path to valid temporary folder where user may put various build artifacts.
Later this folder becomes a realization.

<a name="pylightnix.core.build_name"></a>
## `build_name()`

```python
def build_name(b: Build) -> Name
```

Return the name of a derivation being built.

<a name="pylightnix.core.build_deref"></a>
## `build_deref()`

```python
def build_deref(b: Build, dref: DRef) -> RRef
```

For any [realization](#pylightnix.core.realize) process described with
it's [b:Build](#pylightnix.types.Build) handler, `build_deref` queries a
realization of a dependency `dref`.

`build_deref` is designed to be called by
[Realizers](#pylightnix.types.Realizer), where the final `rref` is not yet
known.  In other cases, [store_deref](#pylightnix.core.store_deref) should be
used.

<a name="pylightnix.core.build_deref_path"></a>
## `build_deref_path()`

```python
def build_deref_path(b: Build, refpath: RefPath) -> Path
```


<a name="pylightnix.core.build_instantiate"></a>
## `build_instantiate()`

```python
def build_instantiate(c: Config) -> DRef
```


<a name="pylightnix.core.build_realize"></a>
## `build_realize()`

```python
def build_realize(dref: DRef, l: Context, o: Path) -> RRef
```


<a name="pylightnix.core.mkcontext"></a>
## `mkcontext()`

```python
def mkcontext() -> Context
```


<a name="pylightnix.core.assert_valid_context"></a>
## `assert_valid_context()`

```python
def assert_valid_context(c: Context) -> None
```


<a name="pylightnix.core.context_eq"></a>
## `context_eq()`

```python
def context_eq(a: Context, b: Context) -> bool
```


<a name="pylightnix.core.context_add"></a>
## `context_add()`

```python
def context_add(context: Context, dref: DRef, rref: RRef) -> Context
```


<a name="pylightnix.core.context_serialize"></a>
## `context_serialize()`

```python
def context_serialize(c: Context) -> str
```


<a name="pylightnix.core.mkdrv"></a>
## `mkdrv()`

```python
def mkdrv(m: Manager, inst: Instantiator, matcher: Matcher, realizer: Realizer) -> DRef
```


<a name="pylightnix.core.recursion_manager"></a>
## `recursion_manager()`

```python
@contextmanager
def recursion_manager(funcname: str)
```


<a name="pylightnix.core.instantiate_"></a>
## `instantiate_()`

```python
def instantiate_(stage: Stage, m: Manager) -> Closure
```


<a name="pylightnix.core.instantiate"></a>
## `instantiate()`

```python
def instantiate(stage: Stage) -> Closure
```

`instantiate` takes the [Stage](#pylightnix.types.Stage) function and
produces corresponding derivation object. Resulting list contains derivation
of the current stage (in it's last element), preceeded by the derivations of
all it's dependencies.

Instantiation is the equivalent of type-checking in the typical compiler's
pipeline.

User-defined [Instantiators](pylightnix.types.Instantiator) calculate stage
configs during the instantiation. This calculations fall under certain
restrictions. In particular, it shouldn't start new instantiations or
realizations recursively, and it shouldn't access realization objects in the
storage.

<a name="pylightnix.core.realize"></a>
## `realize()`

```python
def realize(closure: Closure, force_rebuild: List[DRef] = []) -> RRef
```

`realize` builds a realization of a derivation and it's dependencies.
Return value is a [reference to particular
realization](#pylightnix.types.RRef) which could be [converted to system
path](#pylightnix.core.store_rref2path) to read build artifacts.

<a name="pylightnix.core.only"></a>
## `only()`

```python
def only(dref: DRef, context: Context) -> Optional[RRef]
```


<a name="pylightnix.core.mksymlink"></a>
## `mksymlink()`

```python
def mksymlink(rref: RRef, tgtpath: Path, name: str, withtime=True) -> Path
```

Create a symlink pointing to realization `rref`. Other arguments define
symlink name and location. Informally,
`{tgtpath}/{timeprefix}{name} --> $PYLIGHTNIX_STORE/{rref2dref(rref)}/{rref}`

<a name="pylightnix.core.assert_valid_closure"></a>
## `assert_valid_closure()`

```python
def assert_valid_closure(closure: Closure) -> None
```


<a name="pylightnix.stages"></a>
# `pylightnix.stages`


<a name="pylightnix.stages.trivial"></a>
# `pylightnix.stages.trivial`


<a name="pylightnix.stages.trivial.mknode"></a>
## `mknode()`

```python
def mknode(m: Manager, sources: dict, artifacts: Dict[Name,bytes] = {}) -> DRef
```


<a name="pylightnix.stages.trivial.mkfile"></a>
## `mkfile()`

```python
def mkfile(m: Manager, name: Name, contents: bytes, filename: Optional[Name] = None) -> DRef
```


<a name="pylightnix.stages.fetchurl"></a>
# `pylightnix.stages.fetchurl`


<a name="pylightnix.stages.fetchurl.WGET"></a>
## `WGET`

```python
WGET = get_executable('wget', 'Please install `wget` pacakge')
```


<a name="pylightnix.stages.fetchurl.AUNPACK"></a>
## `AUNPACK`

```python
AUNPACK = get_executable('aunpack', 'Please install `apack` tool from `atool` package')
```


<a name="pylightnix.stages.fetchurl.config"></a>
## `config()`

```python
def config(url: str, sha256: str, mode: str = 'unpack,remove', name: Name = None) -> Config
```


<a name="pylightnix.stages.fetchurl.download"></a>
## `download()`

```python
def download(b: Build) -> Build
```


<a name="pylightnix.stages.fetchurl.fetchurl"></a>
## `fetchurl()`

```python
def fetchurl(m: Manager, args, *,, ,, kwargs) -> DRef
```


