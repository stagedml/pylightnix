# Table of Contents

  * [pylightnix.types](#pylightnix.types)
    * [Path](#pylightnix.types.Path)
    * [SPath](#pylightnix.types.SPath)
    * [StorageSettings](#pylightnix.types.StorageSettings)
    * [Hash](#pylightnix.types.Hash)
    * [HashPart](#pylightnix.types.HashPart)
    * [DRef](#pylightnix.types.DRef)
    * [RRef](#pylightnix.types.RRef)
    * [Name](#pylightnix.types.Name)
    * [RefPath](#pylightnix.types.RefPath)
    * [PylightnixException](#pylightnix.types.PylightnixException)
    * [PromiseException](#pylightnix.types.PromiseException)
    * [\_REF](#pylightnix.types._REF)
    * [Output](#pylightnix.types.Output)
    * [Context](#pylightnix.types.Context)
    * [InstantiateArg](#pylightnix.types.InstantiateArg)
    * [RealizeArg](#pylightnix.types.RealizeArg)
    * [Matcher](#pylightnix.types.Matcher)
    * [MatcherO](#pylightnix.types.MatcherO)
    * [Realizer](#pylightnix.types.Realizer)
    * [RealizerO](#pylightnix.types.RealizerO)
    * [Derivation](#pylightnix.types.Derivation)
    * [Closure](#pylightnix.types.Closure)
    * [Config](#pylightnix.types.Config)
    * [RConfig](#pylightnix.types.RConfig)
    * [ConfigAttrs](#pylightnix.types.ConfigAttrs)
    * [BuildArgs](#pylightnix.types.BuildArgs)
    * [Build](#pylightnix.types.Build)
    * [Registry](#pylightnix.types.Registry)
    * [DRefLike](#pylightnix.types.DRefLike)
    * [StageResult](#pylightnix.types.StageResult)
    * [Stage](#pylightnix.types.Stage)
  * [pylightnix.core](#pylightnix.core)
    * [PYLIGHTNIX\_STORE\_VERSION](#pylightnix.core.PYLIGHTNIX_STORE_VERSION)
    * [PYLIGHTNIX\_NAMEPAT](#pylightnix.core.PYLIGHTNIX_NAMEPAT)
    * [PYLIGHTNIX\_RESERVED](#pylightnix.core.PYLIGHTNIX_RESERVED)
    * [logger](#pylightnix.core.logger)
    * [info](#pylightnix.core.info)
    * [warning](#pylightnix.core.warning)
    * [TL](#pylightnix.core.TL)
    * [tlregistry](#pylightnix.core.tlregistry)
    * [tlstorage](#pylightnix.core.tlstorage)
    * [storagename](#pylightnix.core.storagename)
    * [fsroot](#pylightnix.core.fsroot)
    * [fstmpdir](#pylightnix.core.fstmpdir)
    * [fsstorage](#pylightnix.core.fsstorage)
    * [assert\_valid\_storage](#pylightnix.core.assert_valid_storage)
    * [mkSS](#pylightnix.core.mkSS)
    * [setstorage](#pylightnix.core.setstorage)
    * [setregistry](#pylightnix.core.setregistry)
    * [fsinit](#pylightnix.core.fsinit)
    * [reserved](#pylightnix.core.reserved)
    * [trimhash](#pylightnix.core.trimhash)
    * [mkdref](#pylightnix.core.mkdref)
    * [rref2dref](#pylightnix.core.rref2dref)
    * [undref](#pylightnix.core.undref)
    * [mkrref](#pylightnix.core.mkrref)
    * [unrref](#pylightnix.core.unrref)
    * [mkname](#pylightnix.core.mkname)
    * [path2dref](#pylightnix.core.path2dref)
    * [path2rref](#pylightnix.core.path2rref)
    * [mkconfig](#pylightnix.core.mkconfig)
    * [cfgdict](#pylightnix.core.cfgdict)
    * [cfgcattrs](#pylightnix.core.cfgcattrs)
    * [cfgserialize](#pylightnix.core.cfgserialize)
    * [cfghash](#pylightnix.core.cfghash)
    * [cfgname](#pylightnix.core.cfgname)
    * [cfgdeps](#pylightnix.core.cfgdeps)
    * [mkrefpath](#pylightnix.core.mkrefpath)
    * [resolve](#pylightnix.core.resolve)
    * [dref2path](#pylightnix.core.dref2path)
    * [rref2path](#pylightnix.core.rref2path)
    * [rrefpath2path](#pylightnix.core.rrefpath2path)
    * [drefcfgpath](#pylightnix.core.drefcfgpath)
    * [rrefctx](#pylightnix.core.rrefctx)
    * [drefcfg\_](#pylightnix.core.drefcfg_)
    * [drefcfg](#pylightnix.core.drefcfg)
    * [drefattrs](#pylightnix.core.drefattrs)
    * [rrefattrs](#pylightnix.core.rrefattrs)
    * [drefdeps1](#pylightnix.core.drefdeps1)
    * [rrefdeps1](#pylightnix.core.rrefdeps1)
    * [drefdeps](#pylightnix.core.drefdeps)
    * [rrefdeps](#pylightnix.core.rrefdeps)
    * [alldrefs](#pylightnix.core.alldrefs)
    * [allrrefs](#pylightnix.core.allrrefs)
    * [rootdrefs](#pylightnix.core.rootdrefs)
    * [rootrrefs](#pylightnix.core.rootrrefs)
    * [rrefdata](#pylightnix.core.rrefdata)
    * [drefrrefs](#pylightnix.core.drefrrefs)
    * [drefrrefsC](#pylightnix.core.drefrrefsC)
    * [store\_gc](#pylightnix.core.store_gc)
    * [mkdrv\_](#pylightnix.core.mkdrv_)
    * [mkrealization](#pylightnix.core.mkrealization)
    * [mkcontext](#pylightnix.core.mkcontext)
    * [context\_eq](#pylightnix.core.context_eq)
    * [context\_add](#pylightnix.core.context_add)
    * [context\_deref](#pylightnix.core.context_deref)
    * [context\_derefpath](#pylightnix.core.context_derefpath)
    * [context\_serialize](#pylightnix.core.context_serialize)
    * [output\_validate](#pylightnix.core.output_validate)
    * [output\_realizer](#pylightnix.core.output_realizer)
    * [output\_matcher](#pylightnix.core.output_matcher)
    * [mkdrv](#pylightnix.core.mkdrv)
    * [current\_registry](#pylightnix.core.current_registry)
    * [current\_storage](#pylightnix.core.current_storage)
    * [mkclosure](#pylightnix.core.mkclosure)
    * [\_A](#pylightnix.core._A)
    * [instantiate](#pylightnix.core.instantiate)
    * [RealizeSeqGen](#pylightnix.core.RealizeSeqGen)
    * [realize1](#pylightnix.core.realize1)
    * [realizeMany](#pylightnix.core.realizeMany)
    * [realize](#pylightnix.core.realize)
    * [realizeSeq](#pylightnix.core.realizeSeq)
    * [evaluate](#pylightnix.core.evaluate)
    * [Key](#pylightnix.core.Key)
    * [texthash](#pylightnix.core.texthash)
    * [latest](#pylightnix.core.latest)
    * [exact](#pylightnix.core.exact)
    * [match](#pylightnix.core.match)
    * [match\_all](#pylightnix.core.match_all)
    * [match\_some](#pylightnix.core.match_some)
    * [match\_only](#pylightnix.core.match_only)
    * [match\_latest](#pylightnix.core.match_latest)
    * [match\_exact](#pylightnix.core.match_exact)
    * [cfgsp](#pylightnix.core.cfgsp)
    * [assert\_valid\_refpath](#pylightnix.core.assert_valid_refpath)
    * [assert\_valid\_config](#pylightnix.core.assert_valid_config)
    * [assert\_valid\_name](#pylightnix.core.assert_valid_name)
    * [assert\_valid\_rref](#pylightnix.core.assert_valid_rref)
    * [assert\_valid\_hashpart](#pylightnix.core.assert_valid_hashpart)
    * [assert\_valid\_dref](#pylightnix.core.assert_valid_dref)
    * [assert\_valid\_hash](#pylightnix.core.assert_valid_hash)
    * [assert\_valid\_context](#pylightnix.core.assert_valid_context)
    * [assert\_valid\_closure](#pylightnix.core.assert_valid_closure)
    * [assert\_rref\_deps](#pylightnix.core.assert_rref_deps)
    * [assert\_have\_realizers](#pylightnix.core.assert_have_realizers)
  * [pylightnix.build](#pylightnix.build)
    * [logger](#pylightnix.build.logger)
    * [info](#pylightnix.build.info)
    * [warning](#pylightnix.build.warning)
    * [error](#pylightnix.build.error)
    * [BuildError](#pylightnix.build.BuildError)
    * [mkbuildargs](#pylightnix.build.mkbuildargs)
    * [\_B](#pylightnix.build._B)
    * [build\_wrapper\_](#pylightnix.build.build_wrapper_)
    * [build\_wrapper](#pylightnix.build.build_wrapper)
    * [build\_config](#pylightnix.build.build_config)
    * [build\_context](#pylightnix.build.build_context)
    * [build\_cattrs](#pylightnix.build.build_cattrs)
    * [build\_markstart](#pylightnix.build.build_markstart)
    * [build\_markstop](#pylightnix.build.build_markstop)
    * [build\_markstop\_noexcept](#pylightnix.build.build_markstop_noexcept)
    * [rrefbstart](#pylightnix.build.rrefbstart)
    * [rrefbstop](#pylightnix.build.rrefbstop)
    * [rrefbdelta](#pylightnix.build.rrefbdelta)
    * [build\_outpaths](#pylightnix.build.build_outpaths)
    * [build\_outpath](#pylightnix.build.build_outpath)
    * [build\_name](#pylightnix.build.build_name)
    * [build\_deref\_](#pylightnix.build.build_deref_)
    * [build\_deref](#pylightnix.build.build_deref)
    * [build\_paths](#pylightnix.build.build_paths)
    * [build\_path](#pylightnix.build.build_path)
    * [build\_environ](#pylightnix.build.build_environ)
    * [repl\_continueBuild](#pylightnix.build.repl_continueBuild)
    * [repl\_buildargs](#pylightnix.build.repl_buildargs)
    * [repl\_build](#pylightnix.build.repl_build)
    * [repl\_cancelBuild](#pylightnix.build.repl_cancelBuild)
  * [pylightnix.repl](#pylightnix.repl)
    * [ReplHelper](#pylightnix.repl.ReplHelper)
    * [ERR\_INVALID\_RH](#pylightnix.repl.ERR_INVALID_RH)
    * [ERR\_INACTIVE\_RH](#pylightnix.repl.ERR_INACTIVE_RH)
    * [repl\_continueAll](#pylightnix.repl.repl_continueAll)
    * [repl\_continueMany](#pylightnix.repl.repl_continueMany)
    * [repl\_continue](#pylightnix.repl.repl_continue)
    * [repl\_realize](#pylightnix.repl.repl_realize)
    * [repl\_result](#pylightnix.repl.repl_result)
    * [repl\_rrefs](#pylightnix.repl.repl_rrefs)
    * [repl\_rref](#pylightnix.repl.repl_rref)
    * [repl\_cancel](#pylightnix.repl.repl_cancel)
  * [pylightnix.stages](#pylightnix.stages)
  * [pylightnix.stages.trivial](#pylightnix.stages.trivial)
    * [mknode](#pylightnix.stages.trivial.mknode)
    * [redefine](#pylightnix.stages.trivial.redefine)
    * [realized](#pylightnix.stages.trivial.realized)
  * [pylightnix.stages.fetch2](#pylightnix.stages.fetch2)
    * [logger](#pylightnix.stages.fetch2.logger)
    * [info](#pylightnix.stages.fetch2.info)
    * [error](#pylightnix.stages.fetch2.error)
    * [CURL](#pylightnix.stages.fetch2.CURL)
    * [AUNPACK](#pylightnix.stages.fetch2.AUNPACK)
    * [fetchurl2](#pylightnix.stages.fetch2.fetchurl2)
    * [unpack](#pylightnix.stages.fetch2.unpack)
  * [pylightnix.stages.fetch](#pylightnix.stages.fetch)
    * [logger](#pylightnix.stages.fetch.logger)
    * [info](#pylightnix.stages.fetch.info)
    * [error](#pylightnix.stages.fetch.error)
    * [WGET](#pylightnix.stages.fetch.WGET)
    * [AUNPACK](#pylightnix.stages.fetch.AUNPACK)
    * [\_unpack\_inplace](#pylightnix.stages.fetch._unpack_inplace)
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
    * [linkrref](#pylightnix.bashlike.linkrref)
    * [linkdref](#pylightnix.bashlike.linkdref)
    * [linkrrefs](#pylightnix.bashlike.linkrrefs)
  * [pylightnix.lens](#pylightnix.lens)
    * [LensContext](#pylightnix.lens.LensContext)
    * [val2dict](#pylightnix.lens.val2dict)
    * [val2rref](#pylightnix.lens.val2rref)
    * [val2path](#pylightnix.lens.val2path)
    * [traverse](#pylightnix.lens.traverse)
    * [mutate](#pylightnix.lens.mutate)
    * [lens\_repr](#pylightnix.lens.lens_repr)
    * [Lens](#pylightnix.lens.Lens)
    * [mklens](#pylightnix.lens.mklens)
  * [pylightnix.either](#pylightnix.either)
    * [\_REF](#pylightnix.either._REF)
    * [ExceptionText](#pylightnix.either.ExceptionText)
    * [Either](#pylightnix.either.Either)
    * [mkright](#pylightnix.either.mkright)
    * [mkleft](#pylightnix.either.mkleft)
    * [either\_paths](#pylightnix.either.either_paths)
    * [either\_isRight](#pylightnix.either.either_isRight)
    * [either\_isLeft](#pylightnix.either.either_isLeft)
    * [either\_status](#pylightnix.either.either_status)
    * [either\_loadR](#pylightnix.either.either_loadR)
    * [either\_validate](#pylightnix.either.either_validate)
    * [either\_realizer](#pylightnix.either.either_realizer)
    * [either\_matcher](#pylightnix.either.either_matcher)
    * [mkdrvE](#pylightnix.either.mkdrvE)
    * [realizeE](#pylightnix.either.realizeE)
    * [realizeManyE](#pylightnix.either.realizeManyE)
  * [pylightnix.arch](#pylightnix.arch)
    * [APACK](#pylightnix.arch.APACK)
    * [AUNPACK](#pylightnix.arch.AUNPACK)
    * [spack](#pylightnix.arch.spack)
    * [sunpack](#pylightnix.arch.sunpack)
    * [deref\_](#pylightnix.arch.deref_)
    * [copyclosure](#pylightnix.arch.copyclosure)
  * [pylightnix.deco](#pylightnix.deco)
    * [Attrs](#pylightnix.deco.Attrs)
    * [unroll](#pylightnix.deco.unroll)
    * [autodrv\_](#pylightnix.deco.autodrv_)
    * [autodrv](#pylightnix.deco.autodrv)
    * [autostage\_](#pylightnix.deco.autostage_)
    * [autostage](#pylightnix.deco.autostage)

<a name="pylightnix.types"></a>
# `pylightnix.types`

All main types which we use in Pylightnix are defined here.

<a name="pylightnix.types.Path"></a>
## `Path` Objects

`Path` is an alias for string. It is used in pylightnix to
tell the typechecker that a given string contains a filesystem path.

<a name="pylightnix.types.SPath"></a>
## `SPath` Objects

`SPath` is an alias for string. It is used in pylightnix to
tell the typechecker that a given string contains a path to storage.

<a name="pylightnix.types.StorageSettings"></a>
## `StorageSettings`

```python
StorageSettings = NamedTuple('StorageSettings',[('root',Optional[Path]),
                                              ...
```

Stoarge settings contains a path for the main stoarge and a path for
temporary directories. These paths need to be on the same device in order to
atomic rename work.

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

`DRef` stands for *derivation reference*. It is a string identifier of a
filesystem part of [Derivation](#pylightnix.types.Derivation) object.

The format of derivation reference is `<HashPart>-<Name>`, where:
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
[realizing](#pylightnix.core.realize1) it from scratch.

- For derefencing dependencies at the build time, see
  [build_deref](#pylightnix.core.build_deref).
- For querying the storage, see [store_deref](#pylightnix.core.store_deref).

<a name="pylightnix.types.RRef"></a>
## `RRef` Objects

`RRef` stands for *Realization Reference*. RRefs identify collections of
artifacts of a [Stage](#pylightnix.types.Stage). Stages with non-determenistic
realizers may have several competing realization instances. Every such
instance is identified by a unique RRef.

The format of realization reference is `<HashPart0>-<HashPart1>-<Name>`,
where:
- `<HashPart0>` is calculated over realization's
  [Context](#pylightnix.types.Context) and build artifacts.
- `<HashPart1>-<Name>` forms valid [DRef](#pylightnix.types.DRef) which
  this realizaion was [realized](#pylightnix.core.realize1) from.

Realization reference is created during the
[realization](#pylightnix.core.realize1) process .

Valid realization references may be dereferenced down to system paths of
*build artifacts* by calling [rref2path](#pylightnix.core.rref2path) or by
using [lenses](#pyligntix.lens.Lens).

[Autostage](#pylightnix.deco.autostage) decorator unwraps RRefs of parent
stages into [Attrs](#pylightnix.deco.Attrs) objects.

<a name="pylightnix.types.Name"></a>
## `Name` Objects

`Name` is an alias for string. It is used in pylightnix to tell the
typechecker that a given string contains name of a pylightnix storage object.

Names are restircted to contain charaters matching `PYLIGHTNIX_NAMEPAT`.

See also `mkname`

<a name="pylightnix.types.RefPath"></a>
## `RefPath`

```python
RefPath = List[Union[DRef,str]]
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
[rref2path](#pylightnix.core.store_rref2path)
3.  Join the system path with `[1:]` part of RefPath to get the real filename.

The algorithm described above is implemented as
[build_path](#pylightnix.core.build_path) helper function.

<a name="pylightnix.types.PylightnixException"></a>
## `PylightnixException` Objects

Base class of Pylightnix exceptions

<a name="pylightnix.types.PromiseException"></a>
## `PromiseException` Objects

```python
def __init__(self, dref: DRef, failed: List[Tuple[Path,RefPath]])
```


<a name="pylightnix.types.PromiseException.__init__"></a>
### `PromiseException.__init__()`

```python
def __init__(self, dref: DRef, failed: List[Tuple[Path,RefPath]])
```


<a name="pylightnix.types._REF"></a>
## `_REF`

```python
_REF = TypeVar('_REF')
```


<a name="pylightnix.types.Output"></a>
## `Output` Objects

```python
def __init__(self, val: Iterable[_REF])
```

Output is a base class for 'organized collections of realizations', either
in form of temporary Paths or RRefs.

TODO: Rename into something which has a meaning of `PromisedOuput`

<a name="pylightnix.types.Output.__init__"></a>
### `Output.__init__()`

```python
def __init__(self, val: Iterable[_REF])
```


<a name="pylightnix.types.Context"></a>
## `Context`

```python
Context = Dict[DRef,List[RRef]]
```


<a name="pylightnix.types.InstantiateArg"></a>
## `InstantiateArg`

```python
InstantiateArg = Dict[str,Any]
```

Type of user-defined arguments to pass to the Config

<a name="pylightnix.types.RealizeArg"></a>
## `RealizeArg`

```python
RealizeArg = Dict[str,Any]
```

Type of user-defined arguments to pass to the Realizer

<a name="pylightnix.types.Matcher"></a>
## `Matcher`

```python
Matcher = Callable[[Optional[StorageSettings],List[RRef]],
                   Optional[List[RRef]]]
```

Matchers are user-defined Python functions with the fixed signature. They
serve two purposes:
1. Decide whether to launch a new realization or re-use the results of
realizations completed earlier.
2. Filter a subset of a realizations to depend on out of the set of
available realizations.

Matchers answer 'yes' to the first question by returning None. Non-none value
specifies the matched set of realizations.

The Matcher's invariants are:

- Matcher outputs should only depend on the immutable realizations passed to
them as inputs. Matchers should avoid having side-effects.
- Matchers must be satisfiable. If the matcher returns None, the core
re-runs runs the realization and calls the matcher once again. Returning
None again would be an error.

Pylightnix includes a set of built-in matchers:

- [match_latest](#pylightnix.core.match_latest) prefers the latest
realizations
- [match_all](#pylightnix.core.match_all) takes everything
- [match_some](#pylightnix.core.match_some) takes not less than N realizations
- [match_only](#pylightnix.core.match_only) expects exactly one realization

<a name="pylightnix.types.MatcherO"></a>
## `MatcherO`

```python
MatcherO = Callable[[Optional[StorageSettings],Output[RRef]],
                    Optional[Output[RRef]]]
```


<a name="pylightnix.types.Realizer"></a>
## `Realizer`

```python
Realizer = Callable[[Optional[StorageSettings],DRef,Context,RealizeArg],List[Path]]
```

Realizers are user-defined Python functions. Realizers typically
implement [application-specific algorithms](#pylightnix.core.realize1) which
take some configuration parameters and produce some artifacts.

Realizer accepts the following arguments:

- Path to a global Pylightnix storage
- A [Derivation reference](#pylightnix.types.DRef) being built
- A [Context](#pylightnix.types.Context) encoding the results of dependency
resolution.
- Set of additional user-defined arguments

Context is the key to accessing the dependency artifacts.

Derivation reference is required to access [configuration
parameters](#pylightnix.types.Config) of the algorithm.

Realizers must return one or many folders of realization artifacts (files and
folders containing application-specific data). Every folder is treated as an
alternative realization.  [Matcher](#pylightnix.types.Matcher) is later used
to pick the subset of realizations which matches some application-specific
criteria.  This subset will eventually appear as the `Context`s of downstream
realizaions.

Pylightnix stages may use the simplified realizer API
provided by the [Build](#pylightnix.types.Build) helper class.

Example:

```python
def mystage(r:Registry)->DRef:
def _realize(dref:DRef, context:Context)->List[Path]:
b=mkbuild(dref, context, buildtime=buildtime)
with open(join(build_outpath(b),'artifact'),'w') as f:
f.write('chickenpoop\n')
return [build_outpath(b)]
...
return mkdrv(r, ...,  _realize)
```

<a name="pylightnix.types.RealizerO"></a>
## `RealizerO`

```python
RealizerO = Callable[[Optional[StorageSettings],DRef,Context,RealizeArg],Output[Path]]
```


<a name="pylightnix.types.Derivation"></a>
## `Derivation`

```python
Derivation = NamedTuple('Derivation', [('dref',DRef),
                                       ('matcher',Matcher), ...
```

Derivation is a core Pylightnix entity. It holds the information required to
produce artifacts of individual [Stage](#pylightnix.types.stage).

Fields include:
* [Configuration](#pylightnix.types.Config) objects serialized on disk.
* [Matcher](#pylightnix.types.Matcher) Python function
* [Realizer](#pylightnix.core.realize1) Python function

The actual configuration is stored in the Pylightnix filesystem storage.
Derivation holds the [DRef](#pylightnix.types.DRef) access key.

Derivations normally appear as a result of [mkdrv](#pylightnix.core.mkdrv)
calls.

<a name="pylightnix.types.Closure"></a>
## `Closure`

```python
Closure = NamedTuple('Closure', [('result',Any),
                                 ('targets',List[DRef]),
     ...
```

Closure describes the realization plan of some
[Derivation](#pylightnix.types.Derivation).

The plan is represented by a sequence of
[Derivations](#pylightnix.types.Derivation) one need to realize1 in order to
realize1 a given target derivation.

Closures are typically obtained as a result of the
[instantiate](#pylightnix.core.instantiate) and is typically consumed by the
call to [realize1](#pylightnix.core.realize1) or it's analogs.

<a name="pylightnix.types.Config"></a>
## `Config` Objects

```python
def __init__(self, d: dict)
```

Config is a JSON-serializable dict-like object containing user-defined
attributes. Together with [Realizers](#pylightnix.types.Realizer) and
[Matchers](#pylightnix.types.Matcher), configs describe
[Stage](#pylightnix.types.Stage) objects.

Configs carry Python dictionaries that should contain JSON-serializable types.
Strings, bools, ints, floats, lists or other dicts are fine, but no bytes,
`numpy.float32` or lambdas are allowed. Tuples are also forbidden because they
are not preserved (decoded into lists). Special emphasis is placed on
[DRef](#pylightnix.types.DRef) support which link dependent stages together.

Config of a derivation can't include the Derivation reference to itself,
because it contains the config hash as its part.

Some field names of a config have a special meaning for Pylightnix:

* String `name` field will be used as a part of references to
  a derivation associated with this config.
* [RefPaths](#pylightnix.types.RefPath) represent paths to
  artifacts within the stage artifact folders.
* [SelfRef](#pylightnix.core.selfref) paths represent output paths to be
  produced during the stage's realization.
* [DRef](#pylightnix.types.DRef) represent stage dependencies.  Pylightnix
  collects derivation references and plan the realization order based on them.

Storing an [RRef](#pylightnix.types.RRef) in the config leads to a warning.
Pylightnix does not necessarily knows how to produce the exact reference, so
the end result may not match the expectations.

Configs are normally created from Python dicts by the
[mkconfig](#pylightnix.core.mkconfig) function.

Example:
```python
def mystage(r:Registry)->Dref:
  def _config()->dict:
    name = 'mystage'
    nepoches = 4
    learning_rate = 1e-5
    hidden_size = 128
    return locals()
  return mkdrv(mkconfig(_config()),...)
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

`RConfig` is a [Config](#pylightnix.types.Config) where all
[Self-referenes](#pylightnix.types.PYLIGHTNIX_SELF_TAG) are resolved. RConfig
stands for 'Resolved Config'.

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
BuildArgs = NamedTuple('BuildArgs', [('S',Optional[StorageSettings]),
                                     ('dre ...
```


<a name="pylightnix.types.Build"></a>
## `Build` Objects

```python
def __init__(self, ba: BuildArgs) -> None
```

Build objects track the process of stage's
[realization](#pylightnix.core.realize1). Build allows users to define
[Realizers](#pylightnix.types.Realizer) with only a simple one-argument
signature. The [build_wrapper](#pylightnix.core.build_wrapper) function
converts simplified Build-realizers into the regular ones.

Typical Build operations include:

- [build_config](#pylightnix.core.build_config) - Obtain the RConfig object of
  the current stage
- [build_cattrs](#pylightnix.core.build_cattrs) - Obtain the ConfigAttrs
  helper
- [build_path](#pylightnix.core.build_path) - Convert a RefPath or a
  self-ref path
  into a system file path
- [build_setoutgroups](#pylightnix.build.build_setoutgroups) - Initialize and
  return groups of output folders
- [build_deref](#pylightnix.core.build_deref) - Convert a dependency DRef
  into a realization reference.

[Lenses](#pylightnix.lens.Lens) accept `Build` objects as a configuration
source for derivations being realized.

Build class may be subclassed by applications in order to define
application-specific build-state.  Underscoped
[build_wrapper_](#pylightnix.core.build_wrapper_) accepts additional callback
parameter which informs the core what subclass to create. Note that derived
classes should have the same constructor `def __init__(self,
ba:BuildArgs)->None`.

Example:
```python
class TensorFlowModel(Build):
  model:tf.keras.Model

def train(r:TensorFlowModel)->None:
  o = build_outpath(r)
  r.model = create_model(...)
  ...

def mymodel(r:Registry)->DRef:
  return mkdrv(r, ..., build_wrapper_(TensorFlowModel, train))
```

<a name="pylightnix.types.Build.__init__"></a>
### `Build.__init__()`

```python
def __init__(self, ba: BuildArgs) -> None
```


<a name="pylightnix.types.Registry"></a>
## `Registry` Objects

```python
def __init__(self, S: Optional[StorageSettings] = None)
```

The derivation registry is a mutable storage object where Pylightnix
stores derivations before combining them into a
[Closure](#pylightnix.types.Closure).

Registry doesn't requre any special operations besides creating and passing
around. By convention, Registry objects are first arguments of user-defined
stage functions and the `mkdrv` API function of Pylightnix.

<a name="pylightnix.types.Registry.__init__"></a>
### `Registry.__init__()`

```python
def __init__(self, S: Optional[StorageSettings] = None)
```


<a name="pylightnix.types.DRefLike"></a>
## `DRefLike`

```python
DRefLike = TypeVar('DRefLike',bound=DRef)
```


<a name="pylightnix.types.StageResult"></a>
## `StageResult`

```python
StageResult = Union[DRef,List[DRef],Dict[Any,DRef],Tuple[DRef,...]]
```


<a name="pylightnix.types.Stage"></a>
## `Stage`

```python
Stage = Callable[...,StageResult]
```

Functions with the `Stage` signature are the top-level building blocks of
Pylightnix. Stage functions call [mkdrv](#pylightnix.core.mkdrv) and each
other to produce linked [Derivations](#pylightnix.types.Derivation) and
register them in the [Registry](#pylightnix.types.Registry).

Some built-in stages are:
- [mknode](#pylightnix.stages.trivial.mknode)
- [mkfile](#pylightnix.stages.trivial.mkfile)
- [fetchurl](#pylightnix.stages.fetchurl.fetchurl)

Note: Real stages often accept additional custom arguments which AFAIK
couldn't be handled by the simple MyPy. In a somewhat extended MyPy the Stage
definition would look like:

```Python
Stage = Callable[[Registry,VarArg(Any),KwArg(Any)],DRef]
```

Stage's return value is a [derivation reference](#pylightnix.types.DRef)
which could be either used in other stages, or
[instantiated](#pylightnix.core.instantiate) into the stage realization plan.

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

<a name="pylightnix.core.PYLIGHTNIX_NAMEPAT"></a>
## `PYLIGHTNIX_NAMEPAT`

```python
PYLIGHTNIX_NAMEPAT = "[a-zA-Z0-9_-]"
```

Set the regular expression pattern for valid name characters.

<a name="pylightnix.core.PYLIGHTNIX_RESERVED"></a>
## `PYLIGHTNIX_RESERVED`

```python
PYLIGHTNIX_RESERVED = ['context.json','group.json']
```

Reserved file names are treated specially be the core. Users should
not normally create or alter files with these names.

<a name="pylightnix.core.logger"></a>
## `logger`

```python
logger = getLogger(__name__)
```


<a name="pylightnix.core.info"></a>
## `info`

```python
info = logger.info
```


<a name="pylightnix.core.warning"></a>
## `warning`

```python
warning = logger.warning
```


<a name="pylightnix.core.TL"></a>
## `TL`

```python
TL = threading_local()
```

Thread-local storage for [current_registry](#pylightnix.core.current_registry)
to store its state.

<a name="pylightnix.core.tlregistry"></a>
## `tlregistry()`

```python
def tlregistry(M: Optional[Registry]) -> Optional[Registry]
```

Return the currently active [Registry](#pylightnix.types.Registry)

<a name="pylightnix.core.tlstorage"></a>
## `tlstorage()`

```python
def tlstorage(S: Optional[StorageSettings]) -> Optional[StorageSettings]
```

Return the currently active
[StorageSettings](#pylightnix.types.StorageSettings)

<a name="pylightnix.core.storagename"></a>
## `storagename()`

```python
def storagename()
```

Return the name of Pylightnix storage filder.

<a name="pylightnix.core.fsroot"></a>
## `fsroot()`

```python
def fsroot(S: Optional[StorageSettings] = None) -> Path
```

`fsroot` contains the path to the root of pylightnix shared data folder.
Default is `~/_pylightnix` or `/var/run/_pylightnix` if no `$HOME` is
available.  Setting `PYLIGHTNIX_ROOT` environment variable overwrites the
defaults.

<a name="pylightnix.core.fstmpdir"></a>
## `fstmpdir()`

```python
def fstmpdir(S: Optional[StorageSettings] = None) -> Path
```

Return the location of current Pylightnix temporary folder, defaulting to
the path set by PYLIGHTNIX_TMP environment variable.

<a name="pylightnix.core.fsstorage"></a>
## `fsstorage()`

```python
def fsstorage(S: Optional[StorageSettings] = None) -> Path
```

Return the location of current Pylightnix storage folder, defaulting to
the path set by PYLIGHTNIX_STORAGE environment variable.

<a name="pylightnix.core.assert_valid_storage"></a>
## `assert_valid_storage()`

```python
def assert_valid_storage(S: Optional[StorageSettings] = None) -> None
```


<a name="pylightnix.core.mkSS"></a>
## `mkSS()`

```python
def mkSS(root: str, stordir: Optional[str] = None, tmpdir: Optional[str] = None) -> StorageSettings
```

Constructor for [StorageSettings](#pylightnix.types.StorageSettings)

<a name="pylightnix.core.setstorage"></a>
## `setstorage()`

```python
def setstorage(S: Optional[StorageSettings]) -> Optional[StorageSettings]
```


<a name="pylightnix.core.setregistry"></a>
## `setregistry()`

```python
def setregistry(r: Optional[Registry]) -> Optional[Registry]
```


<a name="pylightnix.core.fsinit"></a>
## `fsinit()`

```python
def fsinit(ss: Optional[Union[str,StorageSettings]] = None, check_not_exist: bool = False, remove_existing: bool = False, use_as_default: bool = False) -> None
```

Imperatively create the filesystem storage and temp direcory if they don't
exist.  Default locations may be altered by `PYLIGHTNIX_STORAGE` and
`PYLIGHTNIX_TMP` env variables.

<a name="pylightnix.core.reserved"></a>
## `reserved()`

```python
def reserved(folder: Path, name: str) -> Path
```


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


<a name="pylightnix.core.path2dref"></a>
## `path2dref()`

```python
def path2dref(p: Path) -> Optional[DRef]
```

Takes either a system path of some realization in the Pylightnix storage
or a symlink pointing to such path. Return a `DRef` which corresponds to this
path.

Note: `path2dref` operates on `p` symbolically. It doesn't actually check the
presence of such an object in storage

<a name="pylightnix.core.path2rref"></a>
## `path2rref()`

```python
def path2rref(p: Path) -> Optional[RRef]
```

Takes either a system path of some realization in the Pylightnix storage
or a symlink pointing to such path. Return `RRef` which corresponds to this
path.

Note: `path2rref` operates on `p` symbolically. It doesn't actually check the
presence of such an object in storage

<a name="pylightnix.core.mkconfig"></a>
## `mkconfig()`

```python
def mkconfig(d: dict) -> Config
```

Create a [Config](#pylightnix.types.Config) object out of config
dictionary. Asserts if the dictionary is not JSON-compatible. As a handy hack,
filter out `r:Registry` variable which likely is an utility
[Registry](#pylightnix.types.Registry) object.

<a name="pylightnix.core.cfgdict"></a>
## `cfgdict()`

```python
def cfgdict(cp: Config) -> dict
```


<a name="pylightnix.core.cfgcattrs"></a>
## `cfgcattrs()`

```python
def cfgcattrs(c: RConfig) -> Any
```


<a name="pylightnix.core.cfgserialize"></a>
## `cfgserialize()`

```python
def cfgserialize(c: Config) -> str
```


<a name="pylightnix.core.cfghash"></a>
## `cfghash()`

```python
def cfghash(c: Config) -> Hash
```


<a name="pylightnix.core.cfgname"></a>
## `cfgname()`

```python
def cfgname(c: Config) -> Name
```

Return a `name` field of a config `c`, defaulting to string "unnmaed".

<a name="pylightnix.core.cfgdeps"></a>
## `cfgdeps()`

```python
def cfgdeps(c: Config) -> Set[DRef]
```


<a name="pylightnix.core.mkrefpath"></a>
## `mkrefpath()`

```python
def mkrefpath(r: DRef, items: List[str] = []) -> RefPath
```

Construct a [RefPath](#pylightnix.types.RefPath) out of a reference `ref`
and a path within the stage's realization

<a name="pylightnix.core.resolve"></a>
## `resolve()`

```python
def resolve(c: Config, r: DRef) -> RConfig
```

Replace all Promise tags with DRef `r`. In particular, all PromisePaths
are converted into RefPaths.

<a name="pylightnix.core.dref2path"></a>
## `dref2path()`

```python
def dref2path(r: DRef, S=None) -> Path
```


<a name="pylightnix.core.rref2path"></a>
## `rref2path()`

```python
def rref2path(r: RRef, S=None) -> Path
```


<a name="pylightnix.core.rrefpath2path"></a>
## `rrefpath2path()`

```python
def rrefpath2path(r: RRef, refpath: RefPath, S=None) -> Path
```


<a name="pylightnix.core.drefcfgpath"></a>
## `drefcfgpath()`

```python
def drefcfgpath(r: DRef, S=None) -> Path
```


<a name="pylightnix.core.rrefctx"></a>
## `rrefctx()`

```python
def rrefctx(r: RRef, S=None) -> Context
```

Return the realization context.

<a name="pylightnix.core.drefcfg_"></a>
## `drefcfg_()`

```python
def drefcfg_(dref: DRef, S=None) -> Config
```

Return `dref` configuration, selfrefs are _not_ resolved

<a name="pylightnix.core.drefcfg"></a>
## `drefcfg()`

```python
def drefcfg(dref: DRef, S=None) -> RConfig
```

Return `dref` configuration, selfrefs are resolved

<a name="pylightnix.core.drefattrs"></a>
## `drefattrs()`

```python
def drefattrs(r: DRef, S=None) -> Any
```

Read the [ConfigAttrs](#pylightnix.types.ConfigAttr) of the storage node `r`.
Note, that it is a kind of 'syntactic sugar' for `drefcfg`. Both
functions do the same thing.

<a name="pylightnix.core.rrefattrs"></a>
## `rrefattrs()`

```python
def rrefattrs(r: RRef, S=None) -> Any
```

Read the [ConfigAttrs](#pylightnix.types.ConfigAttr) of the storage node `r`.
Note, that it is a kind of 'syntactic sugar' for `drefcfg`. Both
functions do the same thing.

<a name="pylightnix.core.drefdeps1"></a>
## `drefdeps1()`

```python
def drefdeps1(drefs: Iterable[DRef], S=None) -> Set[DRef]
```

Return a set of reference's immediate dependencies, not including `drefs`
themselves.

<a name="pylightnix.core.rrefdeps1"></a>
## `rrefdeps1()`

```python
def rrefdeps1(rrefs: Iterable[RRef], S=None) -> Set[RRef]
```

Return a set of reference's immediate dependencies, not including `rrefs`
themselves.

<a name="pylightnix.core.drefdeps"></a>
## `drefdeps()`

```python
def drefdeps(drefs: Iterable[DRef], S=None) -> Set[DRef]
```

Return the complete set of `drefs`'s dependencies, not including `drefs`
themselves.

<a name="pylightnix.core.rrefdeps"></a>
## `rrefdeps()`

```python
def rrefdeps(rrefs: Iterable[RRef], S=None) -> Set[RRef]
```

Return the complete set of rrefs's dependencies, not including `rrefs`
themselves.

TODO: Validate the property that the resulting set IS the minimal complete
set of RRef dependencies. Now it looks so only by creation (see `realizeSeq`,
line mark `I`)

<a name="pylightnix.core.alldrefs"></a>
## `alldrefs()`

```python
def alldrefs(S=None) -> Iterable[DRef]
```

Iterates over all derivations of the storage located at `S`
(PYLIGHTNIX_STORE env is used by default)

<a name="pylightnix.core.allrrefs"></a>
## `allrrefs()`

```python
def allrrefs(S=None) -> Iterable[RRef]
```

Iterates over all realization references in `S` (PYLIGHTNIX_STORE env is
used by default)

<a name="pylightnix.core.rootdrefs"></a>
## `rootdrefs()`

```python
def rootdrefs(S: Optional[StorageSettings] = None) -> Set[DRef]
```

Return root DRefs of the storage `S` as a set

<a name="pylightnix.core.rootrrefs"></a>
## `rootrrefs()`

```python
def rootrrefs(S: Optional[StorageSettings] = None) -> Set[RRef]
```

Return root RRefs of the storage `S` as a set

<a name="pylightnix.core.rrefdata"></a>
## `rrefdata()`

```python
def rrefdata(rref: RRef, S=None) -> Iterable[Path]
```

Iterate over top-level artifacts paths, ignoring reserved files.

<a name="pylightnix.core.drefrrefs"></a>
## `drefrrefs()`

```python
def drefrrefs(dref: DRef, S=None) -> Set[RRef]
```

Iterate over all realizations of a derivation `dref`. The sort order is
unspecified. Matchers are not taken into account.

<a name="pylightnix.core.drefrrefsC"></a>
## `drefrrefsC()`

```python
def drefrrefsC(dref: DRef, context: Context, S=None) -> Iterable[RRef]
```

Iterate over realizations of a derivation `dref` that match the specified
[context](#pylightnix.types.Context). Sorting order is unspecified.

<a name="pylightnix.core.store_gc"></a>
## `store_gc()`

```python
def store_gc(keep_drefs: List[DRef], keep_rrefs: List[RRef], S: Optional[StorageSettings] = None) -> Tuple[Set[DRef],Set[RRef]]
```

Take roots which are in use and should not be removed. Return roots which
are not used and may be removed. Actual removing is to be done by the user.

Default location of `S` may be changed.

See also [rmref](#pylightnix.bashlike.rmref)

<a name="pylightnix.core.mkdrv_"></a>
## `mkdrv_()`

```python
def mkdrv_(c: Config, S=None) -> DRef
```

See [mkdrv](#pylightnix.core.mkdrv)

<a name="pylightnix.core.mkrealization"></a>
## `mkrealization()`

```python
def mkrealization(dref: DRef, l: Context, o: Path, S=None) -> RRef
```

Inserts the newly-obtaind [Stage](#pylightnix.types.Stage) artifacts into
the Storage, return the [realization reference](#pylightnix.types.RRef). Not
intended to be called by user.

Parameters:
- `dref:DRef`: Derivation reference to create the realization of.
- `l:Context`: Context which stores dependency information.
- `o:Path`: Path to temporal (build) folder which contains artifacts,
  prepared by the [Realizer](#pylightnix.types.Realizer).
- `leader`: Tag name and Group identifier of the Group leader. By default,
  we use name `out` and derivation's own rref.

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
def context_add(ctx: Context, dref: DRef, rrefs: List[RRef]) -> Context
```

Add a pair `(dref,rrefs)` into a context `ctx`. `rrefs` are supposed to
form (a subset of) the realizations of `dref`.
Return a new context.

<a name="pylightnix.core.context_deref"></a>
## `context_deref()`

```python
def context_deref(context: Context, dref: DRef) -> List[RRef]
```

TODO: Should it return Output (aka `UniformList`) rather than Python list?

<a name="pylightnix.core.context_derefpath"></a>
## `context_derefpath()`

```python
def context_derefpath(context: Context, refpath: RefPath, S=None) -> List[Path]
```


<a name="pylightnix.core.context_serialize"></a>
## `context_serialize()`

```python
def context_serialize(c: Context) -> str
```


<a name="pylightnix.core.output_validate"></a>
## `output_validate()`

```python
def output_validate(dref: DRef, o: Output[Path], S=None) -> List[Path]
```


<a name="pylightnix.core.output_realizer"></a>
## `output_realizer()`

```python
def output_realizer(f: RealizerO) -> Realizer
```


<a name="pylightnix.core.output_matcher"></a>
## `output_matcher()`

```python
def output_matcher(r: MatcherO) -> Matcher
```


<a name="pylightnix.core.mkdrv"></a>
## `mkdrv()`

```python
def mkdrv(config: Config, matcher: Matcher, realizer: Realizer, r: Optional[Registry] = None) -> DRef
```

Construct a [Derivation](#pylightnix.types.Derivation) object out of
[Config](#pylightnix.types.Config), [Matcher](#pylightnix.types.Matcher) and
[Realizer](#pylightnix.types.Realizer). Register the derivation in the
dependency-resolution [Registry](#pylightnix.types.Registry). Return [Derivation
references](#pylightnix.types.DRef) of the newly-obtained derivation.

Arguments:
- `r:Registry`: A Registry to update with a new derivation

Example:
```python
def somestage(r:Registry)->DRef:
  def _realizer(b:Build):
    with open(join(build_outpath(b),'artifact'),'w') as f:
      f.write(...)
  return mkdrv(r,mkconfig({'name':'mystage'}), match_only(), build_wrapper(_realizer))

rref:RRef=realize1(instantiate(somestage))
```

<a name="pylightnix.core.current_registry"></a>
## `current_registry()`

```python
@contextmanager
def current_registry(r: Registry) -> Iterator[Registry]
```

Sets the default global [Registry](#pylightnix.types.Registry) for the
inner scoped code. Internally calls
[current_storage(r.S)](#pylightnix.core.current_storage)

<a name="pylightnix.core.current_storage"></a>
## `current_storage()`

```python
@contextmanager
def current_storage(S: Optional[StorageSettings]) -> Iterator[Optional[StorageSettings]]
```

Sets the global default
[StorageSettings](#pylightnix.types.StorageSettings) for the inner scoped code

<a name="pylightnix.core.mkclosure"></a>
## `mkclosure()`

```python
def mkclosure(result: Any, r: Registry) -> Closure
```


<a name="pylightnix.core._A"></a>
## `_A`

```python
_A = TypeVar('_A')
```


<a name="pylightnix.core.instantiate"></a>
## `instantiate()`

```python
def instantiate(stage: Union[_A,Callable[...,Any]], args: Any, *,, ,, =, ,, =, ,, kwargs: Any) -> Tuple[_A,Closure]
```

Instantiate scans a Python data object (list,dict or constant) which
contains [DRef](#pylightnix.types.DRef) or evaluates a
[Stage](#pylightnix.types.Stage) function by calling it.

Returns a ready-to be realized [Closure](#pylightnix.types.Closure) formed out
of nested [Derivations](#pylightnix.types.Derivation).

See also [realize](#pylightnix.core.realize).

<a name="pylightnix.core.RealizeSeqGen"></a>
## `RealizeSeqGen`

```python
RealizeSeqGen = Generator[
  Tuple[Optional[StorageSettings],DRef,Context,Derivation,RealizeArg],
  Tuple[Optional[L ...
```


<a name="pylightnix.core.realize1"></a>
## `realize1()`

```python
def realize1(closure: Union[Closure,Tuple[StageResult,Closure]], force_rebuild: Union[List[DRef],bool] = [], assert_realized: List[DRef] = [], realize_args: Dict[DRef,RealizeArg] = {}) -> RRef
```

realize1 gets the results of building the [Stage](#pylightnix.types.Stage).
Returns either the [matching](#pylightnix.types.Matcher) realizations
immediately, or launches the user-defined [realization
procedure](#pylightnix.types.Realizer).

Example:
```python
def mystage(r:Registry)->DRef:
  ...
  return mkdrv(r, ...)

rrefs=realize1(instantiate(mystage))
print(mklen(rref).syspath)
```

Pylightnix contains the following specialized alternatives to `realize1`:

* [realizeMany](#pylightnix.core.realizeMany) - A version for multiple-output
stages.
* [repl_realize](#pylightnix.repl.repl_realize) - A REPL-friendly version.
  version which uses a hardcoded global [Registry](#pylightnix.types.Registry).

<a name="pylightnix.core.realizeMany"></a>
## `realizeMany()`

```python
def realizeMany(closure: Union[Closure,Tuple[StageResult,Closure]], force_rebuild: Union[List[DRef],bool] = [], assert_realized: List[DRef] = [], realize_args: Dict[DRef,RealizeArg] = {}) -> List[RRef]
```


<a name="pylightnix.core.realize"></a>
## `realize()`

```python
def realize(closure: Union[Closure,Tuple[StageResult,Closure]], force_rebuild: Union[List[DRef],bool] = [], assert_realized: List[DRef] = [], realize_args: Dict[DRef,RealizeArg] = {}) -> Tuple[StageResult,Closure,Context]
```

Takes the instantiated [Closure](#pylightnix.types.Closure) and returns
its value together with the realization [Context](#pylightnix.types.Context).
Calls the derivation realizers if their matchers require so.

See also [repl_realize](#pylightnix.repl.repl_realize)

<a name="pylightnix.core.realizeSeq"></a>
## `realizeSeq()`

```python
def realizeSeq(closure: Closure, force_interrupt: List[DRef] = [], assert_realized: List[DRef] = [], realize_args: Dict[DRef,RealizeArg] = {}) -> RealizeSeqGen
```

`realizeSeq` encodes low-level details of the realization algorithm.
Sequentially realize the closure by issuing steps via Python's generator
interface. Consider calling [realize](#pylightnix.core.realize) or it's
analogs instead.

FIXME: try to implement `assert_realized` by calling `redefine` with
appropriate failing realizer on every Derivation.

<a name="pylightnix.core.evaluate"></a>
## `evaluate()`

```python
def evaluate(stage, args, *,, ,, kwargs) -> RRef
```


<a name="pylightnix.core.Key"></a>
## `Key`

```python
Key = Callable[[Optional[StorageSettings], RRef],Optional[Union[int,float,str]]]
```


<a name="pylightnix.core.texthash"></a>
## `texthash()`

```python
def texthash() -> Key
```


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


<a name="pylightnix.core.match"></a>
## `match()`

```python
def match(key: Key, trim: Callable[[List[RRef]],Optional[List[RRef]]], mnext: Optional[Matcher] = None) -> Matcher
```

Create a [Matcher](#pylightnix.types.Matcher) by combining different
sorting keys and selecting a top-n threshold.

Only realizations which have [tag](#pylightnix.types.Tag) 'out' (which is a
default tag name) participate in matching. After the matching, Pylightnix
adds all non-'out' realizations which share [group](#pylightnix.types.Group)
with at least one matched realization.

Arguments:
- `keys`: List of [Key](#pylightnix.types.Key) functions. Defaults ot

<a name="pylightnix.core.match_all"></a>
## `match_all()`

```python
def match_all(S, rrefs)
```


<a name="pylightnix.core.match_some"></a>
## `match_some()`

```python
def match_some(n: int = 1, key=None)
```


<a name="pylightnix.core.match_only"></a>
## `match_only()`

```python
def match_only()
```


<a name="pylightnix.core.match_latest"></a>
## `match_latest()`

```python
def match_latest(n: int = 1) -> Matcher
```


<a name="pylightnix.core.match_exact"></a>
## `match_exact()`

```python
def match_exact(rrefs: List[RRef])
```


<a name="pylightnix.core.cfgsp"></a>
## `cfgsp()`

```python
def cfgsp(c: Config) -> List[Tuple[str,RefPath]]
```

Returns the list of self-references (aka self-paths) in the config.

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


<a name="pylightnix.core.assert_rref_deps"></a>
## `assert_rref_deps()`

```python
def assert_rref_deps(c: Config) -> None
```


<a name="pylightnix.core.assert_have_realizers"></a>
## `assert_have_realizers()`

```python
def assert_have_realizers(r: Registry, drefs: List[DRef]) -> None
```


<a name="pylightnix.build"></a>
# `pylightnix.build`

Built-in realization wrapper named `Build` provides helpful functions like
temporary build directory management, time counting, etc.

<a name="pylightnix.build.logger"></a>
## `logger`

```python
logger = getLogger(__name__)
```


<a name="pylightnix.build.info"></a>
## `info`

```python
info = logger.info
```


<a name="pylightnix.build.warning"></a>
## `warning`

```python
warning = logger.warning
```


<a name="pylightnix.build.error"></a>
## `error`

```python
error = logger.error
```


<a name="pylightnix.build.BuildError"></a>
## `BuildError` Objects

```python
def __init__(self, S: Optional[StorageSettings], dref: DRef, outpaths: Optional[Output[Path]], exception: Exception, msg: str = '')
```

Exception class for build errors

<a name="pylightnix.build.BuildError.__init__"></a>
### `BuildError.__init__()`

```python
def __init__(self, S: Optional[StorageSettings], dref: DRef, outpaths: Optional[Output[Path]], exception: Exception, msg: str = '')
```

Initialize BuildError instance.

<a name="pylightnix.build.BuildError.__str__"></a>
### `BuildError.__str__()`

```python
def __str__(self)
```


<a name="pylightnix.build.mkbuildargs"></a>
## `mkbuildargs()`

```python
def mkbuildargs(S: Optional[StorageSettings], dref: DRef, context: Context, starttime: Optional[str], stoptime: Optional[str], iarg: InstantiateArg, rarg: RealizeArg) -> BuildArgs
```


<a name="pylightnix.build._B"></a>
## `_B`

```python
_B = TypeVar('_B', bound=Build)
```


<a name="pylightnix.build.build_wrapper_"></a>
## `build_wrapper_()`

```python
def build_wrapper_(f: Callable[[_B],None], ctr: Callable[[BuildArgs],_B], nouts: Optional[int] = 1, starttime: Optional[str] = 'AUTO', stoptime: Optional[str] = 'AUTO') -> Realizer
```

Build Adapter which convers user-defined realizers which use
[Build](#pylightnix.types.Build) API into a low-level
[Realizer](#pylightnix.types.Realizer)

<a name="pylightnix.build.build_wrapper"></a>
## `build_wrapper()`

```python
def build_wrapper(f: Callable[[Build],None], nouts: Optional[int] = 1, starttime: Optional[str] = 'AUTO', stoptime: Optional[str] = 'AUTO') -> Realizer
```

Build Adapter which convers user-defined realizers which use
[Build](#pylightnix.types.Build) API into a low-level
[Realizer](#pylightnix.types.Realizer)

<a name="pylightnix.build.build_config"></a>
## `build_config()`

```python
def build_config(b: Build) -> RConfig
```

Return the [Config](#pylightnix.types.RConfig) object of the realization
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

<a name="pylightnix.build.build_markstart"></a>
## `build_markstart()`

```python
def build_markstart(b: Build, nouts: int) -> List[Path]
```


<a name="pylightnix.build.build_markstop"></a>
## `build_markstop()`

```python
def build_markstop(b: Build) -> None
```


<a name="pylightnix.build.build_markstop_noexcept"></a>
## `build_markstop_noexcept()`

```python
def build_markstop_noexcept(b: Build) -> None
```


<a name="pylightnix.build.rrefbstart"></a>
## `rrefbstart()`

```python
def rrefbstart(rref: RRef, S=None) -> Optional[str]
```

Return the buildtime of the current RRef in a format specified by the
[PYLIGHTNIX_TIME](#pylightnix.utils.PYLIGHTNIX_TIME) constant.

[parsetime](#pylightnix.utils.parsetime) may be used to parse stings into
UNIX-Epoch seconds.

Buildtime is the time when the realization process was started. Some
realizations may not provide this information.

<a name="pylightnix.build.rrefbstop"></a>
## `rrefbstop()`

```python
def rrefbstop(rref: RRef, S=None) -> Optional[str]
```

Return the buildtime of the current RRef in a format specified by the
[PYLIGHTNIX_TIME](#pylightnix.utils.PYLIGHTNIX_TIME) constant.

[parsetime](#pylightnix.utils.parsetime) may be used to parse stings into
UNIX-Epoch seconds.

Buildtime is the time when the realization process was started. Some
realizations may not provide this information.

<a name="pylightnix.build.rrefbdelta"></a>
## `rrefbdelta()`

```python
def rrefbdelta(rref: RRef, S=None) -> Optional[float]
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

For any [realization](#pylightnix.core.realize1) process described with
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


<a name="pylightnix.build.build_path"></a>
## `build_path()`

```python
def build_path(b: Build, refpath: RefPath) -> Path
```

A single-realization version of the
[build_paths](#pylightnix.build.build_paths).

<a name="pylightnix.build.build_environ"></a>
## `build_environ()`

```python
def build_environ(b: Build, env: Optional[Any] = None) -> dict
```

Prepare environment by adding Build's config to the environment as
variables. The function resolves all singular RefPaths into system paths
using current Build's context.

FIXME: Use bash-array syntax for multi-ouput paths

<a name="pylightnix.build.repl_continueBuild"></a>
## `repl_continueBuild()`

```python
def repl_continueBuild(b: Build, rh: Optional[ReplHelper] = None) -> Optional[RRef]
```


<a name="pylightnix.build.repl_buildargs"></a>
## `repl_buildargs()`

```python
def repl_buildargs(rh: Optional[ReplHelper] = None) -> BuildArgs
```


<a name="pylightnix.build.repl_build"></a>
## `repl_build()`

```python
def repl_build(rh: Optional[ReplHelper] = None, nouts: Optional[int] = 1) -> Build
```

Return `Build` object for using in repl-based debugging

Example:
```
from stages import some_stage, some_stage_build, some_stage_train

rh=repl_realize(instantiate(some_stage))
b=repl_build(rh)
some_stage_build(b) # Debug as needed
some_stage_train(b) # Debug as needed
```

<a name="pylightnix.build.repl_cancelBuild"></a>
## `repl_cancelBuild()`

```python
def repl_cancelBuild(b: Build, rh: Optional[ReplHelper] = None) -> None
```


<a name="pylightnix.repl"></a>
# `pylightnix.repl`

Repl module defines variants of `instantiate` and `realize1` functions, which
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


<a name="pylightnix.repl.repl_continueAll"></a>
## `repl_continueAll()`

```python
def repl_continueAll(out_paths: Optional[List[Path]] = None, out_rrefs: Optional[List[RRef]] = None, rh: Optional[ReplHelper] = None) -> Optional[Context]
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


<a name="pylightnix.repl.repl_realize"></a>
## `repl_realize()`

```python
def repl_realize(closure: Union[Closure,Tuple[Any,Closure]], force_interrupt: Union[List[DRef],bool] = True, realize_args: Dict[DRef,RealizeArg] = {}) -> ReplHelper
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

<a name="pylightnix.repl.repl_result"></a>
## `repl_result()`

```python
def repl_result(rh: ReplHelper) -> Optional[Context]
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


<a name="pylightnix.repl.repl_cancel"></a>
## `repl_cancel()`

```python
def repl_cancel(rh: Optional[ReplHelper] = None) -> None
```


<a name="pylightnix.stages"></a>
# `pylightnix.stages`


<a name="pylightnix.stages.trivial"></a>
# `pylightnix.stages.trivial`

Trivial builtin stages

<a name="pylightnix.stages.trivial.mknode"></a>
## `mknode()`

```python
def mknode(r: Registry, cfgdict: dict, artifacts: Dict[Name,bytes] = {}, name: str = 'mknode') -> DRef
```


<a name="pylightnix.stages.trivial.redefine"></a>
## `redefine()`

```python
def redefine(stage: Any, new_config: Callable[[dict],None] = lambda x:None, new_matcher: Optional[Matcher] = None, new_realizer: Optional[Realizer] = None) -> Any
```

Define a new Derivation based on the existing one, by updating it's
config, optionally re-writing it's matcher, or it's realizer.

Arguments:
- `stage:Any` a `Stage` function, accepting arbitrary keyword arguments
- `new_config:Callable[[dict],None]` A function to update the `dref`'s config.
  Default varsion makes no changes.
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
realize1(instantiate(redefine(myMLmodel, _new_config)))
```

FIXME: Updating configs is dangerous: it changes its dref and thus breaks
dependencies. Only top-level stages should use `new_confid` currently.

<a name="pylightnix.stages.trivial.realized"></a>
## `realized()`

```python
def realized(stage: Any) -> Stage
```

Asserts that the stage doesn't requre running its realizer.
[Re-defines](#pylightnix.stages.trivial.redefine) stage realizer with a dummy
realizer triggering an assertion.

Example:
```python
rref:RRef=realize1(instantiate(realized(my_long_running_stage, arg="bla")))
# ^^^ Fail if `my_long_running_stage` is not yet realized.
```

<a name="pylightnix.stages.fetch2"></a>
# `pylightnix.stages.fetch2`

Builtin stages for fetching things from the Internet

<a name="pylightnix.stages.fetch2.logger"></a>
## `logger`

```python
logger = getLogger(__name__)
```


<a name="pylightnix.stages.fetch2.info"></a>
## `info`

```python
info = logger.info
```


<a name="pylightnix.stages.fetch2.error"></a>
## `error`

```python
error = logger.error
```


<a name="pylightnix.stages.fetch2.CURL"></a>
## `CURL`

```python
CURL = try_executable('curl',
                    'PYLIGHTNIX_CURL',
                    '`curl` executable ...
```


<a name="pylightnix.stages.fetch2.AUNPACK"></a>
## `AUNPACK`

```python
AUNPACK = try_executable('aunpack',
                       'PYLIGHTNIX_AUNPACK',
                       '`aunp ...
```


<a name="pylightnix.stages.fetch2.fetchurl2"></a>
## `fetchurl2()`

```python
def fetchurl2(url: str, sha256: Optional[str] = None, sha1: Optional[str] = None, name: Optional[str] = None, filename: Optional[str] = None, force_download: bool = False, r: Optional[Registry] = None, kwargs) -> DRef
```

Download file given it's URL addess.

Downloading is done by calling `curl` application. The path to the executable
may be altered by setting the `PYLIGHTNIX_CURL` environment variable.

Agruments:
- `r:Registry` the dependency resolution [Registry](#pylightnix.types.Registry).
- `url:str` URL to download from. Should point to a single file.
- `sha256:str` SHA-256 hash sum of the file.
- `name:Optional[str]`: Name of the Derivation. The stage will attempt to
  deduce the name if not specified.
- `filename:Optional[str]=None` Name of the filename on disk after downloading.
  Stage will attempt to deduced it if not specified.
- `force_download:bool=False` If False, resume the last download if
  possible.
- `check_promises:bool=True` Passed to `mkdrv` as-is.

Example:
```python
def hello_src(r:Registry)->DRef:
  hello_version = '2.10'
  return fetchurl2(
    r,
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b')

rref:RRef=realize1(instantiate(hello_src))
print(rref2path(rref))
```

<a name="pylightnix.stages.fetch2.unpack"></a>
## `unpack()`

```python
def unpack(path: Optional[str] = None, refpath: Optional[RefPath] = None, name: Optional[str] = None, sha256: Optional[str] = None, sha1: Optional[str] = None, aunpack_args: List[str] = [], r: Optional[Registry] = None, kwargs) -> DRef
```


<a name="pylightnix.stages.fetch"></a>
# `pylightnix.stages.fetch`

Builtin stages for fetching things from the Internet

<a name="pylightnix.stages.fetch.logger"></a>
## `logger`

```python
logger = getLogger(__name__)
```


<a name="pylightnix.stages.fetch.info"></a>
## `info`

```python
info = logger.info
```


<a name="pylightnix.stages.fetch.error"></a>
## `error`

```python
error = logger.error
```


<a name="pylightnix.stages.fetch.WGET"></a>
## `WGET`

```python
WGET = try_executable('wget',
                    'PYLIGHTNIX_WGET',
                    'Executable `wget` ...
```


<a name="pylightnix.stages.fetch.AUNPACK"></a>
## `AUNPACK`

```python
AUNPACK = try_executable('aunpack',
                       'PYLIGHTNIX_AUNPACK',
                       '`aunp ...
```


<a name="pylightnix.stages.fetch._unpack_inplace"></a>
## `_unpack_inplace()`

```python
def _unpack_inplace(o: str, fullpath: str, remove_file: bool)
```


<a name="pylightnix.stages.fetch.fetchurl"></a>
## `fetchurl()`

```python
def fetchurl(url: str, sha256: Optional[str] = None, sha1: Optional[str] = None, mode: str = 'unpack,remove', name: Optional[str] = None, filename: Optional[str] = None, force_download: bool = False, check_promises: bool = True, r: Optional[Registry] = None, kwargs) -> DRef
```

Download and unpack an URL addess.

Downloading is done by calling `wget` application. Optional unpacking is
performed with the `aunpack` script from `atool` package. `sha256` defines the
expected SHA-256 hashsum of the stored data. `mode` allows to tweak the
stage's behavior: adding word 'unpack' instructs fetchurl to unpack the
package, adding 'remove' instructs it to remove the archive after unpacking.

If 'unpack' is not expected, then the promise named 'out_path' is created.

Agruments:
- `r:Registry` the dependency resolution [Registry](#pylightnix.types.Registry).
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
def hello_src(r:Registry)->DRef:
  hello_version = '2.10'
  return fetchurl(
    r,
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b')

rref:RRef=realize1(instantiate(hello_src))
print(rref2path(rref))
```

<a name="pylightnix.stages.fetch.fetchlocal"></a>
## `fetchlocal()`

```python
def fetchlocal(sha256: str, path: Optional[str] = None, envname: Optional[str] = None, mode: str = 'unpack,remove', name: Optional[str] = None, filename: Optional[str] = None, check_promises: bool = True, r: Optional[Registry] = None, kwargs) -> DRef
```

Copy local file into Pylightnix storage. This function is typically
intended to register application-specific files which are distributed with a
source repository.

See `fetchurl` for arguments description.

If 'unpack' is not expected, then the promise named 'out_path' is created.

FIXME: Switch regular `fetchurl` to `curl` and call it with `file://` URLs.

<a name="pylightnix.bashlike"></a>
# `pylightnix.bashlike`

Simple functions imitating unix shell tools.

<a name="pylightnix.bashlike.lsdref_"></a>
## `lsdref_()`

```python
def lsdref_(r: DRef, S=None) -> Iterable[str]
```


<a name="pylightnix.bashlike.lsrref_"></a>
## `lsrref_()`

```python
def lsrref_(r: RRef, fn: List[str] = [], S=None) -> Iterable[str]
```


<a name="pylightnix.bashlike.lsrref"></a>
## `lsrref()`

```python
def lsrref(r: RRef, fn: List[str] = [], S=None) -> List[str]
```


<a name="pylightnix.bashlike.lsref"></a>
## `lsref()`

```python
def lsref(r: Union[RRef,DRef], S=None) -> List[str]
```

List the contents of `r`. For [DRefs](#pylightnix.types.DRef), return
realization hashes. For [RRefs](#pylightnix.types.RRef), list artifact files.

<a name="pylightnix.bashlike.catrref_"></a>
## `catrref_()`

```python
def catrref_(r: RRef, fn: List[str], S=None) -> Iterable[str]
```


<a name="pylightnix.bashlike.catref"></a>
## `catref()`

```python
def catref(r: Union[RRef,RefPath,Path], fn: List[str] = [], S=None) -> List[str]
```

Return the contents of r's artifact line by line. `fn` is a list of
folders, relative to rref's root.

<a name="pylightnix.bashlike.rmref"></a>
## `rmref()`

```python
def rmref(r: Union[RRef,DRef], S=None) -> None
```

Forcebly remove a reference from the storage. Removing
[DRefs](#pylightnix.types.DRef) also removes all their realizations.

Currently Pylightnix makes no attempts to synchronize an access to the
storage. In scenarious involving parallelization, users are expected to take
care of possible race conditions.

<a name="pylightnix.bashlike.shell"></a>
## `shell()`

```python
def shell(r: Union[RRef,DRef,Build,Path,str,None] = None, S=None) -> None
```

Open the Unix Shell in the directory associated with the argument passed.
Path to the shell executable is read from the `SHELL` environment variable,
defaulting to `/bin/sh`. If `r` is None, open the shell in the root of the
Pylightnix storage.

The function is expected to be run in REPL Python shells like IPython.

<a name="pylightnix.bashlike.shellref"></a>
## `shellref()`

```python
def shellref(r: Union[RRef,DRef,None] = None, S=None) -> None
```

Alias for [shell](#pylightnix.bashlike.shell). Deprecated.

<a name="pylightnix.bashlike.du"></a>
## `du()`

```python
def du(S=None) -> Dict[DRef,Tuple[int,Dict[RRef,int]]]
```

Calculates the disk usage, in bytes. For every derivation, return it's
total disk usage and disk usages per realizations. Note, that total disk usage
of a derivation is slightly bigger than sum of it's realization's usages.

<a name="pylightnix.bashlike.find"></a>
## `find()`

```python
def find(name: Optional[Union[Stage,str]] = None, newer: Optional[float] = None, S: Optional[StorageSettings] = None) -> List[RRef]
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
def diff(stageA: Union[RRef,DRef,Stage], stageB: Union[RRef,DRef,Stage], S=None) -> None
```

Run system's `diff` utility to print the difference between configs of 2
stages passed.

Note: if argument is a Stage, it is instantiated first

<a name="pylightnix.bashlike.linkrref"></a>
## `linkrref()`

```python
def linkrref(rref: RRef, destdir: Optional[Path] = None, format: str = '_rref_%(T)s_%(N)s', S=None) -> Path
```

linkkrref creates a symbolic link to a particular realization reference.
The new link appears in the `destdir` directory if this argument is not None,
otherwise the current directory is used.

Format accepts the following Python pattern tags:
- `%(T)s` replaced with the build time
- `%(N)s` replaced with the config name

Informally, `linkrref` creates the link:
`{tgtpath}/{format} --> $PYLIGHTNIX_STORE/{dref}/{rref}`.

The function overwrites existing symlinks.

<a name="pylightnix.bashlike.linkdref"></a>
## `linkdref()`

```python
def linkdref(dref: DRef, destdir: Optional[Path] = None, format: str = '_rref_%(N)s', S=None) -> Path
```


<a name="pylightnix.bashlike.linkrrefs"></a>
## `linkrrefs()`

```python
def linkrrefs(rrefs: Iterable[RRef], destdir: Optional[Path] = None, format: str = '_rref_%(T)s_%(N)s', S=None) -> List[Path]
```

A Wrapper around `linkrref` for linking a set of RRefs.

<a name="pylightnix.lens"></a>
# `pylightnix.lens`

Lens module defines the `Lens` helper class, which offers quick navigation
through the dependent configurations

<a name="pylightnix.lens.LensContext"></a>
## `LensContext`

```python
LensContext = NamedTuple('LensContext',[('S',Optional[StorageSettings]),
                                        ( ...
```


<a name="pylightnix.lens.val2dict"></a>
## `val2dict()`

```python
def val2dict(v: Any, ctx: LensContext) -> Optional[dict]
```

Return the `dict` representation of the Lens value, if possible. Getting
the dictionary allows for creating new lenses

<a name="pylightnix.lens.val2rref"></a>
## `val2rref()`

```python
def val2rref(v: Any, ctx: LensContext) -> RRef
```


<a name="pylightnix.lens.val2path"></a>
## `val2path()`

```python
def val2path(v: Any, ctx: LensContext) -> Path
```

Resolve the current value of Lens into system path. Assert if it is not
possible or if the result is associated with multiple paths.

FIXME: re-use val2rref here

<a name="pylightnix.lens.traverse"></a>
## `traverse()`

```python
def traverse(l: "Lens", hint: str) -> Any
```


<a name="pylightnix.lens.mutate"></a>
## `mutate()`

```python
def mutate(l: "Lens", v: Any, hint: str) -> None
```


<a name="pylightnix.lens.lens_repr"></a>
## `lens_repr()`

```python
def lens_repr(l, accessor: str) -> str
```


<a name="pylightnix.lens.Lens"></a>
## `Lens` Objects

```python
def __init__(self, ctx: LensContext, start: Any, steps: List[str]) -> None
```

A Lens is a "syntactic sugar" helper object which could traverse through
various Python and Pylightnix tree-like structures in a uniform way.

The list of supported structures include:

* Python dicts
* Pylightnix [DRefs](#pylightnix.types.DRef)
* Pylightnix [RRefs](#pylightnix.types.RRef)
* Pylightnix [Build](#pylightnix.build.Build) objects
* Pylightnix [Closures](#pylightnix.types.Closure) objects

Lens lifecycle typically consists of three stages:
1. Lens creation with [mklens](#pylightnix.lens.mklens) helper function.
2. Navigation through the nested fileds using regular Python dot-notation.
   Accessing Lens's attributes results in the creation of new Lens.
3. Access to the raw value which could no longer be converted into a Lens. In
   this case the raw value is returned. See `val`, `optval`, `rref`, `dref`,
   etc.

Lenses are not inteded to be created directly, consider using
[mklens](#pylightnix.lens.mklens) constructor.

<a name="pylightnix.lens.Lens.__init__"></a>
### `Lens.__init__()`

```python
def __init__(self, ctx: LensContext, start: Any, steps: List[str]) -> None
```

Arguments:
* `ctx` - is the context in which this Lens is created. The more information
  it contains the more functions are available
* `start` - Source object which we explore
* `steps` - List of attributes to query

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

<a name="pylightnix.lens.Lens.optval"></a>
### `Lens.optval()`

```python
@property
def optval(self) -> Optional[Any]
```

Return the value of Lens as-is

<a name="pylightnix.lens.Lens.val"></a>
### `Lens.val()`

```python
@val.setter
def val(self, v)
```


<a name="pylightnix.lens.Lens.refpath"></a>
### `Lens.refpath()`

```python
@property
def refpath(self) -> RefPath
```

Check that the current value of Lens is a `RefPath` and return it

<a name="pylightnix.lens.Lens.dref"></a>
### `Lens.dref()`

```python
@property
def dref(self) -> DRef
```

Check that the current value of Lens is a `DRef` and return it

<a name="pylightnix.lens.Lens.syspath"></a>
### `Lens.syspath()`

```python
@property
def syspath(self) -> Path
```

Check that the current value of Lens is a `Path` and return it

<a name="pylightnix.lens.Lens.contents"></a>
### `Lens.contents()`

```python
@property
def contents(self) -> str
```

Check that the current value of Lens is a `Path` and return it

<a name="pylightnix.lens.Lens.rref"></a>
### `Lens.rref()`

```python
@property
def rref(self) -> RRef
```

Check that the current value of Lens is an `RRef` and return it

<a name="pylightnix.lens.Lens.closure"></a>
### `Lens.closure()`

```python
@property
def closure(self) -> Closure
```

Constructs a closure of the DRef which this lens points to.
FIXME: Filter the closure derivations from unrelated entries.

<a name="pylightnix.lens.mklens"></a>
## `mklens()`

```python
def mklens(x: Any, o: Optional[Path] = None, b: Optional[Build] = None, rref: Optional[RRef] = None, ctx: Optional[Context] = None, closure: Optional[Closure] = None, build_output_idx: int = 0, S: Optional[StorageSettings] = None, r: Optional[Registry] = None) -> Lens
```

mklens creates [Lens](#pylightnix.lens.Lens) objects from various
Pylightnix objects.

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
- `build_output_idx:int=0` For `Builds`, specify the index of output path,
  defaulted to zero

Example:
```Python
stage=partial(fetchurl, url='http://example.com',
                        sha256='...',
                        output=[promise,'file.txt'],
                        foo={'bar':42}, # Additional configuration item
             )

dref:DRef=instantiate(stage).dref

mklens(dref).url.val  # Access raw value of 'url'
mklens(dref).foo             # Return another lens pointing at 'foo'
mklens(dref).foo.val         # Return raw value of 'foo' (a dict)
mklens(dref).foo.bar.val     # Return raw value of 'bar'
mklens(dref).foo.refpath     # Error! dict is not a path

mklens(dref).output.val      # Return raw output value
mklens(dref).output.refpath  # Return output as a RefPath (a list)
mklens(dref).output.syspath  # Error! not a realization

rref:RRef=realize1(instantiate(stage))

mklens(rref).output.syspath  # Return output as a system path
```

<a name="pylightnix.either"></a>
# `pylightnix.either`


<a name="pylightnix.either._REF"></a>
## `_REF`

```python
_REF = TypeVar('_REF')
```

_REF is either `Path` or `RRef`

<a name="pylightnix.either.ExceptionText"></a>
## `ExceptionText`

```python
ExceptionText = str
```

Alias for exception text

<a name="pylightnix.either.Either"></a>
## `Either` Objects

```python
def __init__(self, right: Optional[Output[_REF]] = None, left: Optional[Tuple[List[_REF],ExceptionText]] = None)
```

Either is a poor-man's `(EitherT Exception Ouput)` monad. It contains
either (RIGHT) result of a realization or (LEFT) error report together with
half-done results to show to the user.

`Either` should be considered as an "upgrade" for regular Output, which allows
user to record the fact of realization failure into the special kind of
realization result rather than rasing an exception.

TODO: Stress the attention on the fact that Either now encodes the list of
items which may not have the same meaning. Some items may now be 'failed'
and we may need a mapping function to apply matchers to them.

TODO: Think about whether we should mark the fact that a stage uses Either
wrappert in the stage configuration or not. Probably we should, because
either-realizers in general are not backward-compatible with regular
realizers.

<a name="pylightnix.either.Either.__init__"></a>
### `Either.__init__()`

```python
def __init__(self, right: Optional[Output[_REF]] = None, left: Optional[Tuple[List[_REF],ExceptionText]] = None)
```


<a name="pylightnix.either.mkright"></a>
## `mkright()`

```python
def mkright(o: Output[_REF]) -> Either[_REF]
```

Create a RIGHT Either

<a name="pylightnix.either.mkleft"></a>
## `mkleft()`

```python
def mkleft(paths: List[Path], exc: ExceptionText) -> Either[Path]
```

Create a LEFT Either

<a name="pylightnix.either.either_paths"></a>
## `either_paths()`

```python
def either_paths(e: Either[_REF]) -> List[_REF]
```


<a name="pylightnix.either.either_isRight"></a>
## `either_isRight()`

```python
def either_isRight(e: Either[_REF]) -> bool
```


<a name="pylightnix.either.either_isLeft"></a>
## `either_isLeft()`

```python
def either_isLeft(e: Either[_REF]) -> bool
```


<a name="pylightnix.either.either_status"></a>
## `either_status()`

```python
def either_status(e: Either[_REF]) -> Optional[ExceptionText]
```


<a name="pylightnix.either.either_loadR"></a>
## `either_loadR()`

```python
def either_loadR(rrefs: List[RRef], S) -> Either[RRef]
```


<a name="pylightnix.either.either_validate"></a>
## `either_validate()`

```python
def either_validate(dref: DRef, e: Either[Path], S=None) -> List[Path]
```


<a name="pylightnix.either.either_realizer"></a>
## `either_realizer()`

```python
def either_realizer(f: Callable[[Optional[StorageSettings],DRef,
                                Context,RealizeArg],Output[Path]]) -> Callable[[Optional[StorageSettings],DRef,
                                Context,RealizeArg],List[Path]]
```

Implements poor-man's `(EitherT Exception Ouput)` monad.
Either, stages become either LEFT (if rasied an error) or
RIGHT (after normal completion). If the stage turns LEFT, then so will be any
of it's dependant stages.

Stages which use `either_wrapper` typically don't use `claims` instead of
`promises` to allow the existance of LEFT-versions of themselves.

Either-stages should use appropriate matchers which supports LEFT-mode.

<a name="pylightnix.either.either_matcher"></a>
## `either_matcher()`

```python
def either_matcher(m: MatcherO) -> Matcher
```

Convert an Either-matcher into the regular Matcher

<a name="pylightnix.either.mkdrvE"></a>
## `mkdrvE()`

```python
def mkdrvE(config: Config, matcher: MatcherO, realizer: RealizerO, m: Optional[Registry] = None) -> DRef
```


<a name="pylightnix.either.realizeE"></a>
## `realizeE()`

```python
def realizeE(closure: Closure, force_rebuild: Union[List[DRef],bool] = [], assert_realized: List[DRef] = [], realize_args: Dict[DRef,RealizeArg] = {}) -> Either[RRef]
```


<a name="pylightnix.either.realizeManyE"></a>
## `realizeManyE()`

```python
def realizeManyE(closure: Union[Closure,Tuple[Any,Closure]], force_rebuild: Union[List[DRef],bool] = [], assert_realized: List[DRef] = [], realize_args: Dict[DRef,RealizeArg] = {}) -> Either[RRef]
```


<a name="pylightnix.arch"></a>
# `pylightnix.arch`

Functions for moving parts of the storage to and from archives.

<a name="pylightnix.arch.APACK"></a>
## `APACK`

```python
APACK = try_executable('apack',
                     'PYLIGHTNIX_APACK',
                     '`apack` execu ...
```


<a name="pylightnix.arch.AUNPACK"></a>
## `AUNPACK`

```python
AUNPACK = try_executable('aunpack',
                     'PYLIGHTNIX_AUNPACK',
                     '`aunpack` ...
```


<a name="pylightnix.arch.spack"></a>
## `spack()`

```python
def spack(roots: List[RRef], out: Path, S: Optional[StorageSettings] = None) -> None
```


<a name="pylightnix.arch.sunpack"></a>
## `sunpack()`

```python
def sunpack(archive: Path, S=None) -> None
```


<a name="pylightnix.arch.deref_"></a>
## `deref_()`

```python
def deref_(ctxr: RRef, dref: DRef, S)
```

query the context for specific dref. If not present - then it must be a
context holder itself.

<a name="pylightnix.arch.copyclosure"></a>
## `copyclosure()`

```python
def copyclosure(rrefs_S: Iterable[RRef], S: StorageSettings, D: Optional[StorageSettings] = None) -> None
```

Copy the closure of `rrefs` from source storage `S` to the destination
storage `D`. If `D` is None, use the default global storage as a desitnation.

TODO: Implement a non-recursive version.

<a name="pylightnix.deco"></a>
# `pylightnix.deco`


<a name="pylightnix.deco.Attrs"></a>
## `Attrs` Objects

A class for proxy objects where realization config parameters are set as
attributs.

<a name="pylightnix.deco.unroll"></a>
## `unroll()`

```python
def unroll(ctx: Context, dref: DRef, b: Optional[Build], rindex: int, max_depth: Optional[int] = None, always_multiref: bool = False, S=None) -> Attrs
```


<a name="pylightnix.deco.autodrv_"></a>
## `autodrv_()`

```python
def autodrv_(kwargs: dict, nouts: int = 1, matcher: Optional[Matcher] = None, always_multiref: bool = False, sourcedeps: List[Any] = [])
```


<a name="pylightnix.deco.autodrv"></a>
## `autodrv()`

```python
def autodrv(args, *,, ,, =, ,, kwargs)
```


<a name="pylightnix.deco.autostage_"></a>
## `autostage_()`

```python
def autostage_(nouts: int = 1, matcher: Optional[Matcher] = None, always_multiref: bool = False, sourcedeps: List[Any] = [], decokw)
```


<a name="pylightnix.deco.autostage"></a>
## `autostage()`

```python
def autostage(args, *,, ,, =, ,, kwargs)
```

Builds a Pylightnix [Stage](#pylightnix.types.Stage) out of Python
function. The decorator arguments form stage
[Configuration](#pylightnix.types.Config) according to the rules explained in
table below.

|Argument in decorator|Type in decorator|Argument in function|Type in function| Comment      |
|:-----------:|:-----------:|:------------:|:-------------:|:---|
| `r` | `Optional[Registry]`  | - | - | [Registry](#pylightnix.types.Registry) to register this stage in |
| `sourcedeps` | `List[Any]` | - | - | List of arbitrary Python objects to track by source |
| `matcher` | `Matcher` | - | - | [Matcher](#pylightnix.types.Matcher) to set instead of the default one. |
| `always_multiref` | `bool` | - | - | Set to `True` to represent dependencies as lists even if they include only one matched realization. |
| `name` | `str` | `name` | `str` | Argument named `name` (if any) is also used as a part of the realization name on disk |
| x | `[selfref,str,...]`  | x | `str` | A promise to produce a file or folder |
| x | `DRef` | x | `Attrs` or `List[Attrs]` or `RRef` or `List[RRef]` | [Attrs](#pylightnix.deco.Attrs) with attributs of parent realization(s) or raw [Realization references](#pylightnix.types.RRef) |
| x | t | x | t | JSON-compatible types (`bool`,`int`,`float`,`str`,lists and dicts of thereof) - are passed without changes |
| - | - | `build` | `Build` | [Build](#pylightnix.types.Build) context for current stage

