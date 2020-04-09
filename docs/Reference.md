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
    * [PYLIGHTNIX\_CLAIM\_TAG](#pylightnix.types.PYLIGHTNIX_CLAIM_TAG)
    * [PromisePath](#pylightnix.types.PromisePath)
    * [Context](#pylightnix.types.Context)
    * [Matcher](#pylightnix.types.Matcher)
    * [InstantiateArg](#pylightnix.types.InstantiateArg)
    * [RealizeArg](#pylightnix.types.RealizeArg)
    * [Realizer](#pylightnix.types.Realizer)
    * [Derivation](#pylightnix.types.Derivation)
    * [Closure](#pylightnix.types.Closure)
    * [Config](#pylightnix.types.Config)
    * [RConfig](#pylightnix.types.RConfig)
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
    * [path2rref](#pylightnix.core.path2rref)
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
    * [store\_cfgpath](#pylightnix.core.store_cfgpath)
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
    * [store\_buildtime](#pylightnix.core.store_buildtime)
    * [store\_gc](#pylightnix.core.store_gc)
    * [store\_instantiate](#pylightnix.core.store_instantiate)
    * [store\_realize](#pylightnix.core.store_realize)
    * [mkcontext](#pylightnix.core.mkcontext)
    * [context\_eq](#pylightnix.core.context_eq)
    * [context\_add](#pylightnix.core.context_add)
    * [context\_deref](#pylightnix.core.context_deref)
    * [context\_serialize](#pylightnix.core.context_serialize)
    * [promise](#pylightnix.core.promise)
    * [claim](#pylightnix.core.claim)
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
  * [pylightnix.build](#pylightnix.build)
    * [mkbuildargs](#pylightnix.build.mkbuildargs)
    * [mkbuild](#pylightnix.build.mkbuild)
    * [B](#pylightnix.build.B)
    * [build\_wrapper\_](#pylightnix.build.build_wrapper_)
    * [build\_wrapper](#pylightnix.build.build_wrapper)
    * [build\_config](#pylightnix.build.build_config)
    * [build\_context](#pylightnix.build.build_context)
    * [build\_cattrs](#pylightnix.build.build_cattrs)
    * [build\_setoutpaths](#pylightnix.build.build_setoutpaths)
    * [build\_outpaths](#pylightnix.build.build_outpaths)
    * [build\_outpath](#pylightnix.build.build_outpath)
    * [build\_name](#pylightnix.build.build_name)
    * [build\_deref\_](#pylightnix.build.build_deref_)
    * [build\_deref](#pylightnix.build.build_deref)
    * [build\_paths](#pylightnix.build.build_paths)
    * [build\_path](#pylightnix.build.build_path)
  * [pylightnix.inplace](#pylightnix.inplace)
    * [PYLIGHTNIX\_MANAGER](#pylightnix.inplace.PYLIGHTNIX_MANAGER)
    * [instantiate\_inplace](#pylightnix.inplace.instantiate_inplace)
    * [realize\_inplace](#pylightnix.inplace.realize_inplace)
  * [pylightnix.repl](#pylightnix.repl)
    * [ReplHelper](#pylightnix.repl.ReplHelper)
    * [ERR\_INVALID\_RH](#pylightnix.repl.ERR_INVALID_RH)
    * [ERR\_INACTIVE\_RH](#pylightnix.repl.ERR_INACTIVE_RH)
    * [repl\_continueMany](#pylightnix.repl.repl_continueMany)
    * [repl\_continue](#pylightnix.repl.repl_continue)
    * [repl\_continueBuild](#pylightnix.repl.repl_continueBuild)
    * [repl\_realize](#pylightnix.repl.repl_realize)
    * [repl\_rrefs](#pylightnix.repl.repl_rrefs)
    * [repl\_rref](#pylightnix.repl.repl_rref)
    * [repl\_buildargs](#pylightnix.repl.repl_buildargs)
    * [repl\_build](#pylightnix.repl.repl_build)
    * [repl\_cancel](#pylightnix.repl.repl_cancel)
    * [repl\_cancelBuild](#pylightnix.repl.repl_cancelBuild)
  * [pylightnix.stages](#pylightnix.stages)
  * [pylightnix.stages.trivial](#pylightnix.stages.trivial)
    * [mknode](#pylightnix.stages.trivial.mknode)
    * [mkfile](#pylightnix.stages.trivial.mkfile)
    * [checkpaths](#pylightnix.stages.trivial.checkpaths)
    * [redefine](#pylightnix.stages.trivial.redefine)
    * [realized](#pylightnix.stages.trivial.realized)
  * [pylightnix.stages.fetch](#pylightnix.stages.fetch)
    * [WGET](#pylightnix.stages.fetch.WGET)
    * [AUNPACK](#pylightnix.stages.fetch.AUNPACK)
    * [\_unpack](#pylightnix.stages.fetch._unpack)
    * [fetchurl](#pylightnix.stages.fetch.fetchurl)
    * [fetchlocal](#pylightnix.stages.fetch.fetchlocal)
  * [pylightnix.bashlike](#pylightnix.bashlike)
    * [lsdref\_](#pylightnix.bashlike.lsdref_)
    * [lsrref\_](#pylightnix.bashlike.lsrref_)
    * [lsrref](#pylightnix.bashlike.lsrref)
    * [lsref](#pylightnix.bashlike.lsref)
    * [catrref\_](#pylightnix.bashlike.catrref_)
    * [catref](#pylightnix.bashlike.catref)
    * [rmref](#pylightnix.bashlike.rmref)
    * [shell](#pylightnix.bashlike.shell)
    * [shellref](#pylightnix.bashlike.shellref)
    * [du](#pylightnix.bashlike.du)
    * [find](#pylightnix.bashlike.find)
    * [diff](#pylightnix.bashlike.diff)
  * [pylightnix.lens](#pylightnix.lens)
    * [Lens](#pylightnix.lens.Lens)
    * [mklens](#pylightnix.lens.mklens)

<a name="pylightnix.types"></a>
# `pylightnix.types`

All main types which we use in Pylightnix are defined here.

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
- `<HashPart>` contains first 32 characters of derivation `RConfig`'s sha256
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

<a name="pylightnix.types.PYLIGHTNIX_CLAIM_TAG"></a>
## `PYLIGHTNIX_CLAIM_TAG`

```python
PYLIGHTNIX_CLAIM_TAG = "__claim__"
```

*Do not change!*
A tag to mark the start of [PromisePaths](#pylightnix.types.PromisePath). In
contrast to promises, Pylightnix doesn't check the claims

<a name="pylightnix.types.PromisePath"></a>
## `PromisePath`

```python
PromisePath = List[Any]
```

PromisePath is an alias for Python list of strings. The first item is a
special tag (the [promise](#pylightnix.core.promise) or the
[claim](#pylightnix.core.claim)) and the subsequent
items should represent a file or directory path parts. PromisePaths are
typically fields of [Configs](#pylightnix.types.Config). They represent
paths to the artifacts which we promise will be created by the derivation
being currently configured.

PromisePaths do exist only at the time of instantiation. Pylightnix converts
them into [RefPath](#pylightnix.types.RefPath) before the realization
starts. Converted configs change their type to
[RConfig](#pylightnix.type.RConfig)

Example:
```python
from pylightnix import mkconfig, mkdrv, promise
def myconfig()->Config:
name = "config-of-some-stage"
promise_binary = [promise, 'usr','bin','hello']
other_params = 42
return mkconfig(locals())
dref=mkdrv(..., config=myconfig(), ...)
```

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
realizations from the set of all realizations available.

Matchers take the derivation reference and the context. They may easily
determine the set of existing realizations (see
[store_rrefs](#pylightnix.core.store_rrefs) and should return the subset of
this set or None which is a request to Pylightnix to produce more
realizations.

Matchers should follow the below rules:

- Matchers should be **pure**. It's output should depend only on the existing
build artifacts of available realizations.
- Matchers should be **satisfiable** by realizers of their stages. If matcher
returns None, the core calls realizer and re-run the matcher only once.

Matchers may return an empty list and by that instruct Pylightnix to leave it's
derivation without realizations.

Pylightnix provides a set of built-in matchers:

- [match](#pylightnix.core.match) is a generic matcher with rich sorting and
filtering API.
- [match_n](#pylightnix.core.match_n) is it's version for fixed number of matches
- [match_best](#pylightnix.core.match_best) decision is made based on a named
build artifact
- [match_all](#pylightnix.core.match_all) matches any number of realizations, including zero.
- [match_some](#pylightnix.core.match_some) matches any existing realizations
- [match_only](#pylightnix.core.match_only) matches exactly one existing
realization (asserts if there are more than one realizations)

<a name="pylightnix.types.InstantiateArg"></a>
## `InstantiateArg`

```python
InstantiateArg = Dict[str,Any]
```


<a name="pylightnix.types.RealizeArg"></a>
## `RealizeArg`

```python
RealizeArg = Dict[str,Any]
```


<a name="pylightnix.types.Realizer"></a>
## `Realizer`

```python
Realizer = Callable[[DRef,Context,RealizeArg],List[Path]]
```

Realizer is a type of callback functions which are defined by the user.
Realizers should implement the stage-specific
[realization](#pylightnix.core.realize) algorithm.

Realizer accepts the following arguments:

- [Reference to a Derivation](#pylightnix.types.DRef) being build
- [Context](#pylightnix.types.Context) encoding the results of dependency
resolution.

`DRef` and `Context` allows programmer to access
[Configs](#pylightnix.types.Config) of the current derivation and all it's
dependencies.

Realizers have to return one or many folder paths of realization artifacts
(files and folders containing stage-specific data). Those folders will be
added to the pool of Realizations of the current derivation.
[Matcher](#pylightnix.types.Matcher) will be called to pick some subset of
existing realizations. The chosen subset will eventually appear in the
Contexts of downstream derivations.

Most of the stages defined in Pylightnix use simplified realizer's API
provided by the [Build](#pylightnix.types.Build) helper class. The
[build_wrapper](#pylightnix.core.build_wrapper) function converts realizers
back to standard format.

Example:

```python
def mystage(m:Manager)->DRef:
def _realize(dref:DRef, context:Context)->List[Path]:
b=mkbuild(dref, context, buildtime=buildtime)
with open(join(build_outpath(b),'artifact'),'w') as f:
f.write('chickenpoop\n')
return [build_outpath(b)]
...
return mkdrv(m, ...,  _realize)
```

<a name="pylightnix.types.Derivation"></a>
## `Derivation`

```python
Derivation = NamedTuple('Derivation', [('dref',DRef), ('matcher',Matcher), ('realizer',Realizer) ])
```

Derivation is the core type of Pylightnix. It keeps all the information about
a stage: it's [configuration](#pylightnix.types.Config), how to
[realize](#pylightnix.core.realize) it and how to make a
[selection](#pylightnix.types.Matcher) among multiple realizations.
Information is stored partly on disk (in the Pylightnix storage), partly in
memory in form of Python code.

Derivations normally appear as a result of [mkdrv](#pylightnix.core.mkdrv)
call.

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

Configs should match the requirements of `assert_valid_config`. Typically,
it's `val` dictionary should contain JSON-serializable types only: strings,
string aliases such as [DRefs](#pylightnix.types.DRef), bools, ints, floats,
lists or other dicts. No bytes, `numpy.float32` or lambdas are allowed. Tuples
are also forbidden because they are not preserved (decoded into lists).

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
  values into a config is probably an error: Pylightnix doesn't have a chance to
  know how to produce exactly this reference so it can't produce a continuous
  realization plan.

Example:
```python
def mystage(m:Manager)->Dref:
  def _config()->Config:
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


<a name="pylightnix.types.RConfig"></a>
## `RConfig` Objects

RConfig is a [Config](#pylightnix.types.Config) where all claims and
promises are resolved.

<a name="pylightnix.types.ConfigAttrs"></a>
## `ConfigAttrs` Objects

```python
def __init__(self, d: dict)
```

`ConfigAttrs` is a helper object allowing to access
[RConfig](#pylightnix.types.RConfig) fields as Python object attributes.

DEPRECATED in favour of [Lenses](#pylightnix.lens.Lens).

<a name="pylightnix.types.ConfigAttrs.__init__"></a>
### `ConfigAttrs.__init__()`

```python
def __init__(self, d: dict)
```


<a name="pylightnix.types.BuildArgs"></a>
## `BuildArgs`

```python
BuildArgs = NamedTuple('BuildArgs', [('dref',DRef),
                                     ('context',Context),
   ...
```


<a name="pylightnix.types.Build"></a>
## `Build` Objects

```python
def __init__(self, ba: BuildArgs) -> None
```

Build is a helper object which tracks the process of stage's
[realization](#pylightnix.core.realize). It allows users to define
[Realizers](#pylightnix.types.Realizer) with a simple one-argument signature.
[build_wrapper](#pylightnix.core.build_wrapper) function converts
Build-realizers into regular ones.

We encode typical build operations in the following associated functions:

- [build_config](#pylightnix.core.build_config) - Obtain the RConfig object of
  the current stage
- [build_cattrs](#pylightnix.core.build_cattrs) - Obtain the ConfigAttrs helper
- [build_path](#pylightnix.core.build_path) - Convert a RefPath or a PromisePath
  into a system file path
- [build_outpath](#pylightnix.core.build_outpath) - Create and return the output path.
- [build_deref](#pylightnix.core.build_deref) - Convert a dependency DRef
  into a realization reference.

[Lenses](#pylightnix.lens.Lens) accept `Build` objects as a source of
configuration of derivations being realized.

Build class may be subclassed by applications in order to define
application-specific build-state.  Underscoped
[build_wrapper_](#pylightnix.core.build_wrapper_) accepts additional parameter
which informs the core what subclass to create. Note that derived classes
should have the same constructor `def __init__(self, ba:BuildArgs)->None`.

Example:
```python
class TensorFlowModel(Build):
  model:tf.keras.Model

def train(m:TensorFlowModel)->None:
  o = build_outpath(m)
  m.model = create_model(...)
  ...
  ...

def mymodel(m:Manager)->DRef:
  return mkdrv(m, ..., build_wrapper_(TensorFlowModel, train))
```

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


<a name="pylightnix.core.path2rref"></a>
## `path2rref()`

```python
def path2rref(p: Path) -> Optional[RRef]
```

Takes either a system path of some realization in the Pylightnix storage
or a symlink pointing to such path. Return `RRef` which corresponds to this
path.

Note: `path2rref` doesn't actually check the existance of such an object in
storage

<a name="pylightnix.core.mkconfig"></a>
## `mkconfig()`

```python
def mkconfig(d: dict) -> Config
```


<a name="pylightnix.core.config_dict"></a>
## `config_dict()`

```python
def config_dict(cp: Config) -> dict
```


<a name="pylightnix.core.config_cattrs"></a>
## `config_cattrs()`

```python
def config_cattrs(c: RConfig) -> Any
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
def config_deps(c: RConfig) -> Set[DRef]
```


<a name="pylightnix.core.config_substitutePromises"></a>
## `config_substitutePromises()`

```python
def config_substitutePromises(c: Config, r: DRef) -> RConfig
```

Replace all Promise tags with DRef `r`. In particular, all PromisePaths
are converted into RefPaths.

<a name="pylightnix.core.config_promises"></a>
## `config_promises()`

```python
def config_promises(c: Config, r: DRef) -> List[Tuple[str,PromisePath]]
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

<a name="pylightnix.core.store_cfgpath"></a>
## `store_cfgpath()`

```python
def store_cfgpath(r: DRef) -> Path
```


<a name="pylightnix.core.store_config_"></a>
## `store_config_()`

```python
def store_config_(r: DRef) -> Config
```


<a name="pylightnix.core.store_config"></a>
## `store_config()`

```python
def store_config(r: Union[DRef,RRef]) -> RConfig
```

Read the [Config](#pylightnix.types.Config) of the derivation and
[resolve](#pylightnix.core.config_substitutePromises) it from promises and
claims.

<a name="pylightnix.core.store_context"></a>
## `store_context()`

```python
def store_context(r: RRef) -> Context
```

FIXME: Either do `context_add(ctx, rref2dref(r), [r])` or document it's absense

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

<a name="pylightnix.core.store_buildtime"></a>
## `store_buildtime()`

```python
def store_buildtime(rref: RRef) -> Optional[str]
```

Return the buildtime of the current RRef in a format specified by the
[PYLIGHTNIX_TIME](#pylightnix.utils.PYLIGHTNIX_TIME) constant.

[parsetime](#pylightnix.utils.parsetime) may be used to parse stings into
UNIX-Epoch seconds.

Buildtime is the time when the realization process has started. Some
realizations may not provide this information.

<a name="pylightnix.core.store_gc"></a>
## `store_gc()`

```python
def store_gc(keep_drefs: List[DRef], keep_rrefs: List[RRef]) -> Tuple[Set[DRef],Set[RRef]]
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

Promise is a magic constant required to create
[PromisePath](#pylightnix.types.PromisePath), where it is used as a start
marker. Promise paths do exist only during
[instantiation](#pylightnix.core.instantiate) pass. The core replaces all
PromisePaths with corresponding [RefPaths](#pylightnix.type.RefPath)
automatically before it starts the realization pass (see
[store_config](#pylightnix.core.store_config)).

Ex-PromisePaths may be later converted into filesystem paths by
[build_path](#pylightnix.core.build_path) or by
[Lenses](#pylightnix.lens.Lens) as usual.

<a name="pylightnix.core.claim"></a>
## `claim`

```python
claim = PYLIGHTNIX_CLAIM_TAG
```

Claim is a [promise](#pylightnix.core.promise) which is not checked by the
Pylightnix. All other properties of promises are valid for claims.  All
PromisPaths which start from `claim` are substituted with corresponding
RefPaths by Pylightnix and may be later converted into system paths.

<a name="pylightnix.core.assert_promise_fulfilled"></a>
## `assert_promise_fulfilled()`

```python
def assert_promise_fulfilled(k: str, p: PromisePath, o: Path) -> None
```


<a name="pylightnix.core.mkdrv"></a>
## `mkdrv()`

```python
def mkdrv(m: Manager, config: Config, matcher: Matcher, realizer: Realizer, check_promises: bool = True) -> DRef
```

Run the instantiation of a particular stage. Create a
[Derivation](#pylightnix.types.Derivation) object out of three main
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
RealizeSeqGen = Generator[Tuple[DRef,Context,Derivation,RealizeArg],Tuple[Optional[List[RRef]],bool],List[RRef]]
```


<a name="pylightnix.core.realize"></a>
## `realize()`

```python
def realize(closure: Closure, force_rebuild: Union[List[DRef],bool] = [], assert_realized: List[DRef] = []) -> RRef
```

A simplified version of [realizeMany](#pylightnix.core.realizeMany).
Expects only one output path.

<a name="pylightnix.core.realizeMany"></a>
## `realizeMany()`

```python
def realizeMany(closure: Closure, force_rebuild: Union[List[DRef],bool] = [], assert_realized: List[DRef] = [], realize_args: Dict[DRef,RealizeArg] = {}) -> List[RRef]
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
def realizeSeq(closure: Closure, force_interrupt: List[DRef] = [], assert_realized: List[DRef] = [], realize_args: Dict[DRef,RealizeArg] = {}) -> RealizeSeqGen
```

Sequentially realize the closure by issuing steps via Python's generator
interface. `realizeSeq` encodes low-level details of the realization
algorithm. Consider calling [realizeMany](#pylightnix.core.realizeMany) or
it's analogs instead.

FIXME: `assert_realized` may probably be a implemented by calling `redefine`
with appropriate failing realizer on every Derivation.

<a name="pylightnix.core.mksymlink"></a>
## `mksymlink()`

```python
def mksymlink(rref: RRef, tgtpath: Path, name: str, withtime=True) -> Path
```

Create a symlink pointing to realization `rref`. Other arguments define
symlink name and location. Informally,
`{tgtpath}/{timeprefix}{name} --> $PYLIGHTNIX_STORE/{dref}/{rref}`.
Overwrite existing symlinks.

<a name="pylightnix.core.match"></a>
## `match()`

```python
def match(keys: List[Key], rmin: Optional[int] = 1, rmax: Optional[int] = 1, exclusive: bool = False) -> Matcher
```

Create a [Matcher](#pylightnix.types.Matcher) by combining different
sorting keys and selecting a top-n threshold.

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


<a name="pylightnix.build"></a>
# `pylightnix.build`

Built-in realization wrapper providing helpful functions like temporary build
directory management, time counting, etc.

<a name="pylightnix.build.mkbuildargs"></a>
## `mkbuildargs()`

```python
def mkbuildargs(dref: DRef, context: Context, timeprefix: Optional[str], iarg: InstantiateArg, rarg: RealizeArg) -> BuildArgs
```


<a name="pylightnix.build.mkbuild"></a>
## `mkbuild()`

```python
def mkbuild(dref: DRef, context: Context, buildtime: bool = True) -> Build
```


<a name="pylightnix.build.B"></a>
## `B`

```python
B = TypeVar('B')
```


<a name="pylightnix.build.build_wrapper_"></a>
## `build_wrapper_()`

```python
def build_wrapper_(f: Callable[[B],None], ctr: Callable[[BuildArgs],B], buildtime: bool = True) -> Realizer
```


<a name="pylightnix.build.build_wrapper"></a>
## `build_wrapper()`

```python
def build_wrapper(f: Callable[[Build],None], buildtime: bool = True) -> Realizer
```

Build Adapter which convers user-defined realizers which use
[Build](#pylightnix.types.Build) API into a low-level
[Realizer](#pylightnix.types.Realizer)

<a name="pylightnix.build.build_config"></a>
## `build_config()`

```python
def build_config(b: Build) -> RConfig
```

Return the [RConfig](#pylightnix.types.RConfig) object of the realization
being built.

<a name="pylightnix.build.build_context"></a>
## `build_context()`

```python
def build_context(b: Build) -> Context
```

Return the [Context](#pylightnix.types.Context) object of the realization
being built.

<a name="pylightnix.build.build_cattrs"></a>
## `build_cattrs()`

```python
def build_cattrs(b: Build) -> Any
```

Cache and return `ConfigAttrs`. Cache allows realizers to update it's
value during the build process, e.g. to use it as a storage.

<a name="pylightnix.build.build_setoutpaths"></a>
## `build_setoutpaths()`

```python
def build_setoutpaths(b: Build, nouts: int) -> List[Path]
```


<a name="pylightnix.build.build_outpaths"></a>
## `build_outpaths()`

```python
def build_outpaths(b: Build) -> List[Path]
```


<a name="pylightnix.build.build_outpath"></a>
## `build_outpath()`

```python
def build_outpath(b: Build) -> Path
```

Return the output path of the realization being built. Output path is a
path to valid temporary folder where user may put various build artifacts.
Later this folder becomes a realization.

<a name="pylightnix.build.build_name"></a>
## `build_name()`

```python
def build_name(b: Build) -> Name
```

Return the name of a derivation being built.

<a name="pylightnix.build.build_deref_"></a>
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

<a name="pylightnix.build.build_deref"></a>
## `build_deref()`

```python
def build_deref(b: Build, dref: DRef) -> RRef
```


<a name="pylightnix.build.build_paths"></a>
## `build_paths()`

```python
def build_paths(b: Build, refpath: RefPath) -> List[Path]
```

Convert given [RefPath](#pylightnix.types.RefPath) (which may be either a
regular RefPath or an ex-[PromisePath](#pylightnix.types.PromisePath)) into
one or many filesystem paths. Conversion refers to the
[Context](#pylightnix.types.Context) of the current realization process by
accessing it's [build_context](#pylightnix.core.build_context).

Typically, we configure stages to match only one realization at once, so the
returned list often has only one entry. Consider using
[build_path](#pylightnix.core.build_path) if this fact is known in advance.

Example:
```python
def config(dep:DRef)->RConfig:
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

<a name="pylightnix.build.build_path"></a>
## `build_path()`

```python
def build_path(b: Build, refpath: RefPath) -> Path
```

A single-realization version of the [build_paths](#pylightnix.core.build_paths).

<a name="pylightnix.inplace"></a>
# `pylightnix.inplace`

This module defines inplace variants of `instantiate` and `realize`
functions. Inplace functions store closures in their own global dependency
resolution [Manager](#pylightnix.types.Manager) and thus offer a simpler API,
but add usual risks of using gloabl variables.

<a name="pylightnix.inplace.PYLIGHTNIX_MANAGER"></a>
## `PYLIGHTNIX_MANAGER`

```python
PYLIGHTNIX_MANAGER = Manager()
```

The Global [Derivation manager](#pylightnix.types.Manager) used by
`instantiate_inplace` and `realize_inplace` functions of this module.

<a name="pylightnix.inplace.instantiate_inplace"></a>
## `instantiate_inplace()`

```python
def instantiate_inplace(stage: Any, args, *,, ,, kwargs) -> DRef
```

Instantiate a `stage`, use `PYLIGHTNIX_MANAGER` for storing derivations.
Return derivation reference of the top-level stage.

<a name="pylightnix.inplace.realize_inplace"></a>
## `realize_inplace()`

```python
def realize_inplace(dref: DRef, force_rebuild: List[DRef] = []) -> RRef
```

Realize the derivation pointed by `dref` by constructing it's
[Closure](#pylightnix.types.Closure) based on the contents of the global
dependency manager and [realizing](#pylightnix.core.realizeMany) this closure.

<a name="pylightnix.repl"></a>
# `pylightnix.repl`

Repl module defines variants of `instantiate` and `realize` functions, which
are suitable for REPL shells. Repl-friendly wrappers (see `repl_realize`) could
pause the computation, save the Pylightnix state into a variable and return to
the REPL's main loop. At this point user could alter the state of the whole
system.  Finally, `repl_continue` or `repl_cancel` could be called to either
continue or cancel the realization.

<a name="pylightnix.repl.ReplHelper"></a>
## `ReplHelper` Objects

```python
def __init__(self, gen: RealizeSeqGen) -> None
```


<a name="pylightnix.repl.ReplHelper.__init__"></a>
### `ReplHelper.__init__()`

```python
def __init__(self, gen: RealizeSeqGen) -> None
```


<a name="pylightnix.repl.ERR_INVALID_RH"></a>
## `ERR_INVALID_RH`

```python
ERR_INVALID_RH = "Neither global, nor user-defined ReplHelper is valid"
```


<a name="pylightnix.repl.ERR_INACTIVE_RH"></a>
## `ERR_INACTIVE_RH`

```python
ERR_INACTIVE_RH = "REPL session is not paused or was already unpaused"
```


<a name="pylightnix.repl.repl_continueMany"></a>
## `repl_continueMany()`

```python
def repl_continueMany(out_paths: Optional[List[Path]] = None, out_rrefs: Optional[List[RRef]] = None, rh: Optional[ReplHelper] = None) -> Optional[List[RRef]]
```


<a name="pylightnix.repl.repl_continue"></a>
## `repl_continue()`

```python
def repl_continue(out_paths: Optional[List[Path]] = None, out_rrefs: Optional[List[RRef]] = None, rh: Optional[ReplHelper] = None) -> Optional[RRef]
```


<a name="pylightnix.repl.repl_continueBuild"></a>
## `repl_continueBuild()`

```python
def repl_continueBuild(b: Build, rh: Optional[ReplHelper] = None) -> Optional[RRef]
```


<a name="pylightnix.repl.repl_realize"></a>
## `repl_realize()`

```python
def repl_realize(closure: Closure, force_interrupt: Union[List[DRef],bool] = True, realize_args: Dict[DRef,RealizeArg] = {}) -> ReplHelper
```

TODO

Example:
```python
rh=repl_realize(instantiate(mystage), force_interrupt=True)
# ^^^ `repl_realize` returnes the `ReplHelper` object which holds the state of
# incomplete realization
b:Build=repl_build()
# ^^^ Access it's build object. Now we may think that we are inside the
# realization function. Lets do some hacks.
with open(join(build_outpath(b),'artifact.txt'), 'w') as f:
  f.write("Fooo")
repl_continueBuild(b)
rref=repl_rref(rh)
# ^^^ Since we didn't program any other pasues, we should get the usual RRef
# holding the result of our hacks.
```

<a name="pylightnix.repl.repl_rrefs"></a>
## `repl_rrefs()`

```python
def repl_rrefs(rh: ReplHelper) -> Optional[List[RRef]]
```


<a name="pylightnix.repl.repl_rref"></a>
## `repl_rref()`

```python
def repl_rref(rh: ReplHelper) -> Optional[RRef]
```


<a name="pylightnix.repl.repl_buildargs"></a>
## `repl_buildargs()`

```python
def repl_buildargs(rh: Optional[ReplHelper] = None, buildtime: bool = True) -> BuildArgs
```


<a name="pylightnix.repl.repl_build"></a>
## `repl_build()`

```python
def repl_build(rh: Optional[ReplHelper] = None, buildtime: bool = True) -> Build
```


<a name="pylightnix.repl.repl_cancel"></a>
## `repl_cancel()`

```python
def repl_cancel(rh: Optional[ReplHelper] = None) -> None
```


<a name="pylightnix.repl.repl_cancelBuild"></a>
## `repl_cancelBuild()`

```python
def repl_cancelBuild(b: Build, rh: Optional[ReplHelper] = None) -> None
```


<a name="pylightnix.stages"></a>
# `pylightnix.stages`


<a name="pylightnix.stages.trivial"></a>
# `pylightnix.stages.trivial`

Trivial builtin stages

<a name="pylightnix.stages.trivial.mknode"></a>
## `mknode()`

```python
def mknode(m: Manager, sources: dict, artifacts: Dict[Name,bytes] = {}, name: str = 'mknode') -> DRef
```


<a name="pylightnix.stages.trivial.mkfile"></a>
## `mkfile()`

```python
def mkfile(m: Manager, name: Name, contents: bytes, filename: Optional[Name] = None) -> DRef
```


<a name="pylightnix.stages.trivial.checkpaths"></a>
## `checkpaths()`

```python
def checkpaths(m: Manager, promises: dict, name: str = "checkpaths") -> DRef
```


<a name="pylightnix.stages.trivial.redefine"></a>
## `redefine()`

```python
def redefine(stage: Any, new_config: Callable[[dict],Config] = mkconfig, new_matcher: Optional[Matcher] = None, new_realizer: Optional[Realizer] = None, check_promises: bool = True) -> Any
```

Define a new Derivation based on the existing one, by updating it's
config, optionally re-writing it's matcher, or it's realizer.

Arguments:
- `stage:Any` a `Stage` function, accepting arbitrary keyword arguments
- `new_config:Callable[[dict],Config]=mkconfig` A function to update the `dref`'s
  config. Defaults to `mkconfig` function (here similar to the identity).
- `new_matcher:Optional[Matcher]=None` Optional new matcher (defaults to the
  existing matcher)
- `new_realizer:Optional[Realizer]=None` Optional new realizer (defaults to
  the existing realizer)

Return:
A callable `Stage`, accepting pass-through arguments

Example:
```python
def _new_config(old_config):
  old_config['learning_rate'] = 1e-5
  return mkconfig(old_config)
realize(instantiate(redefine(myMLmodel, _new_config)))
```

FIXME: Current version will may either update realizer of an existing config,
or create a completely new derivation, depending on whether we change modify
the config or not. One should define the behaviour more clearly.

<a name="pylightnix.stages.trivial.realized"></a>
## `realized()`

```python
def realized(stage: Any) -> Stage
```

[Re-define](#pylightnix.stages.trivial.redefine) stage's realizer by
replacing it with a dummy realizer triggering an assertion. As a result, the
call to [realize](#pylightnix.core.realizeMany) will only succeed if no
realization is actually required. Designed to make users sure that some
stage's realize will return immediately.

Example:
```python
rref:RRef=realize(instantiate(realized(my_long_running_stage, arg="bla")))
# ^^^ Fail if `my_long_running_stage` is not yet realized.
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


<a name="pylightnix.stages.fetch._unpack"></a>
## `_unpack()`

```python
def _unpack(o: str, fullpath: str, remove_file: bool)
```


<a name="pylightnix.stages.fetch.fetchurl"></a>
## `fetchurl()`

```python
def fetchurl(m: Manager, url: str, sha256: Optional[str] = None, sha1: Optional[str] = None, mode: str = 'unpack,remove', name: Optional[str] = None, filename: Optional[str] = None, force_download: bool = False, check_promises: bool = True, kwargs) -> DRef
```

Download and unpack an URL addess.

Downloading is done by calling `wget` application. Optional unpacking is
performed with the `aunpack` script from `atool` package. `sha256` defines the
expected SHA-256 hashsum of the stored data. `mode` allows to tweak the
stage's behavior: adding word 'unpack' instructs fetchurl to unpack the
package, adding 'remove' instructs it to remove the archive after unpacking.

Agruments:
- `m:Manager` the dependency resolution [Manager](#pylightnix.types.Manager).
- `url:str` URL to download from. Should point to a single file.
- `sha256:str` SHA-256 hash sum of the file.
- `model:str='unpack,remove'` Additional options. Format: `[unpack[,remove]]`.
- `name:Optional[str]`: Name of the Derivation. The stage will attempt to
  deduce the name if not specified.
- `filename:Optional[str]=None` Name of the filename on disk after downloading.
  Stage will attempt to deduced it if not specified.
- `force_download:bool=False` If False, resume the last download if
  possible.
- `check_promises:bool=True` Passed to `mkdrv` as-is.

Example:
```python
def hello_src(m:Manager)->DRef:
  hello_version = '2.10'
  return fetchurl(
    m,
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b')

rref:RRef=realize(instantiate(hello_src))
print(rref2path(rref))
```

<a name="pylightnix.stages.fetch.fetchlocal"></a>
## `fetchlocal()`

```python
def fetchlocal(m: Manager, path: str, sha256: str, mode: str = 'unpack,remove', name: Optional[str] = None, filename: Optional[str] = None, kwargs) -> DRef
```

Copy local file into Pylightnix storage. This function is typically
intended to register application-specific files which are distributed with a
source repository.


FIXME: Switch regular `fetchurl` to `curl` and call it with `file://` URLs.

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

<a name="pylightnix.bashlike.shell"></a>
## `shell()`

```python
def shell(r: Union[Build,RRef,DRef,Path,str,None] = None) -> None
```

Open the Unix Shell in the directory associated with the argument passed.
Path to the shell executable is read from the `SHELL` environment variable,
defaulting to `/bin/sh`. If `r` is None, open the shell in the root of the
Pylightnix storage.

The function is expected to be run in REPL Python shells like IPython.

<a name="pylightnix.bashlike.shellref"></a>
## `shellref()`

```python
def shellref(r: Union[RRef,DRef,None] = None) -> None
```

Alias for [shell](#pylightnix.bashlike.shell). Deprecated.

<a name="pylightnix.bashlike.du"></a>
## `du()`

```python
def du() -> Dict[DRef,Tuple[int,Dict[RRef,int]]]
```

Calculates the disk usage, in bytes. For every derivation, return it's
total disk usage and disk usages per realizations. Note, that total disk usage
of a derivation is slightly bigger than sum of it's realization's usages.

<a name="pylightnix.bashlike.find"></a>
## `find()`

```python
def find(name: Optional[Union[Stage,str]] = None, newer: Optional[float] = None) -> List[RRef]
```

Find [RRefs](#pylightnix.types.RRef) in Pylightnix sotrage which
match all of the criteria provided. Without arguments return all RRefs.

Arguments:
- `name:Optional[Union[Stage,str]]=None` match RRefs which have `name` in
  their name.  Matching is done by `fnmatch` Python function which supports
  shell-like glob expressions with '*' and '?' symbols. If name is a
  [Stage](#pylightnix.types.Stage) then it is instantiated and it's name is
  taken.
- `newer:Optional[float]=None` match RRefs which are newer than this number of
  seconds starting from the UNIX Epoch. Zero and negative numbers count
  backward from the current time.

FIXME: If name is a stage, then this function instantiates this stage before
searching. Thus, the storage is moified, which may be a undesired
behaviour

<a name="pylightnix.bashlike.diff"></a>
## `diff()`

```python
def diff(stageA: Union[RRef,DRef,Stage], stageB: Union[RRef,DRef,Stage]) -> None
```

Run system's `diff` utility to print the difference between configs of 2
stages passed.

Note: if argument is a Stage, it is instantiated first

<a name="pylightnix.lens"></a>
# `pylightnix.lens`

Lens module defines the `Lens` helper class, which offers quick navigation
through the dependent configurations

<a name="pylightnix.lens.Lens"></a>
## `Lens` Objects

```python
def __init__(self, ctx: Tuple[Optional[Path],Optional[Context]], v: Any) -> None
```

Lens objects provide quick access to the parameters of stage
configurations by navigating through different kinds of Pylightnix entities
like DRefs, RRefs, Configs and RefPaths.

Lens lifecycle consists of three stages:
1. Creation on the basis of existing objects. Lens may be created out of
   any Python value, but the meaningful operations (besides getting this value
   back) are supported for the Pylightnix types which could be casted to
   Python dictionaries. See [mklens](#pylightnix.lens.mklens) for the list of
   supported source objects.
2. Navigation through the nested configurations. Lenses access configuration
   attributes, automatically dereference Pylightnix references and produce other
   Lenses, which are 'focused' on new locations.
3. Access to the raw value which could no longer be converted into a Lens. In
   this case the raw value is returned.

To create Lenses, use `mklens` function rather than creating it directly
because it encodes a number of supported ways of deducing `ctx` of Lens.

<a name="pylightnix.lens.Lens.__init__"></a>
### `Lens.__init__()`

```python
def __init__(self, ctx: Tuple[Optional[Path],Optional[Context]], v: Any) -> None
```


<a name="pylightnix.lens.Lens.__getattr__"></a>
### `Lens.__getattr__()`

```python
def __getattr__(self, key) -> "Lens"
```

Sugar for `Lens.get`

<a name="pylightnix.lens.Lens.get"></a>
### `Lens.get()`

```python
def get(self, key) -> "Lens"
```

Return a new Lens out of the `key` attribute of the current Lens

<a name="pylightnix.lens.Lens.val"></a>
### `Lens.val()`

```python
@property
def val(self) -> Any
```

Return th current value of Lens as-is

<a name="pylightnix.lens.Lens.refpath"></a>
### `Lens.refpath()`

```python
@property
def refpath(self) -> RefPath
```

Check that the current value of Lens is a `RefPath` and return it

<a name="pylightnix.lens.Lens.syspath"></a>
### `Lens.syspath()`

```python
@property
def syspath(self) -> Path
```

Check that the current value of Lens is a `Path` and return it

<a name="pylightnix.lens.Lens.dref"></a>
### `Lens.dref()`

```python
@property
def dref(self) -> DRef
```

Check that the current value of Lens is a `DRef` and return it

<a name="pylightnix.lens.Lens.rref"></a>
### `Lens.rref()`

```python
@property
def rref(self) -> RRef
```

Check that the current value of Lens is an `RRef` and return it

<a name="pylightnix.lens.Lens.resolve"></a>
### `Lens.resolve()`

```python
def resolve(self) -> Path
```

Resolve the current value of Lens into system path. Assert if it is not
possible or if the result is associated with multiple paths.

<a name="pylightnix.lens.Lens.as_dict"></a>
### `Lens.as_dict()`

```python
def as_dict(self) -> dict
```

Return the `dict` representation of the Lens, asserting that it is possible.

<a name="pylightnix.lens.mklens"></a>
## `mklens()`

```python
def mklens(x: Any, o: Optional[Path] = None, b: Optional[Build] = None, rref: Optional[RRef] = None, ctx: Optional[Context] = None) -> Lens
```

Mklens creates [Lenses](#pylightnix.lens.Lens) from various user objects.

Arguments:
- `x:Any` The object to create the Lens from. Supported source object types
  are:
  * `RRefs`
  * `DRefs`
  * `Build`
  * `RefPath`
  * `dict`
- `b:Optional[Build]=None` Optional `Build` context of the Lens. Passing this
  object would allow Lens to resolve RRefs using the Context of the current
  realization. Also it would allow the Lens to use
  [build_path](#pylightnix.core.build_path) function to
  resolve Build paths.
- `rref:Optional[RRef]=None` Optional `RRef` link. Passing this object will
  allow Lens to resolve other RRefs using the Context of the given RRef.
- `ctx:Optional[Context]=None` Passing optional Context would allow Lens to
  resolve RRefs.

