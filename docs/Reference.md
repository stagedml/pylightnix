# Table of Contents

  * [pylightnix.types](#pylightnix.types)
    * [Path](#pylightnix.types.Path)
    * [SPath](#pylightnix.types.SPath)
    * [Hash](#pylightnix.types.Hash)
    * [HashPart](#pylightnix.types.HashPart)
    * [DRef](#pylightnix.types.DRef)
    * [RRef](#pylightnix.types.RRef)
    * [Name](#pylightnix.types.Name)
    * [RefPath](#pylightnix.types.RefPath)
    * [PYLIGHTNIX\_PROMISE\_TAG](#pylightnix.types.PYLIGHTNIX_PROMISE_TAG)
    * [PYLIGHTNIX\_CLAIM\_TAG](#pylightnix.types.PYLIGHTNIX_CLAIM_TAG)
    * [PromisePath](#pylightnix.types.PromisePath)
    * [Tag](#pylightnix.types.Tag)
    * [Group](#pylightnix.types.Group)
    * [RRefGroup](#pylightnix.types.RRefGroup)
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
    * [R](#pylightnix.types.R)
    * [Stage](#pylightnix.types.Stage)
    * [Key](#pylightnix.types.Key)
  * [pylightnix.core](#pylightnix.core)
    * [logger](#pylightnix.core.logger)
    * [info](#pylightnix.core.info)
    * [warning](#pylightnix.core.warning)
    * [PYLIGHTNIX\_STORE\_VERSION](#pylightnix.core.PYLIGHTNIX_STORE_VERSION)
    * [storagename](#pylightnix.core.storagename)
    * [PYLIGHTNIX\_ROOT](#pylightnix.core.PYLIGHTNIX_ROOT)
    * [PYLIGHTNIX\_TMP](#pylightnix.core.PYLIGHTNIX_TMP)
    * [tempdir](#pylightnix.core.tempdir)
    * [PYLIGHTNIX\_STORE](#pylightnix.core.PYLIGHTNIX_STORE)
    * [storage](#pylightnix.core.storage)
    * [PYLIGHTNIX\_NAMEPAT](#pylightnix.core.PYLIGHTNIX_NAMEPAT)
    * [PYLIGHTNIX\_RESERVED](#pylightnix.core.PYLIGHTNIX_RESERVED)
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
    * [mktag](#pylightnix.core.mktag)
    * [tag\_out](#pylightnix.core.tag_out)
    * [mkgroup](#pylightnix.core.mkgroup)
    * [mkconfig](#pylightnix.core.mkconfig)
    * [config\_dict](#pylightnix.core.config_dict)
    * [config\_cattrs](#pylightnix.core.config_cattrs)
    * [config\_serialize](#pylightnix.core.config_serialize)
    * [config\_hash](#pylightnix.core.config_hash)
    * [config\_name](#pylightnix.core.config_name)
    * [config\_deps](#pylightnix.core.config_deps)
    * [config\_substitutePromises](#pylightnix.core.config_substitutePromises)
    * [config\_promises](#pylightnix.core.config_promises)
    * [mkrefpath](#pylightnix.core.mkrefpath)
    * [assert\_store\_initialized](#pylightnix.core.assert_store_initialized)
    * [store\_initialize](#pylightnix.core.store_initialize)
    * [store\_dref2path](#pylightnix.core.store_dref2path)
    * [store\_rref2path](#pylightnix.core.store_rref2path)
    * [store\_cfgpath](#pylightnix.core.store_cfgpath)
    * [store\_config\_](#pylightnix.core.store_config_)
    * [store\_config](#pylightnix.core.store_config)
    * [store\_context](#pylightnix.core.store_context)
    * [store\_cattrs](#pylightnix.core.store_cattrs)
    * [store\_deps](#pylightnix.core.store_deps)
    * [store\_depRrefs](#pylightnix.core.store_depRrefs)
    * [store\_deepdeps](#pylightnix.core.store_deepdeps)
    * [store\_deepdepRrefs](#pylightnix.core.store_deepdepRrefs)
    * [alldrefs](#pylightnix.core.alldrefs)
    * [allrrefs](#pylightnix.core.allrrefs)
    * [rootdrefs](#pylightnix.core.rootdrefs)
    * [rootrrefs](#pylightnix.core.rootrrefs)
    * [rrefdata](#pylightnix.core.rrefdata)
    * [rrefs2groups](#pylightnix.core.rrefs2groups)
    * [groups2rrefs](#pylightnix.core.groups2rrefs)
    * [drefrrefs](#pylightnix.core.drefrrefs)
    * [store\_rrefs\_](#pylightnix.core.store_rrefs_)
    * [store\_rrefs](#pylightnix.core.store_rrefs)
    * [store\_deref\_](#pylightnix.core.store_deref_)
    * [store\_deref](#pylightnix.core.store_deref)
    * [store\_buildtime](#pylightnix.core.store_buildtime)
    * [store\_tag](#pylightnix.core.store_tag)
    * [store\_group](#pylightnix.core.store_group)
    * [store\_gc](#pylightnix.core.store_gc)
    * [mkdrv\_](#pylightnix.core.mkdrv_)
    * [mkrealization](#pylightnix.core.mkrealization)
    * [mkrgroup](#pylightnix.core.mkrgroup)
    * [mkcontext](#pylightnix.core.mkcontext)
    * [context\_eq](#pylightnix.core.context_eq)
    * [context\_add](#pylightnix.core.context_add)
    * [context\_deref](#pylightnix.core.context_deref)
    * [context\_serialize](#pylightnix.core.context_serialize)
    * [promise](#pylightnix.core.promise)
    * [claim](#pylightnix.core.claim)
    * [assert\_promise\_fulfilled](#pylightnix.core.assert_promise_fulfilled)
    * [mkdrv](#pylightnix.core.mkdrv)
    * [instantiate\_](#pylightnix.core.instantiate_)
    * [instantiate](#pylightnix.core.instantiate)
    * [RealizeSeqGen](#pylightnix.core.RealizeSeqGen)
    * [realize](#pylightnix.core.realize)
    * [realizeGroups](#pylightnix.core.realizeGroups)
    * [realizeMany](#pylightnix.core.realizeMany)
    * [realizeSeq](#pylightnix.core.realizeSeq)
    * [evaluate](#pylightnix.core.evaluate)
    * [linkrref](#pylightnix.core.linkrref)
    * [linkdref](#pylightnix.core.linkdref)
    * [linkrrefs](#pylightnix.core.linkrrefs)
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
    * [assert\_rref\_deps](#pylightnix.core.assert_rref_deps)
    * [assert\_have\_realizers](#pylightnix.core.assert_have_realizers)
  * [pylightnix.build](#pylightnix.build)
    * [logger](#pylightnix.build.logger)
    * [info](#pylightnix.build.info)
    * [warning](#pylightnix.build.warning)
    * [error](#pylightnix.build.error)
    * [BuildError](#pylightnix.build.BuildError)
    * [mkbuildargs](#pylightnix.build.mkbuildargs)
    * [mkbuild](#pylightnix.build.mkbuild)
    * [B](#pylightnix.build.B)
    * [build\_wrapper\_](#pylightnix.build.build_wrapper_)
    * [build\_wrapper](#pylightnix.build.build_wrapper)
    * [build\_config](#pylightnix.build.build_config)
    * [build\_context](#pylightnix.build.build_context)
    * [build\_cattrs](#pylightnix.build.build_cattrs)
    * [build\_setoutgroups](#pylightnix.build.build_setoutgroups)
    * [build\_setoutpaths](#pylightnix.build.build_setoutpaths)
    * [build\_markstop](#pylightnix.build.build_markstop)
    * [store\_buildelta](#pylightnix.build.store_buildelta)
    * [build\_outpaths](#pylightnix.build.build_outpaths)
    * [build\_outpath](#pylightnix.build.build_outpath)
    * [build\_name](#pylightnix.build.build_name)
    * [build\_deref\_](#pylightnix.build.build_deref_)
    * [build\_deref](#pylightnix.build.build_deref)
    * [build\_paths](#pylightnix.build.build_paths)
    * [build\_path](#pylightnix.build.build_path)
    * [build\_environ](#pylightnix.build.build_environ)
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
    * [redefine](#pylightnix.stages.trivial.redefine)
    * [realized](#pylightnix.stages.trivial.realized)
  * [pylightnix.stages.fetch2](#pylightnix.stages.fetch2)
    * [logger](#pylightnix.stages.fetch2.logger)
    * [info](#pylightnix.stages.fetch2.info)
    * [error](#pylightnix.stages.fetch2.error)
    * [CURL](#pylightnix.stages.fetch2.CURL)
    * [fetchurl2](#pylightnix.stages.fetch2.fetchurl2)
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
  * [pylightnix.lens](#pylightnix.lens)
    * [LensContext](#pylightnix.lens.LensContext)
    * [val2dict](#pylightnix.lens.val2dict)
    * [val2path](#pylightnix.lens.val2path)
    * [val2rref](#pylightnix.lens.val2rref)
    * [traverse](#pylightnix.lens.traverse)
    * [mutate](#pylightnix.lens.mutate)
    * [lens\_repr](#pylightnix.lens.lens_repr)
    * [Lens](#pylightnix.lens.Lens)
    * [mklens](#pylightnix.lens.mklens)
  * [pylightnix.either](#pylightnix.either)
    * [either\_wrapper](#pylightnix.either.either_wrapper)
    * [either\_status](#pylightnix.either.either_status)
    * [either\_isRight](#pylightnix.either.either_isRight)
    * [either\_isLeft](#pylightnix.either.either_isLeft)

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
[store_rref2path](#pylightnix.core.store_rref2path).

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
[store_rref2path](#pylightnix.core.store_rref2path)
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

<a name="pylightnix.types.Tag"></a>
## `Tag`

```python
Tag = NewType('Tag', str)
```

Realization Tag is a user-defined string without spaces and newline symbols.
There is a special tag named 'out' which is used by default. Users may choose
to introduce other tags, like 'doc','man' or 'checkpoint'. User-tagged
realizations should refer to some specific 'out' realization.  For
realizations, Having the same tag would mean that those realizations share
some functionality, e.g. contain documentation or are ML model checkpoints.

Every 'out' realization plus zero-to-many other tagged realizations form a
[Group](#pylightnix.types.Group). The group behaves as a whole during
[Matching](#pylightnix.types.Matcher).

Tag invariants:
- Each RRef has its Tag, the default tag name is 'out'
- Several realization of a derivation may have the same tag. That means they
contain functionally equivalent artifacts.

<a name="pylightnix.types.Group"></a>
## `Group`

```python
Group = NewType('Group', str)
```

A type for [RRefGroup](#pylightnix.type.RRefGroup) name.

<a name="pylightnix.types.RRefGroup"></a>
## `RRefGroup`

```python
RRefGroup = Dict[Tag,RRef]
```

RRefGroup unites [tagged](#pylightnix.types.Tag) realizations. For
example, there may be a Group containing tags ['out',log'] and another Group
containing realizations tagged with ['out','log','docs']. Each group must
contain at least one realization tagged with tag 'out' Only 'out'
realizations are subjects for [matching](#pylightnix.types.Matcher).

Group invariants:
- There are no empty Groups
- Each realization belongs to exactly one Group
- All realizations of a Group originates from the same derivation
- All realizations of a Group have the same Context
- At least one realization of a group hase tag 'out'
- All realizations of a Group have different tags

<a name="pylightnix.types.Context"></a>
## `Context`

```python
Context = Dict[DRef,List[RRef]]
```

Context type is an alias for Python dict which maps
[DRefs](#pylightnix.types.DRef) into one or many
[RRefs](#pylightnix.types.RRef).

For any derivation, the Context stores a mapping from it's dependency's
derivations to realizations.

<a name="pylightnix.types.Matcher"></a>
## `Matcher`

```python
Matcher = Callable[[SPath,DRef,Context],Optional[List[RRefGroup]]]
```

Matcher is a type of user-defined functions which select required
realizations from the set of all realizations tagged with tag 'out'.

A Matcher should take a derivation reference and a context as its arguments.
Its task is to read find out which realizations are available and return
some subset of this set (see [store_rrefs](#pylightnix.core.store_rrefs)).
Alternatively, matcher could return None which would be a signal for
Pylightnix to produce more realizations.

Matchers may return an empty set. In contrast to `None`, this would instruct
Pylightnix to leave the derivation without realizations.

Pylightnix calls matchers during the realizaiton. Matching results are
cached in form of `(DRef,List[RRef])` tuple. Pylightnix use it to e.g.
resolve downstream realizations.

Matchers must follow the below rules:

- Matchers should be **pure**. It's output should depend only on the
existing build artifacts of available realizations.
- Matchers should be **satisfiable** by realizers of their stages. If matcher
returns None, the core calls realizer and re-run the matcher only once.

Pylightnix includes a set of built-in matchers:

- [match](#pylightnix.core.match) is a generic matcher with rich sorting and
filtering API.
- [match_n](#pylightnix.core.match_n) is it's version for fixed number of matches
- [match_best](#pylightnix.core.match_best) decision is made based on a named
build artifact
- [match_all](#pylightnix.core.match_all) matches any number of
realizations, including zero.
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
Realizer = Callable[[SPath,DRef,Context,RealizeArg],List[Dict[Tag,Path]]]
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
Derivation = NamedTuple('Derivation', [('dref',DRef),
                                       ('matcher',Matcher), ...
```

Derivation is the core type of Pylightnix. It keeps all the information about
a stage:

* It's [configuration](#pylightnix.types.Config)
* It's [realize](#pylightnix.core.realize) method
* And how to find best [match](#pylightnix.types.Matcher) among possible
multiple realizations.

Information is stored partly on disk (in the Pylightnix storage), partly in
memory in form of Python code.

Derivations normally appear as a result of [mkdrv](#pylightnix.core.mkdrv)
call.

<a name="pylightnix.types.Closure"></a>
## `Closure`

```python
Closure = NamedTuple('Closure', [('dref',DRef),
                                 ('derivations',List[Derivatio ...
```

Closure is a named tuple, containing a reference to target
[DRef](#pylightnix.types.DRef) and a collection of required derivations.
`derivations` of a valid Closure contains complete (but not nesessary
minimal) collection of dependencies of it's target derivation `dref`.

Closure is typically obtained as a result of the
[instantiate](#pylightnix.core.instantiate) and is typically consumed by the
call to [realizeMany](#pylightnix.core.realizeMany) or it's analogs.

<a name="pylightnix.types.Config"></a>
## `Config` Objects

```python
def __init__(self, d: dict)
```

Config is a JSON-serializable dict which contains user-defined attributes
of Pylightnix stage. Together with Realizers and Matchers, Configs determine
stage's realization process.

Configs should match the requirements of `assert_valid_config`. Typically,
it's `val` dictionary should only contain JSON-serializable types: strings,
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

`RConfig` is a [Config](#pylightnix.types.Config) where all
[Claims](#pylightnix.types.PYLIGHTNIX_CLAIM_TAG) and
[Promises](#pylightnix.types.PYLIGHTNIX_PROMISE_TAG) are resolved.  RConfig
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
BuildArgs = NamedTuple('BuildArgs', [('storage',SPath),
                                     ('dref',DRef),
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
- [build_setoutgroups](#pylightnix.build.build_setoutgroups) - Initialize and
  return groups of output folders
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
def __init__(self, S: SPath)
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
def __init__(self, S: SPath)
```


<a name="pylightnix.types.R"></a>
## `R`

```python
R = TypeVar('R',bound=SupportsAbs[DRef])
```


<a name="pylightnix.types.Stage"></a>
## `Stage`

```python
Stage = Callable[[Manager],R]
```

From the user's point of view, Stage is a basic building block of
Pylightnix.  It is a function that 'introduces'
[derivations](#pylightnix.typing.Derivation) to
[Manager](#pylightnix.typing.Manager).  Return value is a [derivation
reference](#pylightnix.types.DRef) which is a proof that the derivation was
introduced sucessfully.

Some built-in stages are:
- [mknode](#pylightnix.stages.trivial.mknode)
- [mkfile](#pylightnix.stages.trivial.mkfile)
- [fetchurl](#pylightnix.stages.fetchurl.fetchurl)

Note: Real stages often accept additional custom arguments which AFAIK
couldn't be handled by the standard Python typesystem. In extended MyPy the
definition would be:
```
Stage = Callable[[Manager,VarArg(Any),KwArg(Any)],DRef]
```
We use `type:ignore` pragmas when we need to pass `**kwargs`.

<a name="pylightnix.types.Key"></a>
## `Key`

```python
Key = Callable[[RRef],Optional[Union[int,float,str]]]
```


<a name="pylightnix.core"></a>
# `pylightnix.core`

Core Pylightnix definitions

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


<a name="pylightnix.core.PYLIGHTNIX_STORE_VERSION"></a>
## `PYLIGHTNIX_STORE_VERSION`

```python
PYLIGHTNIX_STORE_VERSION = 0
```

*Do not change!*
Tracks the version of pylightnix storage

<a name="pylightnix.core.storagename"></a>
## `storagename()`

```python
def storagename()
```


<a name="pylightnix.core.PYLIGHTNIX_ROOT"></a>
## `PYLIGHTNIX_ROOT`

```python
PYLIGHTNIX_ROOT = environ.get('PYLIGHTNIX_ROOT',
  join(environ.get('HOME','/var/run'), '_pylightnix'))
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

<a name="pylightnix.core.tempdir"></a>
## `tempdir()`

```python
def tempdir(tmp: Optional[Path] = None) -> Path
```


<a name="pylightnix.core.PYLIGHTNIX_STORE"></a>
## `PYLIGHTNIX_STORE`

```python
PYLIGHTNIX_STORE = join(PYLIGHTNIX_ROOT, storagename())
```


<a name="pylightnix.core.storage"></a>
## `storage()`

```python
def storage(S: Optional[SPath] = None) -> SPath
```

Returns the location to Pylightnix storage, defaulting to
PYLIGHTNIX_STORE

<a name="pylightnix.core.PYLIGHTNIX_NAMEPAT"></a>
## `PYLIGHTNIX_NAMEPAT`

```python
PYLIGHTNIX_NAMEPAT = "[a-zA-Z0-9_-]"
```


<a name="pylightnix.core.PYLIGHTNIX_RESERVED"></a>
## `PYLIGHTNIX_RESERVED`

```python
PYLIGHTNIX_RESERVED = ['context.json','group.json']
```

Reserved file names are treated specially be the core. Users should
not normally create or alter files with this names.

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

<a name="pylightnix.core.mktag"></a>
## `mktag()`

```python
def mktag(s: str) -> Tag
```


<a name="pylightnix.core.tag_out"></a>
## `tag_out()`

```python
def tag_out() -> Tag
```

Pre-defined default Tag name

<a name="pylightnix.core.mkgroup"></a>
## `mkgroup()`

```python
def mkgroup(s: str) -> Group
```


<a name="pylightnix.core.mkconfig"></a>
## `mkconfig()`

```python
def mkconfig(d: dict) -> Config
```

Create Config object out of config dictionary. Asserts if the dictionary
is not JSON-compatible. As a handy hack, filter out `m:Manager` variable
which likely is an utility [Manager](#pylightnix.types.Manager) object.

FIXME: Should we assert on invalid Config here?

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


<a name="pylightnix.core.mkrefpath"></a>
## `mkrefpath()`

```python
def mkrefpath(r: DRef, items: List[str] = []) -> RefPath
```

Construct a [RefPath](#pylightnix.types.RefPath) out of a reference `ref`
and a path within the stage's realization

<a name="pylightnix.core.assert_store_initialized"></a>
## `assert_store_initialized()`

```python
def assert_store_initialized(S: SPath) -> None
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
- `custom_store:Optional[str]=None`: If not None, create new storage located
  here.
- `custom_tmp:Optional[str]=None`: If not None, set the temp files directory
  here.
- `check_not_exist:bool=False`: Set to True to assert on already existing
  storages. Good to become sure that newly created storage is empty.

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
def store_dref2path(r: DRef, S=None) -> Path
```


<a name="pylightnix.core.store_rref2path"></a>
## `store_rref2path()`

```python
def store_rref2path(r: RRef, S=None) -> Path
```


<a name="pylightnix.core.store_cfgpath"></a>
## `store_cfgpath()`

```python
def store_cfgpath(r: DRef, S=None) -> Path
```


<a name="pylightnix.core.store_config_"></a>
## `store_config_()`

```python
def store_config_(r: DRef, S=None) -> Config
```


<a name="pylightnix.core.store_config"></a>
## `store_config()`

```python
def store_config(r: Union[DRef,RRef], S=None) -> RConfig
```

Read the [Config](#pylightnix.types.Config) of the derivation and
[resolve](#pylightnix.core.config_substitutePromises) it from promises and
claims.

<a name="pylightnix.core.store_context"></a>
## `store_context()`

```python
def store_context(r: RRef, S=None) -> Context
```

FIXME: Either do `context_add(ctx, rref2dref(r), [r])` or document it's absense

<a name="pylightnix.core.store_cattrs"></a>
## `store_cattrs()`

```python
def store_cattrs(r: Union[DRef,RRef], S=None) -> Any
```

Read the [ConfigAttrs](#pylightnix.types.ConfigAttr) of the storage node `r`.
Note, that it is a kind of 'syntactic sugar' for `store_config`. Both
functions do the same thing.

<a name="pylightnix.core.store_deps"></a>
## `store_deps()`

```python
def store_deps(drefs: Iterable[DRef], S=None) -> Set[DRef]
```

Return a list of reference's immediate dependencies, not including `drefs`
themselves.

<a name="pylightnix.core.store_depRrefs"></a>
## `store_depRrefs()`

```python
def store_depRrefs(rrefs: Iterable[RRef], S=None) -> Set[RRef]
```


<a name="pylightnix.core.store_deepdeps"></a>
## `store_deepdeps()`

```python
def store_deepdeps(drefs: Iterable[DRef], S=None) -> Set[DRef]
```

Return the complete set of `drefs`'s dependencies, not including `drefs`
themselves.

<a name="pylightnix.core.store_deepdepRrefs"></a>
## `store_deepdepRrefs()`

```python
def store_deepdepRrefs(rrefs: Iterable[RRef], S=None) -> Set[RRef]
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
def rootdrefs(S: Optional[SPath] = None) -> Set[DRef]
```

Return root DRefs of the storage `S` as a set

<a name="pylightnix.core.rootrrefs"></a>
## `rootrrefs()`

```python
def rootrrefs(S: Optional[SPath] = None) -> Set[RRef]
```

Return root RRefs of the storage `S` as a set

<a name="pylightnix.core.rrefdata"></a>
## `rrefdata()`

```python
def rrefdata(rref: RRef, S=None) -> Iterable[Tuple[str,List[str],List[str]]]
```


<a name="pylightnix.core.rrefs2groups"></a>
## `rrefs2groups()`

```python
def rrefs2groups(rrefs: Iterable[RRef], S=None) -> List[RRefGroup]
```

Split RRefs to a set of [Groups](#pylightnix.types.Group), according to
their [Tags](#pylightnix.types.Tag)

FIXME: re-implement with a complexity better than O(N^2)

<a name="pylightnix.core.groups2rrefs"></a>
## `groups2rrefs()`

```python
def groups2rrefs(grs: List[RRefGroup]) -> List[RRef]
```

Merges several [Groups](#pylightnix.types.Group) of RRefs into a plain
list of RRefs

<a name="pylightnix.core.drefrrefs"></a>
## `drefrrefs()`

```python
def drefrrefs(dref: DRef, S=None) -> List[RRef]
```

Iterate over all realizations of a derivation `dref`. The sort order is
unspecified. Matching is not taken into account.

<a name="pylightnix.core.store_rrefs_"></a>
## `store_rrefs_()`

```python
def store_rrefs_(dref: DRef, S=None) -> List[RRefGroup]
```

Iterate over all realizations of a derivation `dref`. The sort order is
unspecified.

<a name="pylightnix.core.store_rrefs"></a>
## `store_rrefs()`

```python
def store_rrefs(dref: DRef, context: Context, S=None) -> List[RRefGroup]
```

Iterate over realizations of a derivation `dref` which match a specified
[context](#pylightnix.types.Context). Sorting order is unspecified.

<a name="pylightnix.core.store_deref_"></a>
## `store_deref_()`

```python
def store_deref_(context_holder: RRef, dref: DRef, S=None) -> List[RRefGroup]
```


<a name="pylightnix.core.store_deref"></a>
## `store_deref()`

```python
def store_deref(context_holder: RRef, dref: DRef, S=None) -> RRefGroup
```

For any realization `context_holder` and it's dependency `dref`, `store_deref`
queries the realization reference of this dependency.

See also [build_deref](#pylightnix.core.build_deref)

<a name="pylightnix.core.store_buildtime"></a>
## `store_buildtime()`

```python
def store_buildtime(rref: RRef, S=None) -> Optional[str]
```

Return the buildtime of the current RRef in a format specified by the
[PYLIGHTNIX_TIME](#pylightnix.utils.PYLIGHTNIX_TIME) constant.

[parsetime](#pylightnix.utils.parsetime) may be used to parse stings into
UNIX-Epoch seconds.

Buildtime is the time when the realization process has started. Some
realizations may not provide this information.

<a name="pylightnix.core.store_tag"></a>
## `store_tag()`

```python
def store_tag(rref: RRef, S=None) -> Tag
```

Return the [Tag](#pylightnix.types.tag) of a Realization. Default Tag
name is 'out'.

<a name="pylightnix.core.store_group"></a>
## `store_group()`

```python
def store_group(rref: RRef, S=None) -> Group
```

Return group identifier of the realization

<a name="pylightnix.core.store_gc"></a>
## `store_gc()`

```python
def store_gc(keep_drefs: List[DRef], keep_rrefs: List[RRef], S: SPath) -> Tuple[Set[DRef],Set[RRef]]
```

Take roots which are in use and should not be removed. Return roots which
are not used and may be removed. Actual removing is to be done by the user.

Default location of `S` may be changed.

See also [rmref](#pylightnix.bashlike.rmref)

<a name="pylightnix.core.mkdrv_"></a>
## `mkdrv_()`

```python
def mkdrv_(c: Config, S: SPath) -> DRef
```

Create new derivation in storage `S`.

We attempt to do it atomically by creating temp directory first and then
renaming it right into it's place in the storage.

FIXME: Assert or handle possible (but improbable) hash collision [*]

<a name="pylightnix.core.mkrealization"></a>
## `mkrealization()`

```python
def mkrealization(dref: DRef, l: Context, o: Path, leader: Optional[Tuple[Tag,RRef]] = None, S=None) -> RRef
```

Create the [Realization](#pylightnix.types.RRef) object in the storage
`S`. Return new Realization reference.

Parameters:
- `dref:DRef`: Derivation reference to create the realization of.
- `l:Context`: Context which stores dependency information.
- `o:Path`: Path to temporal (build) folder which contains artifacts,
  prepared by the [Realizer](#pylightnix.types.Realizer).
- `leader`: Tag name and Group identifier of the Group leader. By default,
  we use name `out` and derivation's own rref.

FIXME: Assert or handle possible but improbable hash collision[*]
FIXME: Consider(not sure) writing group.json for all realizations[**]

<a name="pylightnix.core.mkrgroup"></a>
## `mkrgroup()`

```python
def mkrgroup(dref: DRef, ctx: Context, og: Dict[Tag,Path], S=None) -> RRefGroup
```

Create [realization group](#pylightnix.types.Group) in storage `S` by
iteratively calling [mkrealization](#pylightnix.core.mkrealization).

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


<a name="pylightnix.core.context_deref"></a>
## `context_deref()`

```python
def context_deref(context: Context, dref: DRef, S=None) -> List[RRefGroup]
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
- `m:Manager`: A Manager to update with a new derivation
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

<a name="pylightnix.core.instantiate_"></a>
## `instantiate_()`

```python
def instantiate_(m: Manager, stage: Any, args, *,, ,, kwargs) -> Closure
```


<a name="pylightnix.core.instantiate"></a>
## `instantiate()`

```python
def instantiate(stage: Any, args, *,, ,, =, ,, kwargs) -> Closure
```

Instantiate takes the [Stage](#pylightnix.types.Stage) function and
calculates the [Closure](#pylightnix.types.Closure) of it's
[Derivations](#pylightnix.types.Derivation).
All new derivations are added to the storage.
See also [realizeMany](#pylightnix.core.realizeMany)

<a name="pylightnix.core.RealizeSeqGen"></a>
## `RealizeSeqGen`

```python
RealizeSeqGen = Generator[Tuple[SPath,DRef,Context,Derivation,RealizeArg],
                          Tuple[Optional[ ...
```


<a name="pylightnix.core.realize"></a>
## `realize()`

```python
def realize(closure: Closure, force_rebuild: Union[List[DRef],bool] = [], assert_realized: List[DRef] = []) -> RRef
```

A simplified version of [realizeMany](#pylightnix.core.realizeMany).
Expects only one output path.

<a name="pylightnix.core.realizeGroups"></a>
## `realizeGroups()`

```python
def realizeGroups(closure: Closure, force_rebuild: Union[List[DRef],bool] = [], assert_realized: List[DRef] = [], realize_args: Dict[DRef,RealizeArg] = {}) -> List[RRefGroup]
```

Obtain one or more [Closure](#pylightnix.types.Closure) realizations of a
stage.

Returned value is a collection of tagged
[realizations](#pylightnix.types.RRef) references.

The function returns [matching](#pylightnix.types.Matcher) realizations
immediately if they are exist.

Otherwize, a number of [Realizers](#pylightnix.types.Realizer) are called.

Example:
```python
def mystage(m:Manager)->DRef:
  ...
  return mkdrv(m, ...)

clo:Closure=instantiate(mystage)
rrefgs:List[RRefGroup]=realizeGroups(clo)
print([mklen(rref).syspath for grp[tag_out()] in rrefgs])
```

Pylightnix contains the following alternatives to `realizeGroup`:

* [realize](#pylightnix.core.realize) - A single-output version
* [repl_realize](#pylightnix.repl.repl_realize) - A REPL-friendly version
* [realize_inplace](#pylightnix.inplace.realize_inplace) - A simplified
  version which uses a global derivation Manager.

- FIXME: Stage's context is calculated inefficiently. Maybe one should track
  dep.tree to avoid calling `store_deepdeps` within the cycle.
- FIXME: Update derivation's matcher after forced rebuilds. Matchers should
  remember and reproduce user's preferences.

<a name="pylightnix.core.realizeMany"></a>
## `realizeMany()`

```python
def realizeMany(closure: Closure, force_rebuild: Union[List[DRef],bool] = [], assert_realized: List[DRef] = [], realize_args: Dict[DRef,RealizeArg] = {}) -> List[RRef]
```


<a name="pylightnix.core.realizeSeq"></a>
## `realizeSeq()`

```python
def realizeSeq(closure: Closure, force_interrupt: List[DRef] = [], assert_realized: List[DRef] = [], realize_args: Dict[DRef,RealizeArg] = {}) -> RealizeSeqGen
```

Sequentially realize the closure by issuing steps via Python's generator
interface. `realizeSeq` encodes low-level details of the realization
algorithm. Consider calling [realizeMany](#pylightnix.core.realizeMany) or
it's analogs instead.

FIXME: `assert_realized` may probably be implemented by calling `redefine`
with appropriate failing realizer on every Derivation.

<a name="pylightnix.core.evaluate"></a>
## `evaluate()`

```python
def evaluate(stage, args, *,, ,, kwargs) -> RRef
```


<a name="pylightnix.core.linkrref"></a>
## `linkrref()`

```python
def linkrref(rref: RRef, destdir: Optional[Path] = None, name: Optional[str] = None, withtime: bool = False, S=None) -> Path
```

Helper function that creates a symbolic link to a particular realization
reference. The link is created under the current directory by default or under
the `destdir` directory.

Create a symlink pointing to realization `rref`. Other arguments define
symlink name and location. Informally,
`{tgtpath}/{timeprefix}{name} --> $PYLIGHTNIX_STORE/{dref}/{rref}`.
Overwrite existing symlinks. Folder named `tgtpath` should exist.

<a name="pylightnix.core.linkdref"></a>
## `linkdref()`

```python
def linkdref(dref: DRef, destdir: Optional[Path] = None, name: Optional[str] = None, S=None) -> Path
```


<a name="pylightnix.core.linkrrefs"></a>
## `linkrrefs()`

```python
def linkrrefs(rrefs: Iterable[RRef], destdir: Optional[Path] = None, withtime: bool = False, S=None) -> List[Path]
```

A Wrapper around `linkrref` for linking a set of RRefs.

<a name="pylightnix.core.mksymlink"></a>
## `mksymlink()`

```python
def mksymlink(rref: RRef, tgtpath: Path, name: str, withtime: bool = True, S=None) -> Path
```

A wrapper for `linkrref`, for backward compatibility

<a name="pylightnix.core.match"></a>
## `match()`

```python
def match(keys: List[Key], rmin: Optional[int] = 1, rmax: Optional[int] = 1, exclusive: bool = False) -> Matcher
```

Create a [Matcher](#pylightnix.types.Matcher) by combining different
sorting keys and selecting a top-n threshold.

Only realizations which have [tag](#pylightnix.types.Tag) 'out' (which is a
default tag name) participate in matching. After the matching, Pylightnix
adds all non-'out' realizations which share [group](#pylightnix.types.Group)
with at least one matched realization.

Arguments:
- `keys`: A list of [Key](#pylightnix.types.Key) functions.
- `rmin`: An integer selecting the minimum number of realizations to accept.
    If non-None, Pylightnix will be asked to run the Realizer **if** the number
    of matching keys is less than this number.
- `rmax`: An integer selecting the maximum number of realizations to match
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


<a name="pylightnix.core.assert_rref_deps"></a>
## `assert_rref_deps()`

```python
def assert_rref_deps(c: Config) -> None
```


<a name="pylightnix.core.assert_have_realizers"></a>
## `assert_have_realizers()`

```python
def assert_have_realizers(m: Manager, drefs: List[DRef]) -> None
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
def __init__(self, S: SPath, dref: DRef, outgroups: List[Dict[Tag,Path]], exception: Exception, msg: str = '')
```

Exception class for build errors

<a name="pylightnix.build.BuildError.__init__"></a>
### `BuildError.__init__()`

```python
def __init__(self, S: SPath, dref: DRef, outgroups: List[Dict[Tag,Path]], exception: Exception, msg: str = '')
```

Initialize BUildError instance.

<a name="pylightnix.build.BuildError.__str__"></a>
### `BuildError.__str__()`

```python
def __str__(self)
```


<a name="pylightnix.build.mkbuildargs"></a>
## `mkbuildargs()`

```python
def mkbuildargs(S: SPath, dref: DRef, context: Context, starttime: Optional[str], iarg: InstantiateArg, rarg: RealizeArg) -> BuildArgs
```


<a name="pylightnix.build.mkbuild"></a>
## `mkbuild()`

```python
def mkbuild(S: SPath, dref: DRef, context: Context, buildtime: bool = True) -> Build
```


<a name="pylightnix.build.B"></a>
## `B`

```python
B = TypeVar('B')
```


<a name="pylightnix.build.build_wrapper_"></a>
## `build_wrapper_()`

```python
def build_wrapper_(f: Callable[[B],None], ctr: Callable[[BuildArgs],B], starttime: Optional[str] = None, stoptime: Optional[str] = None) -> Realizer
```

Build Adapter which convers user-defined realizers which use
[Build](#pylightnix.types.Build) API into a low-level
[Realizer](#pylightnix.types.Realizer)

FIXME: Specify the fact that `B` should be derived from `Build`.
       Maybe just replace `B` with `Build` and require deriving from it?

<a name="pylightnix.build.build_wrapper"></a>
## `build_wrapper()`

```python
def build_wrapper(f: Callable[[Build],None], starttime: Optional[str] = None, stoptime: Optional[str] = None) -> Realizer
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

<a name="pylightnix.build.build_setoutgroups"></a>
## `build_setoutgroups()`

```python
def build_setoutgroups(b: Build, tagset: List[List[Tag]] = [[tag_out()]]) -> List[Dict[Tag,Path]]
```


<a name="pylightnix.build.build_setoutpaths"></a>
## `build_setoutpaths()`

```python
def build_setoutpaths(b: Build, nouts: int) -> List[Path]
```


<a name="pylightnix.build.build_markstop"></a>
## `build_markstop()`

```python
def build_markstop(b: Build, buildstop: Optional[str]) -> None
```


<a name="pylightnix.build.store_buildelta"></a>
## `store_buildelta()`

```python
def store_buildelta(rref: RRef, S=None) -> Optional[float]
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
def build_deref_(b: Build, dref: DRef) -> List[RRefGroup]
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
def build_deref(b: Build, dref: DRef) -> RRefGroup
```


<a name="pylightnix.build.build_paths"></a>
## `build_paths()`

```python
def build_paths(b: Build, refpath: RefPath, tag: Tag = Tag('out')) -> List[Path]
```

Convert given [RefPath](#pylightnix.types.RefPath) (which may be either a
regular RefPath or an ex-[PromisePath](#pylightnix.types.PromisePath)) into
one or many filesystem paths. Conversion refers to the
[Context](#pylightnix.types.Context) of the current realization process by
accessing it's [build_context](#pylightnix.build.build_context).

Typically, we configure stages to match only one realization at once, so the
returned list often has only one entry. For this case there is a simplified
[build_path](#pylightnix.build.build_path) version of this function.

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
def build_path(b: Build, refpath: RefPath, tag: Tag = Tag('out')) -> Path
```

A single-realization version of the [build_paths](#pylightnix.build.build_paths).

<a name="pylightnix.build.build_environ"></a>
## `build_environ()`

```python
def build_environ(b: Build, env: Optional[Any] = None) -> dict
```

Prepare environment by adding Build's config to the environment as
variables. The function resolves all singular RefPaths into system paths
using current Build's context.

FIXME: Use bash-array syntax for multi-ouput paths

<a name="pylightnix.inplace"></a>
# `pylightnix.inplace`

This module defines inplace variants of `instantiate` and `realize`
functions. Inplace functions store closures in their own global dependency
resolution [Manager](#pylightnix.types.Manager) and thus offer a simpler API,
but add usual risks of using gloabl variables.

<a name="pylightnix.inplace.PYLIGHTNIX_MANAGER"></a>
## `PYLIGHTNIX_MANAGER`

```python
PYLIGHTNIX_MANAGER = Manager(storage(None))
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
def repl_continueMany(out_groups: Optional[List[Dict[Tag,Path]]] = None, out_rrefgs: Optional[List[RRefGroup]] = None, rh: Optional[ReplHelper] = None) -> Optional[List[RRef]]
```


<a name="pylightnix.repl.repl_continue"></a>
## `repl_continue()`

```python
def repl_continue(out_groups: Optional[List[Dict[Tag,Path]]] = None, out_rrefs: Optional[List[RRefGroup]] = None, rh: Optional[ReplHelper] = None) -> Optional[RRef]
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

Return `Build` object for using in repl-based debugging

Example:
```
from stages import some_stage, some_stage_build, some_stage_train

rh=repl_realize(instantiate(some_stage))
b=repl_build(rh)
some_stage_build(b) # Debug as needed
some_stage_train(b) # Debug as needed
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
def mknode(m: Manager, config_dict: dict, artifacts: Dict[Name,bytes] = {}, name: str = 'mknode') -> DRef
```


<a name="pylightnix.stages.trivial.mkfile"></a>
## `mkfile()`

```python
def mkfile(m: Manager, name: Name, contents: bytes, filename: Optional[Name] = None) -> DRef
```


<a name="pylightnix.stages.trivial.redefine"></a>
## `redefine()`

```python
def redefine(stage: Any, new_config: Callable[[dict],None] = lambda x:None, new_matcher: Optional[Matcher] = None, new_realizer: Optional[Realizer] = None, check_promises: bool = True) -> Any
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


<a name="pylightnix.stages.fetch2.fetchurl2"></a>
## `fetchurl2()`

```python
def fetchurl2(m: Manager, url: str, sha256: Optional[str] = None, sha1: Optional[str] = None, name: Optional[str] = None, filename: Optional[str] = None, force_download: bool = False, kwargs) -> DRef
```

Download file given it's URL addess.

Downloading is done by calling `wget` application. Optional unpacking is
performed with the `aunpack` script from `atool` package. `sha256` defines the
expected SHA-256 hashsum of the stored data. `mode` allows to tweak the
stage's behavior: adding word 'unpack' instructs fetchurl to unpack the
package, adding 'remove' instructs it to remove the archive after unpacking.

If 'unpack' is not expected, then the promise named 'out_path' is created.

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
  return fetchurl2(
    m,
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b')

rref:RRef=realize(instantiate(hello_src))
print(store_rref2path(rref))
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
def fetchurl(m: Manager, url: str, sha256: Optional[str] = None, sha1: Optional[str] = None, mode: str = 'unpack,remove', name: Optional[str] = None, filename: Optional[str] = None, force_download: bool = False, check_promises: bool = True, kwargs) -> DRef
```

Download and unpack an URL addess.

Downloading is done by calling `wget` application. Optional unpacking is
performed with the `aunpack` script from `atool` package. `sha256` defines the
expected SHA-256 hashsum of the stored data. `mode` allows to tweak the
stage's behavior: adding word 'unpack' instructs fetchurl to unpack the
package, adding 'remove' instructs it to remove the archive after unpacking.

If 'unpack' is not expected, then the promise named 'out_path' is created.

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
print(store_rref2path(rref))
```

<a name="pylightnix.stages.fetch.fetchlocal"></a>
## `fetchlocal()`

```python
def fetchlocal(m: Manager, sha256: str, path: Optional[str] = None, envname: Optional[str] = None, mode: str = 'unpack,remove', name: Optional[str] = None, filename: Optional[str] = None, check_promises: bool = True, kwargs) -> DRef
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

Return the contents of r's artifact line by line. `fn` is a list of
folders, relative to rref's root.

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

<a name="pylightnix.lens.LensContext"></a>
## `LensContext`

```python
LensContext = NamedTuple('LensContext', [('storage',SPath),
                                         ('build_path' ...
```


<a name="pylightnix.lens.val2dict"></a>
## `val2dict()`

```python
def val2dict(v: Any, ctx: LensContext) -> Optional[dict]
```

Return the `dict` representation of the Lens value, if possible. Getting
the dictionary allows for creating new lenses

<a name="pylightnix.lens.val2path"></a>
## `val2path()`

```python
def val2path(v: Any, ctx: LensContext) -> Path
```

Resolve the current value of Lens into system path. Assert if it is not
possible or if the result is associated with multiple paths.

<a name="pylightnix.lens.val2rref"></a>
## `val2rref()`

```python
def val2rref(v: Any, ctx: LensContext) -> RRef
```


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

Lens is a helper `sugar` object which could traverse through various
Python and Pylightnix tree-like structures in a uniform way.

The list of supported structures include:

* Python dicts
* Pylightnix DRefs, which are converted to Python dicts of their
  configuration parameters
* Pylightnix RRefs (which are DRefs plus realizations)
* Pylightnix Build objects (which are DRefs plus temporary build folder)
* Pylightnix Closures (which are DRefs with accompanying library of
  Derivations)

Lens lifecycle typically consists of three stages:
1. Lens creation with [mklens](#pylightnix.lens.mklens) helper function.
2. Navigation through the nested fileds using regular Python dot-notation.
   Accessing Lens's attributes results in the creation of new Lens.
3. Access to the raw value which could no longer be converted into a Lens. In
   this case the raw value is returned. See `val`, `optval`, `rref`, `dref`,
   etc.

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

Check that the current value of Lens is an `RRef` and return it

<a name="pylightnix.lens.mklens"></a>
## `mklens()`

```python
def mklens(x: Any, o: Optional[Path] = None, b: Optional[Build] = None, rref: Optional[RRef] = None, ctx: Optional[Context] = None, closure: Optional[Closure] = None, build_output_idx: int = 0, S: Optional[SPath] = None) -> Lens
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

Examples:
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

rref:RRef=realize(instantiate(stage))

mklens(rref).output.syspath  # Return output as a system path
```

<a name="pylightnix.either"></a>
# `pylightnix.either`


<a name="pylightnix.either.either_wrapper"></a>
## `either_wrapper()`

```python
def either_wrapper(f: Realizer) -> Realizer
```

This wrapper implements poor-man's `(EitherT Error)` monad on stages.
With this wrapper, stages could become either LEFT (if rasied an error) or
RIGHT (after normal completion). If the stage turns LEFT, then so will be any
of it's dependant stages.

Stages which use `either_wrapper` typically don't use `claims` instead of
`promises` to allow the existance of LEFT-versions of themselves.

Either-stages should use appropriate matchers which supports LEFT-mode.

<a name="pylightnix.either.either_status"></a>
## `either_status()`

```python
def either_status(rref: RRef, S=None) -> str
```


<a name="pylightnix.either.either_isRight"></a>
## `either_isRight()`

```python
def either_isRight(rref: RRef, S=None) -> bool
```


<a name="pylightnix.either.either_isLeft"></a>
## `either_isLeft()`

```python
def either_isLeft(rref: RRef, S=None) -> bool
```


