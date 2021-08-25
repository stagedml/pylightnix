-   [GNU Hello demo](#gnu-hello-demo)
    -   [Task](#task)
    -   [Implementation](#implementation)
        -   [Fetchurl and Unpack stages](#fetchurl-and-unpack-stages)
        -   [A custom compile stage](#a-custom-compile-stage)
        -   [Accessing the results](#accessing-the-results)

GNU Hello demo
==============

[Complete source of the demo](./HELLO.py)

Pylightnix is a library for manipulating immutable data objects. It
provides core API for checking, creating and querying such objects using
files and folders as a data sotrage. One kind of applications which
could benefit from this API is package managers.

Task
----

Here we illustrate basic concepts by designing a toy build script for
compiling and running [GNU hello](https://www.gnu.org/software/hello)
program. Note, that this script will miss an important feature of
package managers, namely build isolation, which is out of the
Pylightnix’ scope.

GNU Hello is a demo application which prints ‘Hello world!’ on its
standard output. It’s purpose is to demonstrate the usage of Automake
tools. We will see how Pylighnix could help us to solve this quest. We
assume that the host system provides an access to the GNU Automake
toolchain, that is, Autoconf, Automake, gcc, etc.

We go through the following plan of actions:

1.  Define a rule for downloading GNU Hello sources, using builtin
    `fetchurl` stage.
2.  Define a custom rule for compiling GNU Hello from sources.
3.  Interact with the storage.

Implementation
--------------

Pylightnix offers functions which form a kind of domain-specific
language, embedded in Python language. Our program is a Python script,
which could be executed by a common `python3` interpreter. In this demo
we will need certain standard Python functions. Later we will import
Pylightnix functions as needed.

``` python
from os.path import join
from os import system, chdir, getcwd
from shutil import copytree
from tempfile import TemporaryDirectory
from typing import Any
from subprocess import Popen, PIPE
```

First things first, Pylightnix uses filesystem storage for tracking
immutable data object (or stages) which could depend on each other. This
storage is global, it is the central part of library. In order to check
or create it, we call `initialize`:

``` python
from os import environ
from pylightnix import fsinit

environ['PYLIGHTNIX_ROOT']='/tmp/pylightnix_hello_demo'
fsinit(remove_existing=True)
```

### Fetchurl and Unpack stages

Pylightnix allows us to define, check and execute data processing
operations called **Stages**. Stages may be defined by writing Python
functions (as we will do later) or imported from a small builtin
collection.

Here we import stages `fetchurl2` and `unpack`, along with other
Pylightnix API functions.

``` python
from pylightnix import (fetchurl2, unpack, DRef, RRef, instantiate_inplace,
                        realize_inplace, mklens, selfref)
```

Our goal is to prepare stages for execution by **instantiating** them.
`fetchurl2` is the curl-based web downloader, which accepts the URL
address, the hash and the expected `out` path. We call
`instantiate_inplace` API function on it and get the `tarball`
derivation reference, which identifies both the stage and its parameters
in the Pylightnix storage. No actual work is performed yet.

``` python
hello_version = '2.10'

tarball:DRef = \
  instantiate_inplace(
    fetchurl2,
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b',
    out=[selfref, f'hello-{hello_version}.tar.gz'])
```

Next we pass the path to the tarball to the `unpack` stage by
dereferencing its `out` attribute using the
[mklens](../Reference.md#pylightnix.lens.mklens) helper function.
Pylightnix notes the fact that `unpack` has a reference to `tarball` in
its configuration.

``` python
hello_src:DRef = \
  instantiate_inplace(
    unpack,
    name='unpack-hello',
    refpath=mklens(tarball).out.refpath,
    src=[selfref, f'hello-{hello_version}'])
```

Now, we ask Pylightnix to give us the artifacts of `unpack` stage by
**realizing** it. Pylightnix does the dependency handling and decides to
execute both fetchurl and unpack. The results of realization is
available via realization reference `hello_rref`.

``` python
hello_rref:RRef = realize_inplace(hello_src)
print(hello_rref)
```

``` stdout
hello-2.10/
hello-2.10/COPYING
hello-2.10/tests/
hello-2.10/tests/greeting-1
hello-2.10/tests/traditional-1
hello-2.10/tests/greeting-2
hello-2.10/tests/hello-1
hello-2.10/tests/last-1
hello-2.10/Makefile.am
hello-2.10/config.in
hello-2.10/maint.mk
hello-2.10/README
hello-2.10/INSTALL
hello-2.10/NEWS
hello-2.10/GNUmakefile
hello-2.10/TODO
hello-2.10/ABOUT-NLS
hello-2.10/README-release
hello-2.10/THANKS
hello-2.10/po/
hello-2.10/po/lv.gmo
hello-2.10/po/he.gmo
hello-2.10/po/hu.gmo
hello-2.10/po/quot.sed
hello-2.10/po/pl.gmo
hello-2.10/po/id.gmo
hello-2.10/po/de.po
hello-2.10/po/sv.po
hello-2.10/po/insert-header.sin
hello-2.10/po/nn.gmo
hello-2.10/po/ro.po
hello-2.10/po/tr.po
hello-2.10/po/sl.po
hello-2.10/po/gl.gmo
hello-2.10/po/nb.po
hello-2.10/po/it.po
hello-2.10/po/zh_TW.gmo
hello-2.10/po/vi.gmo
hello-2.10/po/vi.po
hello-2.10/po/hr.gmo
hello-2.10/po/pl.po
hello-2.10/po/POTFILES.in
hello-2.10/po/stamp-po
hello-2.10/po/nl.po
hello-2.10/po/en@boldquot.header
hello-2.10/po/fa.gmo
hello-2.10/po/hr.po
hello-2.10/po/zh_CN.gmo
hello-2.10/po/fi.po
hello-2.10/po/th.gmo
hello-2.10/po/pt_BR.gmo
hello-2.10/po/es.gmo
hello-2.10/po/nb.gmo
hello-2.10/po/th.po
hello-2.10/po/ka.po
hello-2.10/po/Rules-quot
hello-2.10/po/eu.po
hello-2.10/po/sv.gmo
hello-2.10/po/es.po
hello-2.10/po/de.gmo
hello-2.10/po/pt_BR.po
hello-2.10/po/el.gmo
hello-2.10/po/en@quot.header
hello-2.10/po/ko.gmo
hello-2.10/po/zh_CN.po
hello-2.10/po/ka.gmo
hello-2.10/po/hello.pot
hello-2.10/po/fi.gmo
hello-2.10/po/Makevars
hello-2.10/po/ro.gmo
hello-2.10/po/hu.po
hello-2.10/po/fa.po
hello-2.10/po/da.po
hello-2.10/po/it.gmo
hello-2.10/po/bg.gmo
hello-2.10/po/ru.po
hello-2.10/po/zh_TW.po
hello-2.10/po/nn.po
hello-2.10/po/ko.po
hello-2.10/po/sr.gmo
hello-2.10/po/tr.gmo
hello-2.10/po/remove-potcdate.sin
hello-2.10/po/LINGUAS
hello-2.10/po/pt.po
hello-2.10/po/ru.gmo
hello-2.10/po/nl.gmo
hello-2.10/po/uk.po
hello-2.10/po/ms.po
hello-2.10/po/ga.po
hello-2.10/po/et.po
hello-2.10/po/fr.po
hello-2.10/po/gl.po
hello-2.10/po/sl.gmo
hello-2.10/po/bg.po
hello-2.10/po/sk.gmo
hello-2.10/po/ja.gmo
hello-2.10/po/ga.gmo
hello-2.10/po/ca.gmo
hello-2.10/po/he.po
hello-2.10/po/lv.po
hello-2.10/po/boldquot.sed
hello-2.10/po/sr.po
hello-2.10/po/el.po
hello-2.10/po/da.gmo
hello-2.10/po/ChangeLog
hello-2.10/po/ms.gmo
hello-2.10/po/ca.po
hello-2.10/po/Makefile.in.in
hello-2.10/po/pt.gmo
hello-2.10/po/uk.gmo
hello-2.10/po/et.gmo
hello-2.10/po/eu.gmo
hello-2.10/po/sk.po
hello-2.10/po/eo.gmo
hello-2.10/po/id.po
hello-2.10/po/ja.po
hello-2.10/po/eo.po
hello-2.10/po/fr.gmo
hello-2.10/ChangeLog.O
hello-2.10/build-aux/
hello-2.10/build-aux/update-copyright
hello-2.10/build-aux/mdate-sh
hello-2.10/build-aux/config.guess
hello-2.10/build-aux/depcomp
hello-2.10/build-aux/config.rpath
hello-2.10/build-aux/compile
hello-2.10/build-aux/gitlog-to-changelog
hello-2.10/build-aux/useless-if-before-free
hello-2.10/build-aux/announce-gen
hello-2.10/build-aux/test-driver
hello-2.10/build-aux/config.sub
hello-2.10/build-aux/install-sh
hello-2.10/build-aux/gnupload
hello-2.10/build-aux/gnu-web-doc-update
hello-2.10/build-aux/texinfo.tex
hello-2.10/build-aux/gendocs.sh
hello-2.10/build-aux/do-release-commit-and-tag
hello-2.10/build-aux/missing
hello-2.10/build-aux/snippet/
hello-2.10/build-aux/snippet/arg-nonnull.h
hello-2.10/build-aux/snippet/warn-on-use.h
hello-2.10/build-aux/snippet/_Noreturn.h
hello-2.10/build-aux/snippet/c++defs.h
hello-2.10/build-aux/vc-list-files
hello-2.10/build-aux/prefix-gnulib-mk
hello-2.10/AUTHORS
hello-2.10/man/
hello-2.10/man/hello.x
hello-2.10/configure.ac
hello-2.10/lib/
hello-2.10/lib/basename-lgpl.c
hello-2.10/lib/stdlib.in.h
hello-2.10/lib/c-strncasecmp.c
hello-2.10/lib/sys_types.in.h
hello-2.10/lib/c-strcase.h
hello-2.10/lib/stdbool.in.h
hello-2.10/lib/localcharset.c
hello-2.10/lib/exitfail.c
hello-2.10/lib/mbsinit.c
hello-2.10/lib/xstrndup.h
hello-2.10/lib/gnulib.mk
hello-2.10/lib/msvc-nothrow.c
hello-2.10/lib/stddef.in.h
hello-2.10/lib/c-ctype.h
hello-2.10/lib/close-stream.h
hello-2.10/lib/dirname-lgpl.c
hello-2.10/lib/verify.h
hello-2.10/lib/progname.h
hello-2.10/lib/basename.c
hello-2.10/lib/unistd.c
hello-2.10/lib/fpending.h
hello-2.10/lib/strnlen1.h
hello-2.10/lib/getopt.c
hello-2.10/lib/mbsrtowcs.c
hello-2.10/lib/c-ctype.c
hello-2.10/lib/localcharset.h
hello-2.10/lib/ref-add.sin
hello-2.10/lib/xalloc.h
hello-2.10/lib/close-stream.c
hello-2.10/lib/wctype-h.c
hello-2.10/lib/closeout.h
hello-2.10/lib/dirname.h
hello-2.10/lib/memchr.valgrind
hello-2.10/lib/wctype.in.h
hello-2.10/lib/strndup.c
hello-2.10/lib/xstrndup.c
hello-2.10/lib/quotearg.c
hello-2.10/lib/xalloc-oversized.h
hello-2.10/lib/mbsrtowcs-state.c
hello-2.10/lib/exitfail.h
hello-2.10/lib/errno.in.h
hello-2.10/lib/strerror.c
hello-2.10/lib/local.mk
hello-2.10/lib/error.c
hello-2.10/lib/ref-del.sin
hello-2.10/lib/xalloc-die.c
hello-2.10/lib/getopt1.c
hello-2.10/lib/getopt_int.h
hello-2.10/lib/strnlen.c
hello-2.10/lib/getopt.in.h
hello-2.10/lib/strerror-override.c
hello-2.10/lib/error.h
hello-2.10/lib/strerror-override.h
hello-2.10/lib/unistd.in.h
hello-2.10/lib/progname.c
hello-2.10/lib/closeout.c
hello-2.10/lib/malloc.c
hello-2.10/lib/msvc-inval.c
hello-2.10/lib/mbrtowc.c
hello-2.10/lib/gettext.h
hello-2.10/lib/quotearg.h
hello-2.10/lib/string.in.h
hello-2.10/lib/wchar.in.h
hello-2.10/lib/intprops.h
hello-2.10/lib/streq.h
hello-2.10/lib/stdio.in.h
hello-2.10/lib/memchr.c
hello-2.10/lib/fpending.c
hello-2.10/lib/dosname.h
hello-2.10/lib/config.charset
hello-2.10/lib/strnlen1.c
hello-2.10/lib/dirname.c
hello-2.10/lib/msvc-inval.h
hello-2.10/lib/stripslash.c
hello-2.10/lib/c-strcaseeq.h
hello-2.10/lib/quote.h
hello-2.10/lib/c-strcasecmp.c
hello-2.10/lib/mbsrtowcs-impl.h
hello-2.10/lib/xmalloc.c
hello-2.10/lib/msvc-nothrow.h
hello-2.10/Makefile.in
hello-2.10/doc/
hello-2.10/doc/fdl.texi
hello-2.10/doc/local.mk
hello-2.10/doc/version.texi
hello-2.10/doc/stamp-vti
hello-2.10/doc/hello.texi
hello-2.10/doc/hello.info
hello-2.10/ChangeLog
hello-2.10/README-dev
hello-2.10/hello.1
hello-2.10/configure
hello-2.10/src/
hello-2.10/src/hello.c
hello-2.10/src/system.h
hello-2.10/aclocal.m4
hello-2.10/m4/
hello-2.10/m4/extensions.m4
hello-2.10/m4/localcharset.m4
hello-2.10/m4/ssize_t.m4
hello-2.10/m4/gnulib-cache.m4
hello-2.10/m4/wctype_h.m4
hello-2.10/m4/intlmacosx.m4
hello-2.10/m4/codeset.m4
hello-2.10/m4/include_next.m4
hello-2.10/m4/locale-zh.m4
hello-2.10/m4/gettext.m4
hello-2.10/m4/strerror.m4
hello-2.10/m4/xstrndup.m4
hello-2.10/m4/lib-ld.m4
hello-2.10/m4/xalloc.m4
hello-2.10/m4/strndup.m4
hello-2.10/m4/double-slash-root.m4
hello-2.10/m4/mbsrtowcs.m4
hello-2.10/m4/unistd_h.m4
hello-2.10/m4/closeout.m4
hello-2.10/m4/warn-on-use.m4
hello-2.10/m4/error.m4
hello-2.10/m4/errno_h.m4
hello-2.10/m4/stddef_h.m4
hello-2.10/m4/stdio_h.m4
hello-2.10/m4/non-recursive-gnulib-prefix-hack.m4
hello-2.10/m4/stdlib_h.m4
hello-2.10/m4/locale-fr.m4
hello-2.10/m4/iconv.m4
hello-2.10/m4/memchr.m4
hello-2.10/m4/string_h.m4
hello-2.10/m4/gnulib-comp.m4
hello-2.10/m4/gnulib-common.m4
hello-2.10/m4/extern-inline.m4
hello-2.10/m4/wchar_h.m4
hello-2.10/m4/close-stream.m4
hello-2.10/m4/msvc-nothrow.m4
hello-2.10/m4/lib-prefix.m4
hello-2.10/m4/quotearg.m4
hello-2.10/m4/mmap-anon.m4
hello-2.10/m4/fcntl-o.m4
hello-2.10/m4/off_t.m4
hello-2.10/m4/absolute-header.m4
hello-2.10/m4/glibc21.m4
hello-2.10/m4/wint_t.m4
hello-2.10/m4/nls.m4
hello-2.10/m4/malloc.m4
hello-2.10/m4/mbsinit.m4
hello-2.10/m4/fpending.m4
hello-2.10/m4/00gnulib.m4
hello-2.10/m4/po.m4
hello-2.10/m4/strnlen.m4
hello-2.10/m4/getopt.m4
hello-2.10/m4/sys_types_h.m4
hello-2.10/m4/stdbool.m4
hello-2.10/m4/configmake.m4
hello-2.10/m4/sys_socket_h.m4
hello-2.10/m4/msvc-inval.m4
hello-2.10/m4/dirname.m4
hello-2.10/m4/nocrash.m4
hello-2.10/m4/locale-ja.m4
hello-2.10/m4/lib-link.m4
hello-2.10/m4/mbstate_t.m4
hello-2.10/m4/progtest.m4
hello-2.10/m4/wchar_t.m4
hello-2.10/m4/mbrtowc.m4
hello-2.10/contrib/
hello-2.10/contrib/evolution.txt
hello-2.10/contrib/de_franconian_po.txt
rref:b557aecd2a8cc4615100d8b4a5129874-60333c6d4a9ccf5392405086013c0a3b-unpack-hello
```

``` stderr
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  6  708k    6 44434    0     0  97442      0  0:00:07 --:--:--  0:00:07 97229
100  708k  100  708k    0     0   860k      0 --:--:-- --:--:-- --:--:--  859k
hello-2.10.tar.gz: extracted to `hello-2.10'
```

Any RRef could be converted to the system path by calling
[rref2path](../Reference.md#pylightnix.core.rref2path) function or by
using a more feature-rich `mklens`:

``` python
from pylightnix import rref2path

print(rref2path(hello_rref))
print(mklens(hello_rref).val)
print(mklens(hello_rref).syspath)
print(mklens(hello_rref).src.syspath)
```

``` stdout
/tmp/pylightnix_hello_demo/store-v0/60333c6d4a9ccf5392405086013c0a3b-unpack-hello/b557aecd2a8cc4615100d8b4a5129874
rref:b557aecd2a8cc4615100d8b4a5129874-60333c6d4a9ccf5392405086013c0a3b-unpack-hello
/tmp/pylightnix_hello_demo/store-v0/60333c6d4a9ccf5392405086013c0a3b-unpack-hello/b557aecd2a8cc4615100d8b4a5129874
/tmp/pylightnix_hello_demo/store-v0/60333c6d4a9ccf5392405086013c0a3b-unpack-hello/b557aecd2a8cc4615100d8b4a5129874/hello-2.10
```

Pylightnix offers a number of other shell-like helper functions for
accessing realization, like `lsref`:

``` python
from pylightnix import lsref

print(lsref(hello_rref))
```

``` stdout
['context.json', '__buildstart__.txt', 'hello-2.10', '__buildstop__.txt']
```

### A custom compile stage

In this section we define a custom stage to build the newly obtained
sources of GNU Hello application.

Defining Pylighnix stages requires us to provide Pylightnix with the
following components:

-   The JSON-like configuration object.
-   The matcher Python function, dealing with non-determenistic builds.
-   The realizer Python function which specifies the actual build
    process.

The matcher business is beyond the scope of this tutorial. We will use a
trivial `match_only` matcher which instructs Pylightnix to expect no
more than one realization of a stage in its storage.

We produce a `Config` object by returning it from a `_config` function.
Note, that `locals()` is a Python builtin function which returns a
`dict` of current function’s local variables.

``` python
from pylightnix import Config, mkconfig, mklens, selfref

def hello_config()->Config:
  name = 'hello-bin'
  src = mklens(hello_src).src.refpath
  out_hello = [selfref, 'usr', 'bin', 'hello']
  out_log = [selfref, 'build.log']
  return mkconfig(locals())
```

Realizer is another Python function accepting a `Build` context. We
could use `mklens` to query the parameters of the derivation being built
just as we used it for querying parameters of completed realizations.

``` python
from pylightnix import (Path, Build, build_cattrs, build_outpath, build_path,
                        dirrw )

def hello_realize(b:Build)->None:
  with TemporaryDirectory() as tmp:
    copytree(mklens(b).src.syspath,join(tmp,'src'))
    dirrw(Path(join(tmp,'src')))
    cwd = getcwd()
    try:
      chdir(join(tmp,'src'))
      system(f'( ./configure --prefix=/usr && '
             f'  make &&'
             f'  make install DESTDIR={mklens(b).syspath}'
             f')>{mklens(b).out_log.syspath} 2>&1')
    finally:
      chdir(cwd)
```

Finally, we introduce a new stage to Pylightnix by instantiating a
generic [mkdrv](../Reference.md#pylightnix.core.mkdrv) stage:

``` python
from pylightnix import mkdrv, build_wrapper, match_only

hello:DRef = \
  instantiate_inplace(mkdrv, hello_config(), match_only(), build_wrapper(hello_realize))

print(hello)
```

``` stdout
dref:c33deedd371c5de747a5610dc3900dcf-hello-bin
```

As before, we get a `DRef`, which means that basic checks were passed,
and then call a `realize` on it:

``` python
rref:RRef=realize_inplace(hello)
print(rref)
```

``` stdout
rref:64fb50c1c2689c34a236708cabef62e9-c33deedd371c5de747a5610dc3900dcf-hello-bin
```

### Accessing the results

Finally, we convert RRef to the system path and run the GNU Hello
binary.

``` python
print(Popen([mklens(rref).out_hello.syspath],
            stdout=PIPE, shell=True).stdout.read()) # type:ignore
```

``` stdout
b'Hello, world!\n'
```
