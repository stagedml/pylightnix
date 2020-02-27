# Table of Contents

  * [pylightnix.types](#pylightnix.types)
    * [Path](#pylightnix.types.Path)
    * [Hash](#pylightnix.types.Hash)
    * [HashPart](#pylightnix.types.HashPart)
    * [DRef](#pylightnix.types.DRef)
    * [RRef](#pylightnix.types.RRef)
    * [Name](#pylightnix.types.Name)
    * [RefPath](#pylightnix.types.RefPath)
    * [PYLIGHTNIX\_PROMISE\_TAG](#pylightnix.types.PYLIGHTNIX_PROMISE_TAG)
    * [PromisePath](#pylightnix.types.PromisePath)
    * [Context](#pylightnix.types.Context)
    * [Matcher](#pylightnix.types.Matcher)
    * [Realizer](#pylightnix.types.Realizer)
    * [Derivation](#pylightnix.types.Derivation)
    * [Closure](#pylightnix.types.Closure)
    * [Config](#pylightnix.types.Config)
    * [ConfigAttrs](#pylightnix.types.ConfigAttrs)
    * [BuildArgs](#pylightnix.types.BuildArgs)
    * [Build](#pylightnix.types.Build)
    * [Manager](#pylightnix.types.Manager)
    * [Stage](#pylightnix.types.Stage)
    * [Key](#pylightnix.types.Key)
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
    * [config\_cattrs](#pylightnix.core.config_cattrs)
    * [config\_serialize](#pylightnix.core.config_serialize)
    * [config\_hash](#pylightnix.core.config_hash)
    * [config\_name](#pylightnix.core.config_name)
    * [config\_deps](#pylightnix.core.config_deps)
    * [config\_substitutePromises](#pylightnix.core.config_substitutePromises)
    * [config\_promises](#pylightnix.core.config_promises)
    * [assert\_store\_initialized](#pylightnix.core.assert_store_initialized)
    * [store\_initialize](#pylightnix.core.store_initialize)
    * [store\_dref2path](#pylightnix.core.store_dref2path)
    * [rref2path](#pylightnix.core.rref2path)
    * [mkrefpath](#pylightnix.core.mkrefpath)
    * [store\_config\_](#pylightnix.core.store_config_)
    * [store\_config](#pylightnix.core.store_config)
    * [store\_context](#pylightnix.core.store_context)
    * [store\_cattrs](#pylightnix.core.store_cattrs)
    * [store\_deps](#pylightnix.core.store_deps)
    * [store\_deepdeps](#pylightnix.core.store_deepdeps)
    * [store\_deepdepRrefs](#pylightnix.core.store_deepdepRrefs)
    * [store\_drefs](#pylightnix.core.store_drefs)
    * [store\_rrefs\_](#pylightnix.core.store_rrefs_)
    * [store\_rrefs](#pylightnix.core.store_rrefs)
    * [store\_deref\_](#pylightnix.core.store_deref_)
    * [store\_deref](#pylightnix.core.store_deref)
    * [store\_gc](#pylightnix.core.store_gc)
    * [store\_instantiate](#pylightnix.core.store_instantiate)
    * [store\_realize](#pylightnix.core.store_realize)
    * [mkbuildargs](#pylightnix.core.mkbuildargs)
    * [mkbuild](#pylightnix.core.mkbuild)
    * [B](#pylightnix.core.B)
    * [build\_wrapper\_](#pylightnix.core.build_wrapper_)
    * [build\_wrapper](#pylightnix.core.build_wrapper)
    * [build\_config](#pylightnix.core.build_config)
    * [build\_context](#pylightnix.core.build_context)
    * [build\_cattrs](#pylightnix.core.build_cattrs)
    * [build\_outpaths](#pylightnix.core.build_outpaths)
    * [build\_outpath](#pylightnix.core.build_outpath)
    * [build\_name](#pylightnix.core.build_name)
    * [build\_deref\_](#pylightnix.core.build_deref_)
    * [build\_deref](#pylightnix.core.build_deref)
    * [build\_paths](#pylightnix.core.build_paths)
    * [build\_path](#pylightnix.core.build_path)
    * [mkcontext](#pylightnix.core.mkcontext)
    * [context\_eq](#pylightnix.core.context_eq)
    * [context\_add](#pylightnix.core.context_add)
    * [context\_deref](#pylightnix.core.context_deref)
    * [context\_serialize](#pylightnix.core.context_serialize)
    * [promise](#pylightnix.core.promise)
    * [assert\_promise\_fulfilled](#pylightnix.core.assert_promise_fulfilled)
    * [mkdrv](#pylightnix.core.mkdrv)
    * [recursion\_manager](#pylightnix.core.recursion_manager)
    * [instantiate\_](#pylightnix.core.instantiate_)
    * [instantiate](#pylightnix.core.instantiate)
    * [RealizeSeqGen](#pylightnix.core.RealizeSeqGen)
    * [realize](#pylightnix.core.realize)
    * [realizeMany](#pylightnix.core.realizeMany)
    * [realizeSeq](#pylightnix.core.realizeSeq)
    * [mksymlink](#pylightnix.core.mksymlink)
    * [match](#pylightnix.core.match)
    * [latest](#pylightnix.core.latest)
    * [exact](#pylightnix.core.exact)
    * [best](#pylightnix.core.best)
    * [texthash](#pylightnix.core.texthash)
    * [match\_n](#pylightnix.core.match_n)
    * [match\_latest](#pylightnix.core.match_latest)
    * [match\_best](#pylightnix.core.match_best)
    * [match\_all](#pylightnix.core.match_all)
    * [match\_some](#pylightnix.core.match_some)
    * [match\_only](#pylightnix.core.match_only)
    * [assert\_valid\_refpath](#pylightnix.core.assert_valid_refpath)
    * [assert\_valid\_config](#pylightnix.core.assert_valid_config)
    * [assert\_valid\_name](#pylightnix.core.assert_valid_name)
    * [assert\_valid\_rref](#pylightnix.core.assert_valid_rref)
    * [assert\_valid\_hashpart](#pylightnix.core.assert_valid_hashpart)
    * [assert\_valid\_dref](#pylightnix.core.assert_valid_dref)
    * [assert\_valid\_hash](#pylightnix.core.assert_valid_hash)
    * [assert\_valid\_context](#pylightnix.core.assert_valid_context)
    * [assert\_valid\_closure](#pylightnix.core.assert_valid_closure)
    * [warn\_rref\_deps](#pylightnix.core.warn_rref_deps)
    * [assert\_have\_realizers](#pylightnix.core.assert_have_realizers)
    * [assert\_recursion\_manager\_empty](#pylightnix.core.assert_recursion_manager_empty)
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
    * [lsrref](#pylightnix.bashlike.lsrref)
    * [lsref](#pylightnix.bashlike.lsref)
    * [catrref\_](#pylightnix.bashlike.catrref_)
    * [catref](#pylightnix.bashlike.catref)
    * [rmref](#pylightnix.bashlike.rmref)
    * [shellref](#pylightnix.bashlike.shellref)
    * [shell](#pylightnix.bashlike.shell)
    * [du](#pylightnix.bashlike.du)

<a name="pylightnix.types"></a>
# `pylightnix.types`

Main types used in Pylightnix are defined here.

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
reference](#pylightnix.types.RRef) by either dereferencing (that is by
querying for existing realizations) or by
[realizing](#pylightnix.core.realize) it from scratch.

- For derefencing dependencies at the build time, see
  [build_deref](#pylightnix.core.build_deref).
- For querying the storage, see [store_deref](#pylightnix.core.store_deref).

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
## `RefPath`

```python
RefPath = List[Any]
```

RefPath is an alias for Python list (of strings). The first item of
`RefPath` is a [derivation reference](#pylightnix.types.DRef). Other
elements are to represent parts of file path.
RefPath is designed to be used in a stage config where they typically refer
to artifacts of already existing dependencies. To refer to future artifacts of
the derivation being configured, use
[PromisePaths](#pylightnix.types.PromisePath).

To convert `RefPath` into a [system path](#pylightnix.types.Path), one
generally have to perform the following basic actions:

1. Dereference it's first item to obtain the realization. See
[store_deref](#pylightnix.core.store_deref) or
[build_deref](#pylightnix.core.build_deref).
2. Convert the realization reference into system path with
[rref2path](#pylightnix.core.rref2path)
3.  Join the system path with `[1:]` part of RefPath to get the real filename.

The algorithm described above is implemented as
[build_path](#pylightnix.core.build_path) helper function.

<a name="pylightnix.types.PYLIGHTNIX_PROMISE_TAG"></a>
## `PYLIGHTNIX_PROMISE_TAG`

```python
PYLIGHTNIX_PROMISE_TAG = "__promise__"
```

*Do not change!*
A tag to mark the start of [PromisePaths](#pylightnix.types.PromisePath).

<a name="pylightnix.types.PromisePath"></a>
## `PromisePath`

```python
PromisePath = List[Any]
```

PromisePath is an alias for Python list of strings. The first item is a
special tag (the [promise](#pylightnix.core.promise)) and the subsequent
items should represent a file or directory path parts. PromisePaths are to
be used in [Configs](#pylightnix.types.Config). They typically represent
paths to the artifacts which we promise will be created by the derivation
being currently configured.

PromisePaths do exist only at the time of instantiation. Pylightnix converts
them into [RefPath](#pylightnix.types.RefPath) before the realization
starts.

<a name="pylightnix.types.Context"></a>
## `Context`

```python
Context = Dict[DRef,List[RRef]]
```

Context type is an alias for Python dict which maps
[DRefs](#pylightnix.types.DRef) into one or many
[RRefs](#pylightnix.types.RRef).

For any derivation, Context stores a mapping from it's dependency's
derivations to realizations.

<a name="pylightnix.types.Matcher"></a>
## `Matcher`

```python
Matcher = Callable[[DRef,Context],Optional[List[RRef]]]
```

Matcher is a type of user-defined functions which select required
realizations from the set of all available. Matchers also may ask the caller
to build new realizations by returning None.

There are certain rules for matchers:

- Matchers should be **pure**. It's output should depend only on the existing
build artifacts of available realizations.
- Matchers should be **satisfiable** by the their realizaitons. If
matcher returns None, the core calls realizer and re-run the matcher only
once.

Matchers may return an empty list instructs Pylightnix to leave it's
derivation without realizations.

<a name="pylightnix.types.Realizer"></a>
## `Realizer`

```python
Realizer = Callable[[DRef,Context],List[Path]]
```

Realizer is a type of user-defined functions implementing the
[realization](#pylightnix.core.realize) of derivation in a given
[context](#pylightnix.types.Context).

Realizer accepts the following arguments:
- Derivation reference to build the realizations of
- A Context encoding the result of dependency resolution.

Realizer should return one or many system paths of output folders containing
realization artifacts. Those folders will be destroyed (moved) by the core at
the final stage of realization. [Build](#pylightnix.types.Build) helper
objects may be used for simplified output path management and dependency
access.

<a name="pylightnix.types.Derivation"></a>
## `Derivation`

```python
Derivation = NamedTuple('Derivation', [('dref',DRef), ('matcher',Matcher), ('realizer',Realizer) ])
```

Derivation is the core type of Pylightnix. It keeps all the information about
a stage: it's [configuration](#pylightnix.types.Config), how to
[realize](#pylightnix.core.realize) it and how to make a selection among
multiple realizations. Information is stored partly on disk (in the
storage), partly in memory in form of Python code.

<a name="pylightnix.types.Closure"></a>
## `Closure`

```python
Closure = NamedTuple('Closure', [('dref',DRef),('derivations',List[Derivation])])
```

Closure is a named tuple, encoding a reference to derivation, the list of
it's dependencies, plus maybe some additional derivations. So the closure is
complete set of dependencies but not necessary minimal.

Closure is typically obtained as a result of the call to
[instantiate](#pylightnix.core.instantiate) and is typically consumed by the
call to [realizeMany](#pylightnix.core.realizeMany) or it's analogs.

<a name="pylightnix.types.Config"></a>
## `Config` Objects

```python
def __init__(self, d: dict)
```

Config is a JSON-serializable set of user-defined attributes of Pylightnix
node. Typically, configs should determine node's realization process.

`Config` should match the requirements of `assert_valid_config`. Typically,
it's `__dict__` should contain JSON-serializable types only: strings, string
aliases such as [DRefs](#pylightnix.types.DRef), bools, ints, floats, lists or
other dicts. No bytes, `numpy.float32` or lambdas are allowed. Tuples are also
forbidden because they are not preserved (decoded into lists).

Some fields of a config have a special meaning for Pylightnix:

* The field named `name` should be a short readable name. It is used to name
  the Derivation. See `assert_valid_name`.
* Fields of type [RefPath](#pylightnix.types.RefPath) represent the paths to
  the dependency' artifacts
* Fields of type [PromisePath](#pylightnix.types.PromisePath) represent
  future paths which are to be produced during the current stage's realization.
* Values of type [DRef](#pylightnix.types.DRef) encode dependencies.
  Pylightnix scans configs to collect such values and plan the order of
  realizaitons.
* Values of type [RRef](#pylightnix.types.RRef) lead to warning. Placing such
  values into a config is probably an error: Pylightnix can't know how to
  produce exactly this reference and so it can't produce a continuous
  realization plan.

Example:
```python
def mystage(m:Manager)->Dref:
  def _config():
    name = 'mystage'
    nepoches = 4
    learning_rate = 1e-5
    hidden_size = 128
    return mkconfig(locals())
  return mkdrv(_config(),...)
```

<a name="pylightnix.types.Config.__init__"></a>
### `Config.__init__()`

```python
def __init__(self, d: dict)
```


<a name="pylightnix.types.Config.__repr__"></a>
### `Config.__repr__()`

```python
def __repr__(self) -> str
```


<a name="pylightnix.types.ConfigAttrs"></a>
## `ConfigAttrs` Objects

```python
def __init__(self, d: dict)
```

`ConfigAttrs` is a helper object allowing to access
[Config](#pylightnix.types.Config) fields as Python object attributes

<a name="pylightnix.types.ConfigAttrs.__init__"></a>
### `ConfigAttrs.__init__()`

```python
def __init__(self, d: dict)
```


<a name="pylightnix.types.BuildArgs"></a>
## `BuildArgs`

```python
BuildArgs = NamedTuple('BuildArgs', [('dref',DRef), ('cattrs',ConfigAttrs),
                                     ...
```


<a name="pylightnix.types.Build"></a>
## `Build` Objects

```python
def __init__(self, ba: BuildArgs) -> None
```

Build is a helper object which tracks the process of stage's
[realization](#pylightnix.core.realize).

We encode typical build operations in the following associated functions:

- [build_config](#pylightnix.core.build_config) - Obtain the Config object of
  the current stage
- [build_cattrs](#pylightnix.core.build_cattrs) - Obtain the ConfigAttrs helper
- [build_path](#pylightnix.core.build_path) - Convert a RefPath or a PromisePath
  into a system file path
- [build_outpath](#pylightnix.core.build_outpath) - Create and return the output path.
- [build_deref](#pylightnix.core.build_deref) - Convert a dependency DRef
  into a realization reference.

<a name="pylightnix.types.Build.__init__"></a>
### `Build.__init__()`

```python
def __init__(self, ba: BuildArgs) -> None
```


<a name="pylightnix.types.Manager"></a>
## `Manager` Objects

```python
def __init__(self)
```

The derivation manager is a mutable storage where we store derivations
before combining them into a [Closure](#pylightnix.types.Closure).

Manager doesn't have any associated user-level operations. It is typically a
first argument of stage functions which should be passed downstream without
modifications.

The [inplace module](#pylightnix.inplace) defines it's own [global derivation
manager](#pylightnix.inplace.PYLIGHTNIX_MANAGER) to simplify the usage even
more.

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


<a name="pylightnix.types.Key"></a>
## `Key`

```python
Key = Callable[[RRef],Optional[Union[int,float,str]]]
```


<a name="pylightnix.core"></a>
# `pylightnix.core`

Core Pylightnix definitions

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


<a name="pylightnix.core.config_cattrs"></a>
## `config_cattrs()`

```python
def config_cattrs(c: Config) -> Any
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
def config_deps(c: Config) -> Set[DRef]
```


<a name="pylightnix.core.config_substitutePromises"></a>
## `config_substitutePromises()`

```python
def config_substitutePromises(c: Config, r: DRef) -> Config
```

Replace all Promise tags with DRef `r`. In particular, all PromisePaths
are converted into RefPaths.

<a name="pylightnix.core.config_promises"></a>
## `config_promises()`

```python
def config_promises(c: Config, r: DRef) -> List[Tuple[str,RefPath]]
```


<a name="pylightnix.core.assert_store_initialized"></a>
## `assert_store_initialized()`

```python
def assert_store_initialized() -> None
```


<a name="pylightnix.core.store_initialize"></a>
## `store_initialize()`

```python
def store_initialize(custom_store: Optional[str] = None, custom_tmp: Optional[str] = None, check_not_exist: bool = False) -> None
```

Create the storage and temp direcories if they don't exist. Default
locations are determined by `PYLIGHTNIX_STORE` and `PYLIGHTNIX_TMP` global
variables which in turn may be set by either setting environment variables of
the same name or by direct assigning.

Parameters:
- `custom_store`: If not None, create new storage located here.
- `custom_tmp`: If not None, set the temp files directory here.
- `check_not_exist`: Set to True to assert on already existing storages

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

Construct a [RefPath](#pylightnix.types.RefPath) out of a reference `ref`
and a path within the stage's realization

<a name="pylightnix.core.store_config_"></a>
## `store_config_()`

```python
def store_config_(r: DRef) -> Config
```


<a name="pylightnix.core.store_config"></a>
## `store_config()`

```python
def store_config(r: Union[DRef,RRef]) -> Config
```

Read the [Config](#pylightnix.types.Config) of the derivatoin referenced by `r`.

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

Read the [ConfigAttrs](#pylightnix.types.ConfigAttr) of the storage node `r`.
Note, that it is a kind of 'syntactic sugar' for `store_config`. Both
functions do the same thing.

<a name="pylightnix.core.store_deps"></a>
## `store_deps()`

```python
def store_deps(drefs: Iterable[DRef]) -> Set[DRef]
```

Return a list of reference's immediate dependencies, not including `refs`
themselves.

<a name="pylightnix.core.store_deepdeps"></a>
## `store_deepdeps()`

```python
def store_deepdeps(roots: Iterable[DRef]) -> Set[DRef]
```

Return the complete set of `roots`'s dependencies, not including `roots`
themselves.

<a name="pylightnix.core.store_deepdepRrefs"></a>
## `store_deepdepRrefs()`

```python
def store_deepdepRrefs(roots: Iterable[RRef]) -> Set[RRef]
```

Return the complete set of root's dependencies, not including `roots`
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

Iterate over realizations of a derivation `dref`, which match a
[context](#pylightnix.types.Context). The sort order is unspecified.

<a name="pylightnix.core.store_deref_"></a>
## `store_deref_()`

```python
def store_deref_(context_holder: RRef, dref: DRef) -> List[RRef]
```


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
def store_gc(keep_drefs_: List[DRef], keep_rrefs_: List[RRef]) -> Tuple[Set[DRef],Set[RRef]]
```

Take roots which are in use and should not be removed. Return roots which
are not used and may be removed. Actual removing is to be done by the user.

See also [rmref](#pylightnix.bashlike.rmref)

<a name="pylightnix.core.store_instantiate"></a>
## `store_instantiate()`

```python
def store_instantiate(c: Config) -> DRef
```

Place new instantiation into the storage. We attempt to do it atomically
by moving the directory right into it's place.

FIXME: Assert or handle possible (but improbable) hash collision (*)

<a name="pylightnix.core.store_realize"></a>
## `store_realize()`

```python
def store_realize(dref: DRef, l: Context, o: Path) -> RRef
```

FIXME: Assert or handle possible but improbable hash collision (*)

<a name="pylightnix.core.mkbuildargs"></a>
## `mkbuildargs()`

```python
def mkbuildargs(dref: DRef, context: Context, buildtime: bool = True) -> BuildArgs
```


<a name="pylightnix.core.mkbuild"></a>
## `mkbuild()`

```python
def mkbuild(dref: DRef, context: Context, buildtime: bool = True) -> Build
```


<a name="pylightnix.core.B"></a>
## `B`

```python
B = TypeVar('B')
```


<a name="pylightnix.core.build_wrapper_"></a>
## `build_wrapper_()`

```python
def build_wrapper_(f: Callable[[B],None], ctr: Callable[[BuildArgs],B], buildtime: bool = True) -> Realizer
```


<a name="pylightnix.core.build_wrapper"></a>
## `build_wrapper()`

```python
def build_wrapper(f: Callable[[Build],None], buildtime: bool = True)
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
def build_cattrs(b: Build) -> Any
```


<a name="pylightnix.core.build_outpaths"></a>
## `build_outpaths()`

```python
def build_outpaths(b: Build, nouts: int = 1) -> List[Path]
```


<a name="pylightnix.core.build_outpath"></a>
## `build_outpath()`

```python
def build_outpath(b: Build) -> Path
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

<a name="pylightnix.core.build_deref_"></a>
## `build_deref_()`

```python
def build_deref_(b: Build, dref: DRef) -> List[RRef]
```

For any [realization](#pylightnix.core.realize) process described with
it's [Build](#pylightnix.types.Build) handler, `build_deref` queries a
realization of dependency `dref`.

`build_deref` is designed to be called from
[Realizer](#pylightnix.types.Realizer) functions. In other cases,
[store_deref](#pylightnix.core.store_deref) should be used.

<a name="pylightnix.core.build_deref"></a>
## `build_deref()`

```python
def build_deref(b: Build, dref: DRef) -> RRef
```


<a name="pylightnix.core.build_paths"></a>
## `build_paths()`

```python
def build_paths(b: Build, refpath: RefPath) -> List[Path]
```

Convert given [RefPath](#pylightnix.types.RefPath) (which may be an
ex-[PromisePath](#pylightnix.types.PromisePath)) into a set of filesystem
paths. Conversion refers to the [Context](#pylightnix.types.Context) of the
realization, as specified by the `b` helper.

Typically, we configure stages to match only one realization at once, so the
returned list is often a singleton list. See
[build_path](#pylightnix.core.build_path).

Example:
```python
def config(dep:DRef)->Config:
  name = 'example-stage'
  input = [dep,"path","to","input.txt"]
  output = [promise,"output.txt"]
  some_param = 42
  return mkconfig(locals())

def realize(b:Build)->None:
  c=config_cattrs(b)
  with open(build_path(b, c.input),'r') as finp:
    with open(build_path(b, c.output),'w') as fout:
      fout.write(finp.read())

def mystage(m:Manager)->DRef:
  dep:DRef=otherstage(m)
  return mkdrv(m, config(dep), match_only(), build_wrapper(realize))
```

<a name="pylightnix.core.build_path"></a>
## `build_path()`

```python
def build_path(b: Build, refpath: RefPath) -> Path
```

A single-realization version of the [build_paths](#pylightnix.core.build_paths).

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
def context_add(context: Context, dref: DRef, rrefs: List[RRef]) -> Context
```


<a name="pylightnix.core.context_deref"></a>
## `context_deref()`

```python
def context_deref(context: Context, dref: DRef) -> List[RRef]
```


<a name="pylightnix.core.context_serialize"></a>
## `context_serialize()`

```python
def context_serialize(c: Context) -> str
```


<a name="pylightnix.core.promise"></a>
## `promise`

```python
promise = PYLIGHTNIX_PROMISE_TAG
```

Used to create [PromisePath](#pylightnix.types.PromisePath) as a start
marker. Promise paths exist only during
[instantiation](#pylightnix.core.instantiate). Before the realization, the
core replaces all PromisePaths with the corresponding
[RefPaths](#pylightnix.type.RefPath) automatically (see
[store_config](#pylightnix.core.store_config)).

Converted RefPaths may be converted into filesystem paths by
[build_path](#pylightnix.core.build_path) as ususal.

Example:
```python
def hello_builder_config()->Config:
promise_binary = [promise, 'usr','bin','hello']
return mkconfig(locals())
dref=mkdrv(..., config=hello_builder_config(), ...)
```

<a name="pylightnix.core.assert_promise_fulfilled"></a>
## `assert_promise_fulfilled()`

```python
def assert_promise_fulfilled(k: str, p: RefPath, o: Path) -> None
```


<a name="pylightnix.core.mkdrv"></a>
## `mkdrv()`

```python
def mkdrv(m: Manager, config: Config, matcher: Matcher, realizer: Realizer, check_promises: bool = True) -> DRef
```

Run the instantiation of a particular stage. Create a
[Derivation](#pylightnix.types.Derivation) object of out of three main
components: the Derivation reference, the Matcher and the Realizer. Register
the derivation in a [Manager](#pylightnix.types.Manager) to aid dependency
resolution. Return [Derivation reference](#pylightnix.types.DRef) of the
derivation produced.

Arguments:
- `check_promises:bool=True`: Make sure that all
  [PromisePath](#pylightnix.types.PromisePaths) of stage's configuration
  correspond to existing files or firectories.

Example:
```python
def somestage(m:Manager)->DRef:
  def _realizer(b:Build):
    with open(join(build_outpath(b),'artifact'),'w') as f:
      f.write(...)
  return mkdrv(m,mkconfig({'name':'mystage'}), match_only(), build_wrapper(_realizer))

rref:RRef=realize(instantiate(somestage))
```

<a name="pylightnix.core.recursion_manager"></a>
## `recursion_manager()`

```python
@contextmanager
def recursion_manager(funcname: str)
```

Recursion manager is a helper context manager which detects and prevents
unwanted recursions. Currently, the following kinds of recursions are catched:

- `instantiate() -> <config> -> instantiate()`. Instantiate stores Derivation
  in Manager and returns a DRef as a proof that given Manager contains given
  Derivation. Recursive call to instantiate would break this idea by
  introducing nested Managers.
- `realize() -> <realizer> -> realize()`. Sometimes this recursion is OK,
  but in some cases it may lead to infinite loop, so we deny it completely for now.
- `realize() -> <realizer> -> instantiate()`. Instantiate produces new DRefs,
  while realize should only work with existing DRefs which form a Closure.

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

Instantiate takes the [Stage](#pylightnix.types.Stage) function and
calculates the [Closure](#pylightnix.types.Closure) of it's
[Derivations](#pylightnix.types.Derivation).
All new derivations are added to the storage.
See also [realizeMany](#pylightnix.core.realizeMany)

<a name="pylightnix.core.RealizeSeqGen"></a>
## `RealizeSeqGen`

```python
RealizeSeqGen = Generator[Tuple[DRef,Context,Derivation],Tuple[Optional[List[RRef]],bool],List[RRef]]
```


<a name="pylightnix.core.realize"></a>
## `realize()`

```python
def realize(closure: Closure, force_rebuild: Union[List[DRef],bool] = []) -> RRef
```

A simplified version of [realizeMany](#pylightnix.core.realizeMany).
Expects only one output path.

<a name="pylightnix.core.realizeMany"></a>
## `realizeMany()`

```python
def realizeMany(closure: Closure, force_rebuild: Union[List[DRef],bool] = []) -> List[RRef]
```

Obtain one or more realizations of a stage's
[Closure](#pylightnix.types.Closure).

If [matching](#pylightnix.types.Matcher) realizations do exist in the
storage, and if user doesn't ask to forcebly rebuild the stage, `realizeMany`
returns the references immediately.

Otherwize, it calls [Realizers](#pylightnix.types.Realizer) of the Closure to
get desired realizations of the closure top-level derivation.

Returned value is a list realization references
[realizations](#pylightnix.types.RRef). Every RRef may be [converted
to system path](#pylightnix.core.rref2path) of the folder which
contains build artifacts.

In order to create each realization, realizeMany moves it's build artifacts
into the storage by executing `os.replace` function which are assumed to be
atomic. `realizeMany` also assumes that derivation's config is present in the
storage at this moment (See e.g. [rmref](#pylightnix.bashlike.rmref))

Example:
```python
def mystage(m:Manager)->DRef:
  ...
  return mkdrv(m, ...)

clo:Closure=instantiate(mystage)
rrefs:List[RRef]=realizeMany(clo)
print('Available realizations:', [rref2path(rref) for rref in rrefs])
```

`realizeMany` has the following analogs:

* [realize](#pylightnix.core.realize) - A single-output version
* [repl_realize](#pylightnix.repl.repl_realize) - A REPL-friendly version
* [realize_inplace](#pylightnix.inplace.realize_inplace) - A simplified
  version which uses a global derivation Manager.

- FIXME: Stage's context is calculated inefficiently. Maybe one should track
  dep.tree to avoid calling `store_deepdeps` within the cycle.
- FIXME: Update derivation's matcher after forced rebuilds. Matchers should
  remember and reproduce user's preferences.

<a name="pylightnix.core.realizeSeq"></a>
## `realizeSeq()`

```python
def realizeSeq(closure: Closure, force_interrupt: List[DRef] = []) -> RealizeSeqGen
```

Sequentially realize the closure by issuing steps via Python's generator
interface. `realizeSeq` encodes low-level details of the realization
algorithm. Consider calling [realizeMany](#pylightnix.core.realizeMany) or
it's analogs instead.

<a name="pylightnix.core.mksymlink"></a>
## `mksymlink()`

```python
def mksymlink(rref: RRef, tgtpath: Path, name: str, withtime=True) -> Path
```

Create a symlink pointing to realization `rref`. Other arguments define
symlink name and location. Informally,
`{tgtpath}/{timeprefix}{name} --> $PYLIGHTNIX_STORE/{rref2dref(rref)}/{rref}`

<a name="pylightnix.core.match"></a>
## `match()`

```python
def match(keys: List[Key], rmin: Optional[int] = 1, rmax: Optional[int] = 1, exclusive: bool = False) -> Matcher
```

Create a matcher by combining different sorting keys and selecting a
top-n threshold.

Arguments:
- `keys`: List of [Key](#pylightnix.types.Key) functions. Defaults ot
- `rmin`: An integer selecting the minimum number of realizations to accept.
  If non-None, Realizer is expected to produce at least this number of
  realizations.
- `rmax`: An integer selecting the maximum number of realizations to return
  (realizer is free to produce more realizations)
- `exclusive`: If true, asserts if the number of realizations exceeds `rmax`

<a name="pylightnix.core.latest"></a>
## `latest()`

```python
def latest() -> Key
```


<a name="pylightnix.core.exact"></a>
## `exact()`

```python
def exact(expected: List[RRef]) -> Key
```


<a name="pylightnix.core.best"></a>
## `best()`

```python
def best(filename: str) -> Key
```


<a name="pylightnix.core.texthash"></a>
## `texthash()`

```python
def texthash() -> Key
```


<a name="pylightnix.core.match_n"></a>
## `match_n()`

```python
def match_n(n: int = 1, keys=[]) -> Matcher
```

Return a [Matcher](#pylightnix.types.Matcher) which matchs with any
number of realizations which is greater or equal than `n`.

<a name="pylightnix.core.match_latest"></a>
## `match_latest()`

```python
def match_latest(n: int = 1) -> Matcher
```


<a name="pylightnix.core.match_best"></a>
## `match_best()`

```python
def match_best(filename: str, n: int = 1) -> Matcher
```

Return a [Matcher](#pylightnix.types.Matcher) which checks contexts of
realizations and then compares them based on stage-specific scores. For each
realization, score is read from artifact file named `filename` that should
contain a single float number. Realization with largest score wins.

<a name="pylightnix.core.match_all"></a>
## `match_all()`

```python
def match_all() -> Matcher
```

Return a [Matcher](#pylightnix.types.Matcher) which matchs with **ANY**
number of realizations, including zero.

<a name="pylightnix.core.match_some"></a>
## `match_some()`

```python
def match_some(n: int = 1) -> Matcher
```

Return a [Matcher](#pylightnix.types.Matcher) which matchs with any
number of realizations which is greater or equal than `n`.

<a name="pylightnix.core.match_only"></a>
## `match_only()`

```python
def match_only() -> Matcher
```

Return a [Matcher](#pylightnix.types.Matcher) which expects no more than
one realization for every [derivation](#pylightnix.types.DRef), given the
[context](#pylightnix.types.Context).

<a name="pylightnix.core.assert_valid_refpath"></a>
## `assert_valid_refpath()`

```python
def assert_valid_refpath(refpath: RefPath) -> None
```


<a name="pylightnix.core.assert_valid_config"></a>
## `assert_valid_config()`

```python
def assert_valid_config(c: Config) -> Config
```


<a name="pylightnix.core.assert_valid_name"></a>
## `assert_valid_name()`

```python
def assert_valid_name(s: Name) -> None
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


<a name="pylightnix.core.warn_rref_deps"></a>
## `warn_rref_deps()`

```python
def warn_rref_deps(c: Config) -> None
```


<a name="pylightnix.core.assert_have_realizers"></a>
## `assert_have_realizers()`

```python
def assert_have_realizers(m: Manager, drefs: List[DRef]) -> None
```


<a name="pylightnix.core.assert_recursion_manager_empty"></a>
## `assert_recursion_manager_empty()`

```python
def assert_recursion_manager_empty()
```


<a name="pylightnix.inplace"></a>
# `pylightnix.inplace`

This module defines inplace variants of `instantiate` and `realize`.
Inplace functions use a single global [Manager](#pylightnix.types.Manager)
which is easier to use but has usual risks of gloabl variables.

<a name="pylightnix.inplace.PYLIGHTNIX_MANAGER"></a>
## `PYLIGHTNIX_MANAGER`

```python
PYLIGHTNIX_MANAGER = Manager()
```

The Global [Derivation manager](#pylightnix.types.Manager) used by
`instantiate_inplace` and `realize_inplace` functions.

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

Trivial builtin stages

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

Builtin stages for fetching things from the Internet

<a name="pylightnix.stages.fetch.WGET"></a>
## `WGET`

```python
WGET = try_executable('wget', 'Please install `wget` pacakge.')
```


<a name="pylightnix.stages.fetch.AUNPACK"></a>
## `AUNPACK`

```python
AUNPACK = try_executable('aunpack', 'Please install `apack` tool from `atool` package.')
```


<a name="pylightnix.stages.fetch.fetchurl"></a>
## `fetchurl()`

```python
def fetchurl(m: Manager, url: str, sha256: str, mode: str = 'unpack,remove', name: Optional[str] = None, filename: Optional[str] = None, force_download: bool = False) -> DRef
```

Download and unpack an URL addess.

Downloading is done by calling `wget` application. Optional unpacking is
performed with the `aunpack` script from `atool` package. `sha256` defines the
expected SHA-256 hashsum of the stored data. `mode` allows to tweak the
stage's behavior: adding word 'unpack' instructs fetchurl to unpack the
package, adding 'remove' instructs it to remove the archive after unpacking.

Agruments:
- `m:Manager` the dependency resolving manager of Pylightnix. Provided by
  `instantiate`
- `url:str` URL to download from. Should point to a single file.
- `sha256:str` SHA-256 hash sum of the file.
- `model:str` Additional options. Format: `[unpack[,remove]]`.
- `name:Optional[str]`: Name of the Derivation. The stage will attempt to
  deduce the name if not specified.
- `filename:Optional[str]` Name of the filename on disk after downloading.
  Stage will attempt to deduced it if not specified.
- `force_download:bool` If False (the default), resume the last download if
  possible.

<a name="pylightnix.bashlike"></a>
# `pylightnix.bashlike`

Simple functions imitating unix shell tools.

<a name="pylightnix.bashlike.lsdref_"></a>
## `lsdref_()`

```python
def lsdref_(r: DRef) -> Iterable[str]
```


<a name="pylightnix.bashlike.lsrref_"></a>
## `lsrref_()`

```python
def lsrref_(r: RRef, fn: List[str] = []) -> Iterable[str]
```


<a name="pylightnix.bashlike.lsrref"></a>
## `lsrref()`

```python
def lsrref(r: RRef, fn: List[str] = []) -> List[str]
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

<a name="pylightnix.bashlike.rmref"></a>
## `rmref()`

```python
def rmref(r: Union[RRef,DRef]) -> None
```

Forcebly remove a reference from the storage. Removing
[DRefs](#pylightnix.types.DRef) also removes all their realizations.

Currently Pylightnix makes no attempts to synchronize an access to the
storage. In scenarious involving parallelization, users are expected to take
care of possible race conditions.

<a name="pylightnix.bashlike.shellref"></a>
## `shellref()`

```python
def shellref(r: Union[RRef,DRef,None] = None) -> None
```

Alias for [shell](#pylightnix.bashlike.shell)

<a name="pylightnix.bashlike.shell"></a>
## `shell()`

```python
def shell(r: Union[RRef,DRef,Path,str,None] = None) -> None
```

Open the directory corresponding to `r` in Unix Shell for inspection. The
path to shell executable is read from the `SHELL` environment variable,
defaulting to `/bin/sh`. If `r` is None, open the shell in the root of the
storage.

<a name="pylightnix.bashlike.du"></a>
## `du()`

```python
def du() -> Dict[DRef,Tuple[int,Dict[RRef,int]]]
```

Calculates the disk usage, in bytes. For every derivation, return it's
total disk usage and disk usages per realizations. Note, that total disk usage
of a derivation is slightly bigger than sum of it's realization's usages.

