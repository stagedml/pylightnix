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
    * [trimhash](#pylightnix.core.trimhash)
    * [mkdref](#pylightnix.core.mkdref)
    * [rref2dref](#pylightnix.core.rref2dref)
    * [undref](#pylightnix.core.undref)
    * [mkrref](#pylightnix.core.mkrref)
    * [unrref](#pylightnix.core.unrref)
    * [mkname](#pylightnix.core.mkname)
    * [mkconfig](#pylightnix.core.mkconfig)
    * [config\_dict](#pylightnix.core.config_dict)
    * [config\_ro](#pylightnix.core.config_ro)
    * [config\_serialize](#pylightnix.core.config_serialize)
    * [config\_hash](#pylightnix.core.config_hash)
    * [config\_name](#pylightnix.core.config_name)
    * [config\_deps](#pylightnix.core.config_deps)
    * [assert\_store\_initialized](#pylightnix.core.assert_store_initialized)
    * [store\_initialize](#pylightnix.core.store_initialize)
    * [store\_dref2path](#pylightnix.core.store_dref2path)
    * [rref2path](#pylightnix.core.rref2path)
    * [mkrefpath](#pylightnix.core.mkrefpath)
    * [store\_config](#pylightnix.core.store_config)
    * [store\_context](#pylightnix.core.store_context)
    * [store\_cattrs](#pylightnix.core.store_cattrs)
    * [store\_deps](#pylightnix.core.store_deps)
    * [store\_deepdeps](#pylightnix.core.store_deepdeps)
    * [store\_drefs](#pylightnix.core.store_drefs)
    * [store\_rrefs\_](#pylightnix.core.store_rrefs_)
    * [store\_rrefs](#pylightnix.core.store_rrefs)
    * [store\_deref](#pylightnix.core.store_deref)
    * [store\_gc](#pylightnix.core.store_gc)
    * [store\_instantiate](#pylightnix.core.store_instantiate)
    * [store\_realize](#pylightnix.core.store_realize)
    * [mkbuild](#pylightnix.core.mkbuild)
    * [build\_wrapper](#pylightnix.core.build_wrapper)
    * [build\_config](#pylightnix.core.build_config)
    * [build\_context](#pylightnix.core.build_context)
    * [build\_cattrs](#pylightnix.core.build_cattrs)
    * [build\_outpath](#pylightnix.core.build_outpath)
    * [build\_name](#pylightnix.core.build_name)
    * [build\_deref](#pylightnix.core.build_deref)
    * [build\_path](#pylightnix.core.build_path)
    * [mkcontext](#pylightnix.core.mkcontext)
    * [context\_eq](#pylightnix.core.context_eq)
    * [context\_add](#pylightnix.core.context_add)
    * [context\_deref](#pylightnix.core.context_deref)
    * [context\_serialize](#pylightnix.core.context_serialize)
    * [mkdrv](#pylightnix.core.mkdrv)
    * [recursion\_manager](#pylightnix.core.recursion_manager)
    * [instantiate\_](#pylightnix.core.instantiate_)
    * [instantiate](#pylightnix.core.instantiate)
    * [realize](#pylightnix.core.realize)
    * [mksymlink](#pylightnix.core.mksymlink)
    * [only](#pylightnix.core.only)
    * [largest](#pylightnix.core.largest)
    * [assert\_valid\_refpath](#pylightnix.core.assert_valid_refpath)
    * [assert\_valid\_config](#pylightnix.core.assert_valid_config)
    * [assert\_valid\_name](#pylightnix.core.assert_valid_name)
    * [isrref](#pylightnix.core.isrref)
    * [assert\_valid\_rref](#pylightnix.core.assert_valid_rref)
    * [assert\_valid\_hashpart](#pylightnix.core.assert_valid_hashpart)
    * [isdref](#pylightnix.core.isdref)
    * [assert\_valid\_dref](#pylightnix.core.assert_valid_dref)
    * [assert\_valid\_hash](#pylightnix.core.assert_valid_hash)
    * [assert\_valid\_context](#pylightnix.core.assert_valid_context)
    * [assert\_valid\_closure](#pylightnix.core.assert_valid_closure)
    * [assert\_no\_rref\_deps](#pylightnix.core.assert_no_rref_deps)
    * [assert\_have\_realizers](#pylightnix.core.assert_have_realizers)
  * [pylightnix.inplace](#pylightnix.inplace)
    * [PYLIGHTNIX\_MANAGER](#pylightnix.inplace.PYLIGHTNIX_MANAGER)
    * [instantiate\_inplace](#pylightnix.inplace.instantiate_inplace)
    * [realize\_inplace](#pylightnix.inplace.realize_inplace)
  * [pylightnix.stages](#pylightnix.stages)
  * [pylightnix.stages.trivial](#pylightnix.stages.trivial)
    * [mknode](#pylightnix.stages.trivial.mknode)
    * [mkfile](#pylightnix.stages.trivial.mkfile)
  * [pylightnix.stages.fetch](#pylightnix.stages.fetch)
    * [WGET](#pylightnix.stages.fetch.WGET)
    * [AUNPACK](#pylightnix.stages.fetch.AUNPACK)
    * [fetchurl](#pylightnix.stages.fetch.fetchurl)
  * [pylightnix.bashlike](#pylightnix.bashlike)
    * [lsdref\_](#pylightnix.bashlike.lsdref_)
    * [lsrref\_](#pylightnix.bashlike.lsrref_)
    * [lsref](#pylightnix.bashlike.lsref)
    * [catrref\_](#pylightnix.bashlike.catrref_)
    * [catref](#pylightnix.bashlike.catref)
    * [rmrref](#pylightnix.bashlike.rmrref)
    * [rmdref](#pylightnix.bashlike.rmdref)
    * [rmref](#pylightnix.bashlike.rmref)

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
storage. For a valid DRef, `$PYLIGHTNIX_STORE/<HashPart>-<Name>/` does
exist and is a directory which contains `config.json` file.

Derivation references are results of
[instantiation](#pylightnix.core.instantiate).

Derivation reference may be converted into a [realization
reference](#pylightnix.types.RRef) by either dereferencing (that is querying
for existing realizations) or [realizing](#pylightnix.core.realize) it from
scratch.

For derefencing, one can use [build_deref](#pylightnix.core.build_deref) at
build time or [store_deref](#pylightnix.core.store_deref) otherwise.

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
[rref2path](#pylightnix.core.rref2path).

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
   [rref2path](#pylightnix.core.rref2path)
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

For any derivation, Context stores a mapping from it's dependencie's
derivations to their realizations. In contrast to
[Closure](#pylightnix.types.Closure) type, Context contains a minimal closure
of derivation's dependencies.

<a name="pylightnix.types.Build"></a>
## `Build`

```python
Build = NamedTuple('Build', [('dref',DRef), ('context',Context), ('timeprefix',str), ('outpath',Path)])
```

Build is a helper object which tracks the process of [realization](#pylightnix.core.realize).

Useful associated functions are:
- [build_wrapper](#pylightnix.core.build_wrapper)
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

Realizer is a user-defined function which defines how to
[build](#pylightnix.core.realize) a given derivation in a given
[context](#pylightnix.types.Context).

For given derivation being built, it's Realizer may access the following
objects via [Build helpers](#pylightnix.types.Build):
- Configuration of the derivation and configurations of all it's
dependencies. See [build_config](#pylightnix.core.build_config).
- Realizations of all the dependencies (and thus, their build artifacts).
See [build_path](#pylightnix.core.build_path).

<a name="pylightnix.types.Derivation"></a>
## `Derivation`

```python
Derivation = NamedTuple('Derivation', [('dref',DRef), ('matcher',Matcher), ('realizer',Realizer) ])
```

Derivation is a core type of Pylightnix. It keeps all the information about
a stage: it's [configuration](#pylightnix.types.Config), how to
[realize](#pylightnix.core.realize) it and how to make a selection among
multiple realizations. Information is stored partly on disk (in the
storage), partly in memory in form of a Python code.

<a name="pylightnix.types.Closure"></a>
## `Closure`

```python
Closure = NamedTuple('Closure', [('dref',DRef),('derivations',List[Derivation])])
```

Closure is a named tuple, encoding a reference to derivation and a whole list
of it's dependencies, plus maybe some additional derivations. So the closure
is complete but not necessary minimal.

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
PYLIGHTNIX_STORE_VERSION = 0
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

<a name="pylightnix.core.trimhash"></a>
## `trimhash()`

```python
def trimhash(h: Hash) -> HashPart
```

Trim a hash to get `HashPart` objects which are used in referencing

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


<a name="pylightnix.core.assert_store_initialized"></a>
## `assert_store_initialized()`

```python
def assert_store_initialized() -> None
```


<a name="pylightnix.core.store_initialize"></a>
## `store_initialize()`

```python
def store_initialize(custom_store: Optional[str] = None, custom_tmp: Optional[str] = None) -> None
```

Create the storage and temp direcories. Default locations are determined
by `PYLIGHTNIX_STORE` and `PYLIGHTNIX_TMP` variables. Note, that they could be
overwritten either by setting environment variables of the same name before
starting the Python or by assigning to them right after importing pylighnix.

See also [assert_store_initialized](#pylightnix.core.assert_store_initialized).

Example:
```python
import pylightnix.core
pylightnix.core.PYLIGHTNIX_STORE='/tmp/custom_pylightnix_storage'
pylightnix.core.PYLIGHTNIX_TMP='/tmp/custom_pylightnix_tmp'
pylightnix.core.store_initialize()
```

<a name="pylightnix.core.store_dref2path"></a>
## `store_dref2path()`

```python
def store_dref2path(r: DRef) -> Path
```


<a name="pylightnix.core.rref2path"></a>
## `rref2path()`

```python
def rref2path(r: RRef) -> Path
```


<a name="pylightnix.core.mkrefpath"></a>
## `mkrefpath()`

```python
def mkrefpath(r: DRef, items: List[str] = []) -> RefPath
```

Construct a RefPath out of a reference `ref` and a path within the node

<a name="pylightnix.core.store_config"></a>
## `store_config()`

```python
def store_config(r: Union[DRef,RRef]) -> Config
```


<a name="pylightnix.core.store_context"></a>
## `store_context()`

```python
def store_context(r: RRef) -> Context
```


<a name="pylightnix.core.store_cattrs"></a>
## `store_cattrs()`

```python
def store_cattrs(r: Union[DRef,RRef]) -> Any
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

Iterate over all realizations of a derivation `dref`. The sort order is
unspecified.

<a name="pylightnix.core.store_rrefs"></a>
## `store_rrefs()`

```python
def store_rrefs(dref: DRef, context: Context) -> Iterable[RRef]
```

Iterate over those realizations of a derivation `dref`, which match a
[context]($pylightnix.types.Context). The sort order is unspecified.

<a name="pylightnix.core.store_deref"></a>
## `store_deref()`

```python
def store_deref(context_holder: RRef, dref: DRef) -> RRef
```

For any realization `context_holder` and it's dependency `dref`, `store_deref`
queries the realization reference of this dependency.

See also [build_deref](#pylightnix.core.build_deref)

<a name="pylightnix.core.store_gc"></a>
## `store_gc()`

```python
def store_gc(refs_in_use: List[DRef]) -> List[DRef]
```

Take roots which are in use and should not be removed. Return roots which
are not used and may be removed. Actual removing is to be done by user-defined
application.

<a name="pylightnix.core.store_instantiate"></a>
## `store_instantiate()`

```python
def store_instantiate(c: Config) -> DRef
```


<a name="pylightnix.core.store_realize"></a>
## `store_realize()`

```python
def store_realize(dref: DRef, l: Context, o: Path) -> RRef
```


<a name="pylightnix.core.mkbuild"></a>
## `mkbuild()`

```python
def mkbuild(dref: DRef, context: Context, buildtime: bool = True) -> Build
```


<a name="pylightnix.core.build_wrapper"></a>
## `build_wrapper()`

```python
def build_wrapper(f: Callable[[Build],None], buildtime: bool = True) -> Realizer
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

<a name="pylightnix.core.build_cattrs"></a>
## `build_cattrs()`

```python
def build_cattrs(m: Build) -> Any
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
it's [Build](#pylightnix.types.Build) handler, `build_deref` queries a
realization of dependency `dref`.

`build_deref` is designed to be called from
[Realizer](#pylightnix.types.Realizer) functions. In other cases,
[store_deref](#pylightnix.core.store_deref) should be used.

<a name="pylightnix.core.build_path"></a>
## `build_path()`

```python
def build_path(b: Build, refpath: RefPath) -> Path
```


<a name="pylightnix.core.mkcontext"></a>
## `mkcontext()`

```python
def mkcontext() -> Context
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


<a name="pylightnix.core.context_deref"></a>
## `context_deref()`

```python
def context_deref(context: Context, dref: DRef) -> RRef
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
def instantiate_(m: Manager, stage: Any, args, *,, ,, kwargs) -> Closure
```


<a name="pylightnix.core.instantiate"></a>
## `instantiate()`

```python
def instantiate(stage: Any, args, *,, ,, kwargs) -> Closure
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

New derivations are added to the storage by moving a temporary folder inside
the storage folder.

<a name="pylightnix.core.realize"></a>
## `realize()`

```python
def realize(closure: Closure, force_rebuild: List[DRef] = []) -> RRef
```

Build a realization of the derivation by executing a
[Realizer](#pylightnix.types.Realizer) on it's
[Closure](#pylightnix.types.Closure).

Return [reference to new realization](#pylightnix.types.RRef) which could be
later [converted to system path](#pylightnix.core.rref2path) to access build
artifacts.

New realization is added to the storage by moving a temporary folder inside
the storage. `realize` assumes that derivation is still there at this moment
(See e.g. [rmref](#pylightnix.bashlike.rmref))

- FIXME: stage's context is calculated inefficiently. Maybe one should track
  dep.tree to avoid calling `store_deepdeps` within the cycle.

<a name="pylightnix.core.mksymlink"></a>
## `mksymlink()`

```python
def mksymlink(rref: RRef, tgtpath: Path, name: str, withtime=True) -> Path
```

Create a symlink pointing to realization `rref`. Other arguments define
symlink name and location. Informally,
`{tgtpath}/{timeprefix}{name} --> $PYLIGHTNIX_STORE/{rref2dref(rref)}/{rref}`

<a name="pylightnix.core.only"></a>
## `only()`

```python
def only() -> Matcher
```

Return a [Matcher](#pylightnix.types.Matcher) which expects no more than
one realization for every [derivation](#pylightnix.types.DRef), given the
[context](#pylightnix.types.Context).

<a name="pylightnix.core.largest"></a>
## `largest()`

```python
def largest(filename: str) -> Matcher
```

Return a [Matcher](#pylightnix.types.Matcher) which checks contexts of
realizations and then compares them based on stage-specific scores. For each
realization, score is read from artifact file named `filename` that should
contain a single float number. Realization with largest score wins.

<a name="pylightnix.core.assert_valid_refpath"></a>
## `assert_valid_refpath()`

```python
def assert_valid_refpath(refpath: RefPath) -> None
```


<a name="pylightnix.core.assert_valid_config"></a>
## `assert_valid_config()`

```python
def assert_valid_config(c: Config)
```


<a name="pylightnix.core.assert_valid_name"></a>
## `assert_valid_name()`

```python
def assert_valid_name(s: Name) -> None
```


<a name="pylightnix.core.isrref"></a>
## `isrref()`

```python
def isrref(ref: str) -> bool
```


<a name="pylightnix.core.assert_valid_rref"></a>
## `assert_valid_rref()`

```python
def assert_valid_rref(ref: str) -> None
```


<a name="pylightnix.core.assert_valid_hashpart"></a>
## `assert_valid_hashpart()`

```python
def assert_valid_hashpart(hp: HashPart) -> None
```


<a name="pylightnix.core.isdref"></a>
## `isdref()`

```python
def isdref(ref: str) -> bool
```


<a name="pylightnix.core.assert_valid_dref"></a>
## `assert_valid_dref()`

```python
def assert_valid_dref(ref: str) -> None
```


<a name="pylightnix.core.assert_valid_hash"></a>
## `assert_valid_hash()`

```python
def assert_valid_hash(h: Hash) -> None
```

Asserts if it's `Hash` argument is ill-formed.

<a name="pylightnix.core.assert_valid_context"></a>
## `assert_valid_context()`

```python
def assert_valid_context(c: Context) -> None
```


<a name="pylightnix.core.assert_valid_closure"></a>
## `assert_valid_closure()`

```python
def assert_valid_closure(closure: Closure) -> None
```


<a name="pylightnix.core.assert_no_rref_deps"></a>
## `assert_no_rref_deps()`

```python
def assert_no_rref_deps(c: Config) -> None
```


<a name="pylightnix.core.assert_have_realizers"></a>
## `assert_have_realizers()`

```python
def assert_have_realizers(m: Manager, drefs: List[DRef]) -> None
```


<a name="pylightnix.inplace"></a>
# `pylightnix.inplace`


<a name="pylightnix.inplace.PYLIGHTNIX_MANAGER"></a>
## `PYLIGHTNIX_MANAGER`

```python
PYLIGHTNIX_MANAGER = Manager()
```

Global Derivation manager used for Inplace mode of operation

<a name="pylightnix.inplace.instantiate_inplace"></a>
## `instantiate_inplace()`

```python
def instantiate_inplace(stage: Any, args, *,, ,, kwargs) -> DRef
```


<a name="pylightnix.inplace.realize_inplace"></a>
## `realize_inplace()`

```python
def realize_inplace(dref: DRef, force_rebuild: List[DRef] = []) -> RRef
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


<a name="pylightnix.stages.fetch"></a>
# `pylightnix.stages.fetch`


<a name="pylightnix.stages.fetch.WGET"></a>
## `WGET`

```python
WGET = get_executable('wget', 'Please install `wget` pacakge')
```


<a name="pylightnix.stages.fetch.AUNPACK"></a>
## `AUNPACK`

```python
AUNPACK = get_executable('aunpack', 'Please install `apack` tool from `atool` package')
```


<a name="pylightnix.stages.fetch.fetchurl"></a>
## `fetchurl()`

```python
def fetchurl(m: Manager, url: str, sha256: str, mode: str = 'unpack,remove', drvname: Optional[Name] = None, filename: Optional[str] = None) -> DRef
```

Download and unpack an URL addess.

Downloading is done by calling `wget` application. Optional unpacking is
performed with the `aunpack` script from `atool` package. `sha256` defines the
expected SHA-256 hashsum of the stored data. `mode` allows to tweak the
stage's behavior: adding word 'unpack' instructs fetchurl to unpack the
package, adding 'remove' instructs it to remove the archive after unpacking.

<a name="pylightnix.bashlike"></a>
# `pylightnix.bashlike`


<a name="pylightnix.bashlike.lsdref_"></a>
## `lsdref_()`

```python
def lsdref_(r: DRef) -> Iterable[str]
```


<a name="pylightnix.bashlike.lsrref_"></a>
## `lsrref_()`

```python
def lsrref_(r: RRef) -> Iterable[str]
```


<a name="pylightnix.bashlike.lsref"></a>
## `lsref()`

```python
def lsref(r: Union[RRef,DRef]) -> List[str]
```

List the contents of `r`. For [DRefs](#pylightnix.types.DRef), return
realization hashes. For [RRefs](#pylightnix.types.RRef), list artifact files.

<a name="pylightnix.bashlike.catrref_"></a>
## `catrref_()`

```python
def catrref_(r: RRef, fn: List[str]) -> Iterable[str]
```


<a name="pylightnix.bashlike.catref"></a>
## `catref()`

```python
def catref(r: RRef, fn: List[str]) -> List[str]
```

Return the contents of r's artifact file `fn` line by line.

<a name="pylightnix.bashlike.rmrref"></a>
## `rmrref()`

```python
def rmrref(r: RRef) -> None
```


<a name="pylightnix.bashlike.rmdref"></a>
## `rmdref()`

```python
def rmdref(r: DRef) -> None
```


<a name="pylightnix.bashlike.rmref"></a>
## `rmref()`

```python
def rmref(r: Union[RRef,DRef]) -> None
```

Forcebly remove a reference from the storage. Removing
[DRefs](#pylightnix.types.DRef) also removes all their realizations.

Currently Pylightnix makes no attempts to synchronize an access to the
storage.  Users are expected to take care of possible parallelization issues.

