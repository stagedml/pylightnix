-   [GNU Hello demo](#gnu-hello-demo)
    -   [Task](#task)
    -   [Implementation](#implementation)
        -   [Basic terms](#basic-terms)
        -   [Custom stages](#custom-stages)

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

(Here we also call `dirrm` to *clear* the storage to demonstrate how do
realizers work)

Location of the storage is kept in an internal global variable and
normally shouldn’t be changed during the work, but since Pylightnix
doesnt run any background services, it is totally up ot you. Read the
[initialize docstring
reference](../Reference.md#pylightnix.core.initialize) for details.

Note that in most applications we don’t really need to initialize a
separate storage, but could safely use the default one. To check or
initialize default storage, just call `initialize()` without arguments.

### Basic terms

Pylightnix allows us to define, check and execute data processing
operations called **stages**. We will define a custom stage later, for
now we use a builtin stage `fetchurl` (which is an analog of `fetchurl`
expression of Nix package manager).

``` python
from pylightnix import DRef, instantiate_inplace, fetchurl, selfref

hello_version = '2.10'

hello_src:DRef = \
  instantiate_inplace(
    fetchurl,
    name='hello-src',
    url=f'http://ftp.gnu.org/gnu/hello/hello-{hello_version}.tar.gz',
    sha256='31e066137a962676e89f69d1b65382de95a7ef7d914b8cb956f41ea72e0f516b',
    src=[selfref, f'hello-{hello_version}'])
```

By this definition we created `hello_src` variable of type
[DRef](../Reference.md#pylightnix.types.DRef) which holds a reference to
a **Derivation** of fetchurl stage. By specifying **PromisePath** src,
we promise that realizations of this derivation will contain named file
or folder. In this case we expect that ‘hello-2.10’ folder will exist.
Pylightnix will check this promise and raise the exception if it is not
fulfilled.

Having a `hello_src` derivation reference means several things:

-   (a) Configuration of the corresponding stage has passed certain
        checks and does exist in the storage as a JSON object.

-   (b) Pylighnix knows how to **Realize** this stage, i.e. it has a
        Python function to produce some data (files) to put them in
        storage.

-   (c) Pylightnix noted the
        [promise](../Reference.md#pylightnix.types.PromisePath) made by
        `hello_src`. After it’s realization, it will check that
        `hello-2.10` folder appears among build artifacts.

For [fetchurl](../Reference.md#pylightnix.stages.fetchurl.fetchurl), the
output data will contain the contents of URL, after downloading and
unpacking. In this case, we expect to see `hello-2.10` folder,
containing the hello’s sources. Let’s check it:

``` python
from pylightnix import RRef, realize_inplace

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
rref:ff001de6af7b8772d89d5cc68f063242-95684cef96ee35949ccb49ac064598f7-hello-src
```

``` stderr
--2021-08-25 02:21:23--  http://ftp.gnu.org/gnu/hello/hello-2.10.tar.gz
Распознаётся ftp.gnu.org (ftp.gnu.org)… 209.51.188.20, 2001:470:142:3::b
Подключение к ftp.gnu.org (ftp.gnu.org)|209.51.188.20|:80... соединение установлено.
HTTP-запрос отправлен. Ожидание ответа… 200 OK
Длина: 725946 (709K) [application/x-gzip]
Сохранение в: «/tmp/pylightnix_hello_demo/tmp/fetchurl/hello-2.10.tar.gz.tmp»

     0K .......... .......... .......... .......... ..........  7%  219K 3s
    50K .......... .......... .......... .......... .......... 14%  444K 2s
   100K .......... .......... .......... .......... .......... 21% 10,7M 1s
   150K .......... .......... .......... .......... .......... 28% 11,2M 1s
   200K .......... .......... .......... .......... .......... 35%  464K 1s
   250K .......... .......... .......... .......... .......... 42% 10,6M 1s
   300K .......... .......... .......... .......... .......... 49% 11,2M 0s
   350K .......... .......... .......... .......... .......... 56% 11,0M 0s
   400K .......... .......... .......... .......... .......... 63%  513K 0s
   450K .......... .......... .......... .......... .......... 70% 11,2M 0s
   500K .......... .......... .......... .......... .......... 77% 10,6M 0s
   550K .......... .......... .......... .......... .......... 84% 11,0M 0s
   600K .......... .......... .......... .......... .......... 91% 11,3M 0s
   650K .......... .......... .......... .......... .......... 98% 11,8M 0s
   700K ........                                              100% 10,3M=0,6s

2021-08-25 02:21:23 (1,17 MB/s) - «/tmp/pylightnix_hello_demo/tmp/fetchurl/hello-2.10.tar.gz.tmp» сохранён [725946/725946]

hello-2.10.tar.gz: extracted to `hello-2.10'
```

OK, now we should see the signs of actual work being done. Something was
just downloaded and we also see a string starting with ‘rref:…’ in
*stdout*. This string is a **Realization reference** of type
[RRef](../Reference.md#pylightnix.types.RRef), it uniquely identifies
some data in the Pylightnix filesystem storage.

Any RRef could be converted to system by calling
[rref2path](../Reference.md#pylightnix.core.rref2path) function:

``` python
from pylightnix import rref2path

print(rref2path(hello_rref))
```

``` stdout
/tmp/pylightnix_hello_demo/store-v0/95684cef96ee35949ccb49ac064598f7-hello-src/ff001de6af7b8772d89d5cc68f063242
```

Also, Pylightnix offers a shell-like helper functions to quickly examine
the content of references. One of them is `lsref`:

``` python
from pylightnix import lsref

print(lsref(hello_rref))
```

``` stdout
['context.json', '__buildstart__.txt', 'hello-2.10', '__buildstop__.txt']
```

### Custom stages

We want to build the GNU hello, so we need some code to do this job.
Pylighnix aims at providing only a generic minimalistic API, so it
doesn’t have a builtin stage for compiling applications. Luckily, it is
not hard to define it, as we should see.

All Pylighnix stages consist of three important components:

-   The configuration, which is a JSON-Object of parameters and
    references
-   The matcher, which is a Python function for dealing with
    non-determenistic builds.
-   The realizer, which is a Python function encoding the actual build
    process

The matcher business is beyond the scope of this tutorial. We will use
trivial `match_only` matcher which asks the core to build the stage and
then returns build result.

#### Configuration

Let’s deal with other two components. We start by defining a
configuration:

``` python
from pylightnix import Config, mkconfig, mklens

def hello_config()->Config:
  name = 'hello-bin'
  src = mklens(hello_src).src.refpath
  return mkconfig(locals())
```

Here, we specify two configuration attributes: a name and a
[RefPath](../Reference.md#pylightnix.types.RefPath) which links our new
stage with some realization of the previous stage. RefPath is normally a
Python list `[hello_src, 'hello-2.10']`, but the
[Lens](../Reference.md#pylightnix.lens.Lens) helper gets this value for
us based on a promise made by this dependency. We will convert it into a
system path at the time of realization, as we will see soon.

As a side note, `locals()` is a Python builtin function which returns a
`dict` of current function’s local variables.

*Note, we should only use **Derivation references** in configurations.
Realization references are accessible either from global scope or from
realize functions*

#### Realization

Let’s now move to the realization part of our Hello builder stage:

``` python
from pylightnix import ( Path, Build, build_cattrs, build_outpath, build_path, dirrw )

def hello_realize(b:Build)->None:
  with TemporaryDirectory() as tmp:
    copytree(mklens(b).src.syspath,join(tmp,'src'))
    dirrw(Path(join(tmp,'src')))
    cwd = getcwd()
    try:
      chdir(join(tmp,'src'))
      system(f'./configure --prefix=/usr')
      system(f'make')
      system(f'make install DESTDIR={mklens(b).syspath}')
    finally:
      chdir(cwd)
```

Another interesting thing is the call to `build_path` function. It is
the point where we **Dereference refpaths** by converting them into
system paths. Pylightnix guarantees that referenced stages are already
realized at the time of dereferencing.

The rest is simple. We copy sources to the temp folder and perform the
usual configure-make-install on it.

#### Running the stage

Finally, we introduce our new stage to Pylightnix:

``` python
from pylightnix import mkdrv, build_wrapper, match_only

hello:DRef = \
  instantiate_inplace(mkdrv, hello_config(), match_only(), build_wrapper(hello_realize))

print(hello)
```

``` stdout
dref:b2a453f8cef994367d10b903236d06ef-hello-bin
```

In this instantiation, [mkdrv](../Reference.md#pylightnix.core.mkdrv)
(which stands for ‘make derivation’) plays the role of `fetchurl` from
the previous stage. As before, we first get a `DRef`, which means that
basic checks were passed, and then call `realize`:

``` python
rref:RRef=realize_inplace(hello)
print(rref)
```

``` stdout
checking for a BSD-compatible install... /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/install -c
checking whether build environment is sane... yes
checking for a thread-safe mkdir -p... /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/mkdir -p
checking for gawk... gawk
checking whether make sets $(MAKE)... yes
checking whether make supports nested variables... yes
checking for gcc... gcc
checking whether the C compiler works... yes
checking for C compiler default output file name... a.out
checking for suffix of executables... 
checking whether we are cross compiling... no
checking for suffix of object files... o
checking whether we are using the GNU C compiler... yes
checking whether gcc accepts -g... yes
checking for gcc option to accept ISO C89... none needed
checking whether gcc understands -c and -o together... yes
checking for style of include used by make... GNU
checking dependency style of gcc... gcc3
checking how to run the C preprocessor... gcc -E
checking for grep that handles long lines and -e... /nix/store/b0vjq4r4sp9z4l2gbkc5dyyw5qfgyi3r-gnugrep-3.4/bin/grep
checking for egrep... /nix/store/b0vjq4r4sp9z4l2gbkc5dyyw5qfgyi3r-gnugrep-3.4/bin/grep -E
checking for Minix Amsterdam compiler... no
checking for ANSI C header files... yes
checking for sys/types.h... yes
checking for sys/stat.h... yes
checking for stdlib.h... yes
checking for string.h... yes
checking for memory.h... yes
checking for strings.h... yes
checking for inttypes.h... yes
checking for stdint.h... yes
checking for unistd.h... yes
checking minix/config.h usability... no
checking minix/config.h presence... no
checking for minix/config.h... no
checking whether it is safe to define __EXTENSIONS__... yes
checking whether _XOPEN_SOURCE should be defined... no
checking build system type... x86_64-unknown-linux-gnu
checking host system type... x86_64-unknown-linux-gnu
checking whether // is distinct from /... no
checking whether the preprocessor supports include_next... yes
checking whether system header files limit the line length... no
checking for complete errno.h... yes
checking whether strerror_r is declared... yes
checking for strerror_r... yes
checking whether strerror_r returns char *... yes
checking for stdio_ext.h... yes
checking for getopt.h... yes
checking for unistd.h... (cached) yes
checking for sys/mman.h... yes
checking for sys/socket.h... yes
checking for wchar.h... yes
checking for features.h... yes
checking for wctype.h... yes
checking for getopt.h... (cached) yes
checking for getopt_long_only... yes
checking whether getopt is POSIX compatible... yes
checking for working GNU getopt function... yes
checking for working GNU getopt_long function... yes
checking whether getenv is declared... yes
checking for nl_langinfo and CODESET... yes
checking for symlink... yes
checking for mbsinit... yes
checking for mbrtowc... yes
checking for mbsrtowcs... yes
checking for mprotect... yes
checking for _set_invalid_parameter_handler... no
checking for strndup... yes
checking for iswcntrl... yes
checking for working fcntl.h... yes
checking whether getc_unlocked is declared... yes
checking whether we are using the GNU C Library >= 2.1 or uClibc... yes
checking for a sed that does not truncate output... /nix/store/p34p7ysy84579lndk7rbrz6zsfr03y71-gnused-4.8/bin/sed
checking whether malloc, realloc, calloc are POSIX compliant... yes
checking for mbstate_t... yes
checking for a traditional japanese locale... ja_JP
checking for a transitional chinese locale... zh_CN.GB18030
checking for a french Unicode locale... fr_FR.UTF-8
checking for a traditional french locale... fr_FR
checking for mmap... yes
checking for MAP_ANONYMOUS... yes
checking whether memchr works... yes
checking for stdbool.h that conforms to C99... yes
checking for _Bool... yes
checking for wchar_t... yes
checking whether strerror(0) succeeds... yes
checking for C/C++ restrict keyword... __restrict
checking whether ffsl is declared without a macro... yes
checking whether ffsll is declared without a macro... yes
checking whether memmem is declared without a macro... yes
checking whether mempcpy is declared without a macro... yes
checking whether memrchr is declared without a macro... yes
checking whether rawmemchr is declared without a macro... yes
checking whether stpcpy is declared without a macro... yes
checking whether stpncpy is declared without a macro... yes
checking whether strchrnul is declared without a macro... yes
checking whether strdup is declared without a macro... yes
checking whether strncat is declared without a macro... yes
checking whether strndup is declared without a macro... yes
checking whether strnlen is declared without a macro... yes
checking whether strpbrk is declared without a macro... yes
checking whether strsep is declared without a macro... yes
checking whether strcasestr is declared without a macro... yes
checking whether strtok_r is declared without a macro... yes
checking whether strerror_r is declared without a macro... yes
checking whether strsignal is declared without a macro... yes
checking whether strverscmp is declared without a macro... yes
checking whether strndup is declared... (cached) yes
checking whether strnlen is declared... (cached) yes
checking for pid_t... yes
checking for mode_t... yes
checking whether <wchar.h> uses 'inline' correctly... yes
checking for wint_t... yes
checking whether // is distinct from /... (cached) no
checking for error_at_line... yes
checking for __fpending... yes
checking whether __fpending is declared... yes
checking whether mbrtowc handles incomplete characters... yes
checking whether mbrtowc works as well as mbtowc... yes
checking whether mbrtowc handles a NULL pwc argument... yes
checking whether mbrtowc handles a NULL string argument... yes
checking whether mbrtowc has a correct return value... yes
checking whether mbrtowc returns 0 when parsing a NUL character... yes
checking whether mbrtowc works on empty input... yes
checking whether mbrtowc handles incomplete characters... (cached) yes
checking whether mbrtowc works as well as mbtowc... (cached) yes
checking whether mbrtowc handles incomplete characters... (cached) yes
checking whether mbrtowc works as well as mbtowc... (cached) yes
checking whether mbsrtowcs works... yes
checking whether program_invocation_name is declared... yes
checking whether program_invocation_short_name is declared... yes
checking for ssize_t... yes
checking whether NULL can be used in arbitrary expressions... yes
checking whether dprintf is declared without a macro... yes
checking whether fpurge is declared without a macro... no
checking whether fseeko is declared without a macro... yes
checking whether ftello is declared without a macro... yes
checking whether getdelim is declared without a macro... yes
checking whether getline is declared without a macro... yes
checking whether gets is declared without a macro... no
checking whether pclose is declared without a macro... yes
checking whether popen is declared without a macro... yes
checking whether renameat is declared without a macro... yes
checking whether snprintf is declared without a macro... yes
checking whether tmpfile is declared without a macro... yes
checking whether vdprintf is declared without a macro... yes
checking whether vsnprintf is declared without a macro... yes
checking whether _Exit is declared without a macro... yes
checking whether atoll is declared without a macro... yes
checking whether canonicalize_file_name is declared without a macro... yes
checking whether getloadavg is declared without a macro... yes
checking whether getsubopt is declared without a macro... yes
checking whether grantpt is declared without a macro... yes
checking whether initstate is declared without a macro... yes
checking whether initstate_r is declared without a macro... yes
checking whether mkdtemp is declared without a macro... yes
checking whether mkostemp is declared without a macro... yes
checking whether mkostemps is declared without a macro... yes
checking whether mkstemp is declared without a macro... yes
checking whether mkstemps is declared without a macro... yes
checking whether posix_openpt is declared without a macro... yes
checking whether ptsname is declared without a macro... yes
checking whether ptsname_r is declared without a macro... yes
checking whether random is declared without a macro... yes
checking whether random_r is declared without a macro... yes
checking whether realpath is declared without a macro... yes
checking whether rpmatch is declared without a macro... yes
checking whether secure_getenv is declared without a macro... yes
checking whether setenv is declared without a macro... yes
checking whether setstate is declared without a macro... yes
checking whether setstate_r is declared without a macro... yes
checking whether srandom is declared without a macro... yes
checking whether srandom_r is declared without a macro... yes
checking whether strtod is declared without a macro... yes
checking whether strtoll is declared without a macro... yes
checking whether strtoull is declared without a macro... yes
checking whether unlockpt is declared without a macro... yes
checking whether unsetenv is declared without a macro... yes
checking for working strerror function... yes
checking for working strndup... yes
checking for working strnlen... yes
checking whether chdir is declared without a macro... yes
checking whether chown is declared without a macro... yes
checking whether dup is declared without a macro... yes
checking whether dup2 is declared without a macro... yes
checking whether dup3 is declared without a macro... yes
checking whether environ is declared without a macro... yes
checking whether euidaccess is declared without a macro... yes
checking whether faccessat is declared without a macro... yes
checking whether fchdir is declared without a macro... yes
checking whether fchownat is declared without a macro... yes
checking whether fdatasync is declared without a macro... yes
checking whether fsync is declared without a macro... yes
checking whether ftruncate is declared without a macro... yes
checking whether getcwd is declared without a macro... yes
checking whether getdomainname is declared without a macro... yes
checking whether getdtablesize is declared without a macro... yes
checking whether getgroups is declared without a macro... yes
checking whether gethostname is declared without a macro... yes
checking whether getlogin is declared without a macro... yes
checking whether getlogin_r is declared without a macro... yes
checking whether getpagesize is declared without a macro... yes
checking whether getusershell is declared without a macro... yes
checking whether setusershell is declared without a macro... yes
checking whether endusershell is declared without a macro... yes
checking whether group_member is declared without a macro... yes
checking whether isatty is declared without a macro... yes
checking whether lchown is declared without a macro... yes
checking whether link is declared without a macro... yes
checking whether linkat is declared without a macro... yes
checking whether lseek is declared without a macro... yes
checking whether pipe is declared without a macro... yes
checking whether pipe2 is declared without a macro... yes
checking whether pread is declared without a macro... yes
checking whether pwrite is declared without a macro... yes
checking whether readlink is declared without a macro... yes
checking whether readlinkat is declared without a macro... yes
checking whether rmdir is declared without a macro... yes
checking whether sethostname is declared without a macro... yes
checking whether sleep is declared without a macro... yes
checking whether symlink is declared without a macro... yes
checking whether symlinkat is declared without a macro... yes
checking whether ttyname_r is declared without a macro... yes
checking whether unlink is declared without a macro... yes
checking whether unlinkat is declared without a macro... yes
checking whether usleep is declared without a macro... yes
checking whether btowc is declared without a macro... yes
checking whether wctob is declared without a macro... yes
checking whether mbsinit is declared without a macro... yes
checking whether mbrtowc is declared without a macro... yes
checking whether mbrlen is declared without a macro... yes
checking whether mbsrtowcs is declared without a macro... yes
checking whether mbsnrtowcs is declared without a macro... yes
checking whether wcrtomb is declared without a macro... yes
checking whether wcsrtombs is declared without a macro... yes
checking whether wcsnrtombs is declared without a macro... yes
checking whether wcwidth is declared without a macro... yes
checking whether wmemchr is declared without a macro... yes
checking whether wmemcmp is declared without a macro... yes
checking whether wmemcpy is declared without a macro... yes
checking whether wmemmove is declared without a macro... yes
checking whether wmemset is declared without a macro... yes
checking whether wcslen is declared without a macro... yes
checking whether wcsnlen is declared without a macro... yes
checking whether wcscpy is declared without a macro... yes
checking whether wcpcpy is declared without a macro... yes
checking whether wcsncpy is declared without a macro... yes
checking whether wcpncpy is declared without a macro... yes
checking whether wcscat is declared without a macro... yes
checking whether wcsncat is declared without a macro... yes
checking whether wcscmp is declared without a macro... yes
checking whether wcsncmp is declared without a macro... yes
checking whether wcscasecmp is declared without a macro... yes
checking whether wcsncasecmp is declared without a macro... yes
checking whether wcscoll is declared without a macro... yes
checking whether wcsxfrm is declared without a macro... yes
checking whether wcsdup is declared without a macro... yes
checking whether wcschr is declared without a macro... yes
checking whether wcsrchr is declared without a macro... yes
checking whether wcscspn is declared without a macro... yes
checking whether wcsspn is declared without a macro... yes
checking whether wcspbrk is declared without a macro... yes
checking whether wcsstr is declared without a macro... yes
checking whether wcstok is declared without a macro... yes
checking whether wcswidth is declared without a macro... yes
checking whether iswcntrl works... yes
checking for towlower... yes
checking for wctype_t... yes
checking for wctrans_t... yes
checking whether wctype is declared without a macro... yes
checking whether iswctype is declared without a macro... yes
checking whether wctrans is declared without a macro... yes
checking whether towctrans is declared without a macro... yes
checking whether NLS is requested... yes
checking for msgfmt... no
checking for gmsgfmt... :
checking for xgettext... no
checking for msgmerge... no
checking for ld used by gcc... ld
checking if the linker (ld) is GNU ld... yes
checking for shared library run path origin... done
checking for CFPreferencesCopyAppValue... no
checking for CFLocaleCopyCurrent... no
checking for GNU gettext in libc... yes
checking whether to use NLS... yes
checking where the gettext function comes from... libc
checking that generated files are newer than configure... done
configure: creating ./config.status
config.status: creating Makefile
config.status: creating po/Makefile.in
config.status: creating config.h
config.status: executing depfiles commands
config.status: executing po-directories commands
config.status: creating po/POTFILES
config.status: creating po/Makefile
make[1]: вход в каталог «/run/user/1000/tmprp0m6vev/src»
rm -f lib/configmake.h-t && \
{ echo '/* DO NOT EDIT! GENERATED AUTOMATICALLY! */'; \
  echo '#define PREFIX "/usr"'; \
  echo '#define EXEC_PREFIX "/usr"'; \
  echo '#define BINDIR "/usr/bin"'; \
  echo '#define SBINDIR "/usr/sbin"'; \
  echo '#define LIBEXECDIR "/usr/libexec"'; \
  echo '#define DATAROOTDIR "/usr/share"'; \
  echo '#define DATADIR "/usr/share"'; \
  echo '#define SYSCONFDIR "/usr/etc"'; \
  echo '#define SHAREDSTATEDIR "/usr/com"'; \
  echo '#define LOCALSTATEDIR "/usr/var"'; \
  echo '#define RUNSTATEDIR "/usr/var/run"'; \
  echo '#define INCLUDEDIR "/usr/include"'; \
  echo '#define OLDINCLUDEDIR "/usr/include"'; \
  echo '#define DOCDIR "/usr/share/doc/hello"'; \
  echo '#define INFODIR "/usr/share/info"'; \
  echo '#define HTMLDIR "/usr/share/doc/hello"'; \
  echo '#define DVIDIR "/usr/share/doc/hello"'; \
  echo '#define PDFDIR "/usr/share/doc/hello"'; \
  echo '#define PSDIR "/usr/share/doc/hello"'; \
  echo '#define LIBDIR "/usr/lib"'; \
  echo '#define LISPDIR "/usr/share/emacs/site-lisp"'; \
  echo '#define LOCALEDIR "/usr/share/locale"'; \
  echo '#define MANDIR "/usr/share/man"'; \
  echo '#define MANEXT ""'; \
  echo '#define PKGDATADIR "/usr/share/hello"'; \
  echo '#define PKGINCLUDEDIR "/usr/include/hello"'; \
  echo '#define PKGLIBDIR "/usr/lib/hello"'; \
  echo '#define PKGLIBEXECDIR "/usr/libexec/hello"'; \
} | sed '/""/d' > lib/configmake.h-t && \
mv -f lib/configmake.h-t lib/configmake.h
rm -f lib/arg-nonnull.h-t lib/arg-nonnull.h && \
sed -n -e '/GL_ARG_NONNULL/,$p' \
  < ./build-aux/snippet/arg-nonnull.h \
  > lib/arg-nonnull.h-t && \
mv lib/arg-nonnull.h-t lib/arg-nonnull.h
rm -f lib/c++defs.h-t lib/c++defs.h && \
sed -n -e '/_GL_CXXDEFS/,$p' \
  < ./build-aux/snippet/c++defs.h \
  > lib/c++defs.h-t && \
mv lib/c++defs.h-t lib/c++defs.h
rm -f lib/warn-on-use.h-t lib/warn-on-use.h && \
sed -n -e '/^.ifndef/,$p' \
  < ./build-aux/snippet/warn-on-use.h \
  > lib/warn-on-use.h-t && \
mv lib/warn-on-use.h-t lib/warn-on-use.h
rm -f lib/stdio.h-t lib/stdio.h && \
{ echo '/* DO NOT EDIT! GENERATED AUTOMATICALLY! */' && \
  sed -e 's|@''GUARD_PREFIX''@|GL|g' \
      -e 's|@''INCLUDE_NEXT''@|include_next|g' \
      -e 's|@''PRAGMA_SYSTEM_HEADER''@|#pragma GCC system_header|g' \
      -e 's|@''PRAGMA_COLUMNS''@||g' \
      -e 's|@''NEXT_STDIO_H''@|<stdio.h>|g' \
      -e 's/@''GNULIB_DPRINTF''@/0/g' \
      -e 's/@''GNULIB_FCLOSE''@/0/g' \
      -e 's/@''GNULIB_FDOPEN''@/0/g' \
      -e 's/@''GNULIB_FFLUSH''@/0/g' \
      -e 's/@''GNULIB_FGETC''@/1/g' \
      -e 's/@''GNULIB_FGETS''@/1/g' \
      -e 's/@''GNULIB_FOPEN''@/0/g' \
      -e 's/@''GNULIB_FPRINTF''@/1/g' \
      -e 's/@''GNULIB_FPRINTF_POSIX''@/0/g' \
      -e 's/@''GNULIB_FPURGE''@/0/g' \
      -e 's/@''GNULIB_FPUTC''@/1/g' \
      -e 's/@''GNULIB_FPUTS''@/1/g' \
      -e 's/@''GNULIB_FREAD''@/1/g' \
      -e 's/@''GNULIB_FREOPEN''@/0/g' \
      -e 's/@''GNULIB_FSCANF''@/1/g' \
      -e 's/@''GNULIB_FSEEK''@/0/g' \
      -e 's/@''GNULIB_FSEEKO''@/0/g' \
      -e 's/@''GNULIB_FTELL''@/0/g' \
      -e 's/@''GNULIB_FTELLO''@/0/g' \
      -e 's/@''GNULIB_FWRITE''@/1/g' \
      -e 's/@''GNULIB_GETC''@/1/g' \
      -e 's/@''GNULIB_GETCHAR''@/1/g' \
      -e 's/@''GNULIB_GETDELIM''@/0/g' \
      -e 's/@''GNULIB_GETLINE''@/0/g' \
      -e 's/@''GNULIB_OBSTACK_PRINTF''@/0/g' \
      -e 's/@''GNULIB_OBSTACK_PRINTF_POSIX''@/0/g' \
      -e 's/@''GNULIB_PCLOSE''@/0/g' \
      -e 's/@''GNULIB_PERROR''@/0/g' \
      -e 's/@''GNULIB_POPEN''@/0/g' \
      -e 's/@''GNULIB_PRINTF''@/1/g' \
      -e 's/@''GNULIB_PRINTF_POSIX''@/0/g' \
      -e 's/@''GNULIB_PUTC''@/1/g' \
      -e 's/@''GNULIB_PUTCHAR''@/1/g' \
      -e 's/@''GNULIB_PUTS''@/1/g' \
      -e 's/@''GNULIB_REMOVE''@/0/g' \
      -e 's/@''GNULIB_RENAME''@/0/g' \
      -e 's/@''GNULIB_RENAMEAT''@/0/g' \
      -e 's/@''GNULIB_SCANF''@/1/g' \
      -e 's/@''GNULIB_SNPRINTF''@/0/g' \
      -e 's/@''GNULIB_SPRINTF_POSIX''@/0/g' \
      -e 's/@''GNULIB_STDIO_H_NONBLOCKING''@/0/g' \
      -e 's/@''GNULIB_STDIO_H_SIGPIPE''@/0/g' \
      -e 's/@''GNULIB_TMPFILE''@/0/g' \
      -e 's/@''GNULIB_VASPRINTF''@/0/g' \
      -e 's/@''GNULIB_VDPRINTF''@/0/g' \
      -e 's/@''GNULIB_VFPRINTF''@/1/g' \
      -e 's/@''GNULIB_VFPRINTF_POSIX''@/0/g' \
      -e 's/@''GNULIB_VFSCANF''@/0/g' \
      -e 's/@''GNULIB_VSCANF''@/0/g' \
      -e 's/@''GNULIB_VPRINTF''@/1/g' \
      -e 's/@''GNULIB_VPRINTF_POSIX''@/0/g' \
      -e 's/@''GNULIB_VSNPRINTF''@/0/g' \
      -e 's/@''GNULIB_VSPRINTF_POSIX''@/0/g' \
      < ./lib/stdio.in.h | \
  sed -e 's|@''HAVE_DECL_FPURGE''@|1|g' \
      -e 's|@''HAVE_DECL_FSEEKO''@|1|g' \
      -e 's|@''HAVE_DECL_FTELLO''@|1|g' \
      -e 's|@''HAVE_DECL_GETDELIM''@|1|g' \
      -e 's|@''HAVE_DECL_GETLINE''@|1|g' \
      -e 's|@''HAVE_DECL_OBSTACK_PRINTF''@|1|g' \
      -e 's|@''HAVE_DECL_SNPRINTF''@|1|g' \
      -e 's|@''HAVE_DECL_VSNPRINTF''@|1|g' \
      -e 's|@''HAVE_DPRINTF''@|1|g' \
      -e 's|@''HAVE_FSEEKO''@|1|g' \
      -e 's|@''HAVE_FTELLO''@|1|g' \
      -e 's|@''HAVE_PCLOSE''@|1|g' \
      -e 's|@''HAVE_POPEN''@|1|g' \
      -e 's|@''HAVE_RENAMEAT''@|1|g' \
      -e 's|@''HAVE_VASPRINTF''@|1|g' \
      -e 's|@''HAVE_VDPRINTF''@|1|g' \
      -e 's|@''REPLACE_DPRINTF''@|0|g' \
      -e 's|@''REPLACE_FCLOSE''@|0|g' \
      -e 's|@''REPLACE_FDOPEN''@|0|g' \
      -e 's|@''REPLACE_FFLUSH''@|0|g' \
      -e 's|@''REPLACE_FOPEN''@|0|g' \
      -e 's|@''REPLACE_FPRINTF''@|0|g' \
      -e 's|@''REPLACE_FPURGE''@|0|g' \
      -e 's|@''REPLACE_FREOPEN''@|0|g' \
      -e 's|@''REPLACE_FSEEK''@|0|g' \
      -e 's|@''REPLACE_FSEEKO''@|0|g' \
      -e 's|@''REPLACE_FTELL''@|0|g' \
      -e 's|@''REPLACE_FTELLO''@|0|g' \
      -e 's|@''REPLACE_GETDELIM''@|0|g' \
      -e 's|@''REPLACE_GETLINE''@|0|g' \
      -e 's|@''REPLACE_OBSTACK_PRINTF''@|0|g' \
      -e 's|@''REPLACE_PERROR''@|0|g' \
      -e 's|@''REPLACE_POPEN''@|0|g' \
      -e 's|@''REPLACE_PRINTF''@|0|g' \
      -e 's|@''REPLACE_REMOVE''@|0|g' \
      -e 's|@''REPLACE_RENAME''@|0|g' \
      -e 's|@''REPLACE_RENAMEAT''@|0|g' \
      -e 's|@''REPLACE_SNPRINTF''@|0|g' \
      -e 's|@''REPLACE_SPRINTF''@|0|g' \
      -e 's|@''REPLACE_STDIO_READ_FUNCS''@|0|g' \
      -e 's|@''REPLACE_STDIO_WRITE_FUNCS''@|0|g' \
      -e 's|@''REPLACE_TMPFILE''@|0|g' \
      -e 's|@''REPLACE_VASPRINTF''@|0|g' \
      -e 's|@''REPLACE_VDPRINTF''@|0|g' \
      -e 's|@''REPLACE_VFPRINTF''@|0|g' \
      -e 's|@''REPLACE_VPRINTF''@|0|g' \
      -e 's|@''REPLACE_VSNPRINTF''@|0|g' \
      -e 's|@''REPLACE_VSPRINTF''@|0|g' \
      -e 's|@''ASM_SYMBOL_PREFIX''@||g' \
      -e '/definitions of _GL_FUNCDECL_RPL/r lib/c++defs.h' \
      -e '/definition of _GL_ARG_NONNULL/r lib/arg-nonnull.h' \
      -e '/definition of _GL_WARN_ON_USE/r lib/warn-on-use.h'; \
} > lib/stdio.h-t && \
mv lib/stdio.h-t lib/stdio.h
rm -f lib/stdlib.h-t lib/stdlib.h && \
{ echo '/* DO NOT EDIT! GENERATED AUTOMATICALLY! */' && \
  sed -e 's|@''GUARD_PREFIX''@|GL|g' \
      -e 's|@''INCLUDE_NEXT''@|include_next|g' \
      -e 's|@''PRAGMA_SYSTEM_HEADER''@|#pragma GCC system_header|g' \
      -e 's|@''PRAGMA_COLUMNS''@||g' \
      -e 's|@''NEXT_STDLIB_H''@|<stdlib.h>|g' \
      -e 's/@''GNULIB__EXIT''@/0/g' \
      -e 's/@''GNULIB_ATOLL''@/0/g' \
      -e 's/@''GNULIB_CALLOC_POSIX''@/0/g' \
      -e 's/@''GNULIB_CANONICALIZE_FILE_NAME''@/0/g' \
      -e 's/@''GNULIB_GETLOADAVG''@/0/g' \
      -e 's/@''GNULIB_GETSUBOPT''@/0/g' \
      -e 's/@''GNULIB_GRANTPT''@/0/g' \
      -e 's/@''GNULIB_MALLOC_POSIX''@/1/g' \
      -e 's/@''GNULIB_MBTOWC''@/0/g' \
      -e 's/@''GNULIB_MKDTEMP''@/0/g' \
      -e 's/@''GNULIB_MKOSTEMP''@/0/g' \
      -e 's/@''GNULIB_MKOSTEMPS''@/0/g' \
      -e 's/@''GNULIB_MKSTEMP''@/0/g' \
      -e 's/@''GNULIB_MKSTEMPS''@/0/g' \
      -e 's/@''GNULIB_POSIX_OPENPT''@/0/g' \
      -e 's/@''GNULIB_PTSNAME''@/0/g' \
      -e 's/@''GNULIB_PTSNAME_R''@/0/g' \
      -e 's/@''GNULIB_PUTENV''@/0/g' \
      -e 's/@''GNULIB_QSORT_R''@/0/g' \
      -e 's/@''GNULIB_RANDOM''@/0/g' \
      -e 's/@''GNULIB_RANDOM_R''@/0/g' \
      -e 's/@''GNULIB_REALLOC_POSIX''@/0/g' \
      -e 's/@''GNULIB_REALPATH''@/0/g' \
      -e 's/@''GNULIB_RPMATCH''@/0/g' \
      -e 's/@''GNULIB_SECURE_GETENV''@/0/g' \
      -e 's/@''GNULIB_SETENV''@/0/g' \
      -e 's/@''GNULIB_STRTOD''@/0/g' \
      -e 's/@''GNULIB_STRTOLL''@/0/g' \
      -e 's/@''GNULIB_STRTOULL''@/0/g' \
      -e 's/@''GNULIB_SYSTEM_POSIX''@/0/g' \
      -e 's/@''GNULIB_UNLOCKPT''@/0/g' \
      -e 's/@''GNULIB_UNSETENV''@/0/g' \
      -e 's/@''GNULIB_WCTOMB''@/0/g' \
      < ./lib/stdlib.in.h | \
  sed -e 's|@''HAVE__EXIT''@|1|g' \
      -e 's|@''HAVE_ATOLL''@|1|g' \
      -e 's|@''HAVE_CANONICALIZE_FILE_NAME''@|1|g' \
      -e 's|@''HAVE_DECL_GETLOADAVG''@|1|g' \
      -e 's|@''HAVE_GETSUBOPT''@|1|g' \
      -e 's|@''HAVE_GRANTPT''@|1|g' \
      -e 's|@''HAVE_MKDTEMP''@|1|g' \
      -e 's|@''HAVE_MKOSTEMP''@|1|g' \
      -e 's|@''HAVE_MKOSTEMPS''@|1|g' \
      -e 's|@''HAVE_MKSTEMP''@|1|g' \
      -e 's|@''HAVE_MKSTEMPS''@|1|g' \
      -e 's|@''HAVE_POSIX_OPENPT''@|1|g' \
      -e 's|@''HAVE_PTSNAME''@|1|g' \
      -e 's|@''HAVE_PTSNAME_R''@|1|g' \
      -e 's|@''HAVE_RANDOM''@|1|g' \
      -e 's|@''HAVE_RANDOM_H''@|1|g' \
      -e 's|@''HAVE_RANDOM_R''@|1|g' \
      -e 's|@''HAVE_REALPATH''@|1|g' \
      -e 's|@''HAVE_RPMATCH''@|1|g' \
      -e 's|@''HAVE_SECURE_GETENV''@|1|g' \
      -e 's|@''HAVE_DECL_SETENV''@|1|g' \
      -e 's|@''HAVE_STRTOD''@|1|g' \
      -e 's|@''HAVE_STRTOLL''@|1|g' \
      -e 's|@''HAVE_STRTOULL''@|1|g' \
      -e 's|@''HAVE_STRUCT_RANDOM_DATA''@|1|g' \
      -e 's|@''HAVE_SYS_LOADAVG_H''@|0|g' \
      -e 's|@''HAVE_UNLOCKPT''@|1|g' \
      -e 's|@''HAVE_DECL_UNSETENV''@|1|g' \
      -e 's|@''REPLACE_CALLOC''@|0|g' \
      -e 's|@''REPLACE_CANONICALIZE_FILE_NAME''@|0|g' \
      -e 's|@''REPLACE_MALLOC''@|0|g' \
      -e 's|@''REPLACE_MBTOWC''@|0|g' \
      -e 's|@''REPLACE_MKSTEMP''@|0|g' \
      -e 's|@''REPLACE_PTSNAME''@|0|g' \
      -e 's|@''REPLACE_PTSNAME_R''@|0|g' \
      -e 's|@''REPLACE_PUTENV''@|0|g' \
      -e 's|@''REPLACE_QSORT_R''@|0|g' \
      -e 's|@''REPLACE_RANDOM_R''@|0|g' \
      -e 's|@''REPLACE_REALLOC''@|0|g' \
      -e 's|@''REPLACE_REALPATH''@|0|g' \
      -e 's|@''REPLACE_SETENV''@|0|g' \
      -e 's|@''REPLACE_STRTOD''@|0|g' \
      -e 's|@''REPLACE_UNSETENV''@|0|g' \
      -e 's|@''REPLACE_WCTOMB''@|0|g' \
      -e '/definitions of _GL_FUNCDECL_RPL/r lib/c++defs.h' \
      -e '/definition of _Noreturn/r ./build-aux/snippet/_Noreturn.h' \
      -e '/definition of _GL_ARG_NONNULL/r lib/arg-nonnull.h' \
      -e '/definition of _GL_WARN_ON_USE/r lib/warn-on-use.h'; \
} > lib/stdlib.h-t && \
mv lib/stdlib.h-t lib/stdlib.h
rm -f lib/string.h-t lib/string.h && \
{ echo '/* DO NOT EDIT! GENERATED AUTOMATICALLY! */' && \
  sed -e 's|@''GUARD_PREFIX''@|GL|g' \
      -e 's|@''INCLUDE_NEXT''@|include_next|g' \
      -e 's|@''PRAGMA_SYSTEM_HEADER''@|#pragma GCC system_header|g' \
      -e 's|@''PRAGMA_COLUMNS''@||g' \
      -e 's|@''NEXT_STRING_H''@|<string.h>|g' \
      -e 's/@''GNULIB_FFSL''@/0/g' \
      -e 's/@''GNULIB_FFSLL''@/0/g' \
      -e 's/@''GNULIB_MBSLEN''@/0/g' \
      -e 's/@''GNULIB_MBSNLEN''@/0/g' \
      -e 's/@''GNULIB_MBSCHR''@/0/g' \
      -e 's/@''GNULIB_MBSRCHR''@/0/g' \
      -e 's/@''GNULIB_MBSSTR''@/0/g' \
      -e 's/@''GNULIB_MBSCASECMP''@/0/g' \
      -e 's/@''GNULIB_MBSNCASECMP''@/0/g' \
      -e 's/@''GNULIB_MBSPCASECMP''@/0/g' \
      -e 's/@''GNULIB_MBSCASESTR''@/0/g' \
      -e 's/@''GNULIB_MBSCSPN''@/0/g' \
      -e 's/@''GNULIB_MBSPBRK''@/0/g' \
      -e 's/@''GNULIB_MBSSPN''@/0/g' \
      -e 's/@''GNULIB_MBSSEP''@/0/g' \
      -e 's/@''GNULIB_MBSTOK_R''@/0/g' \
      -e 's/@''GNULIB_MEMCHR''@/1/g' \
      -e 's/@''GNULIB_MEMMEM''@/0/g' \
      -e 's/@''GNULIB_MEMPCPY''@/0/g' \
      -e 's/@''GNULIB_MEMRCHR''@/0/g' \
      -e 's/@''GNULIB_RAWMEMCHR''@/0/g' \
      -e 's/@''GNULIB_STPCPY''@/0/g' \
      -e 's/@''GNULIB_STPNCPY''@/0/g' \
      -e 's/@''GNULIB_STRCHRNUL''@/0/g' \
      -e 's/@''GNULIB_STRDUP''@/0/g' \
      -e 's/@''GNULIB_STRNCAT''@/0/g' \
      -e 's/@''GNULIB_STRNDUP''@/1/g' \
      -e 's/@''GNULIB_STRNLEN''@/1/g' \
      -e 's/@''GNULIB_STRPBRK''@/0/g' \
      -e 's/@''GNULIB_STRSEP''@/0/g' \
      -e 's/@''GNULIB_STRSTR''@/0/g' \
      -e 's/@''GNULIB_STRCASESTR''@/0/g' \
      -e 's/@''GNULIB_STRTOK_R''@/0/g' \
      -e 's/@''GNULIB_STRERROR''@/1/g' \
      -e 's/@''GNULIB_STRERROR_R''@/0/g' \
      -e 's/@''GNULIB_STRSIGNAL''@/0/g' \
      -e 's/@''GNULIB_STRVERSCMP''@/0/g' \
      < ./lib/string.in.h | \
  sed -e 's|@''HAVE_FFSL''@|1|g' \
      -e 's|@''HAVE_FFSLL''@|1|g' \
      -e 's|@''HAVE_MBSLEN''@|0|g' \
      -e 's|@''HAVE_MEMCHR''@|1|g' \
      -e 's|@''HAVE_DECL_MEMMEM''@|1|g' \
      -e 's|@''HAVE_MEMPCPY''@|1|g' \
      -e 's|@''HAVE_DECL_MEMRCHR''@|1|g' \
      -e 's|@''HAVE_RAWMEMCHR''@|1|g' \
      -e 's|@''HAVE_STPCPY''@|1|g' \
      -e 's|@''HAVE_STPNCPY''@|1|g' \
      -e 's|@''HAVE_STRCHRNUL''@|1|g' \
      -e 's|@''HAVE_DECL_STRDUP''@|1|g' \
      -e 's|@''HAVE_DECL_STRNDUP''@|1|g' \
      -e 's|@''HAVE_DECL_STRNLEN''@|1|g' \
      -e 's|@''HAVE_STRPBRK''@|1|g' \
      -e 's|@''HAVE_STRSEP''@|1|g' \
      -e 's|@''HAVE_STRCASESTR''@|1|g' \
      -e 's|@''HAVE_DECL_STRTOK_R''@|1|g' \
      -e 's|@''HAVE_DECL_STRERROR_R''@|1|g' \
      -e 's|@''HAVE_DECL_STRSIGNAL''@|1|g' \
      -e 's|@''HAVE_STRVERSCMP''@|1|g' \
      -e 's|@''REPLACE_STPNCPY''@|0|g' \
      -e 's|@''REPLACE_MEMCHR''@|0|g' \
      -e 's|@''REPLACE_MEMMEM''@|0|g' \
      -e 's|@''REPLACE_STRCASESTR''@|0|g' \
      -e 's|@''REPLACE_STRCHRNUL''@|0|g' \
      -e 's|@''REPLACE_STRDUP''@|0|g' \
      -e 's|@''REPLACE_STRSTR''@|0|g' \
      -e 's|@''REPLACE_STRERROR''@|0|g' \
      -e 's|@''REPLACE_STRERROR_R''@|0|g' \
      -e 's|@''REPLACE_STRNCAT''@|0|g' \
      -e 's|@''REPLACE_STRNDUP''@|0|g' \
      -e 's|@''REPLACE_STRNLEN''@|0|g' \
      -e 's|@''REPLACE_STRSIGNAL''@|0|g' \
      -e 's|@''REPLACE_STRTOK_R''@|0|g' \
      -e 's|@''UNDEFINE_STRTOK_R''@|0|g' \
      -e '/definitions of _GL_FUNCDECL_RPL/r lib/c++defs.h' \
      -e '/definition of _GL_ARG_NONNULL/r lib/arg-nonnull.h' \
      -e '/definition of _GL_WARN_ON_USE/r lib/warn-on-use.h'; \
      < ./lib/string.in.h; \
} > lib/string.h-t && \
mv lib/string.h-t lib/string.h
/nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/mkdir -p lib/sys
rm -f lib/sys/types.h-t lib/sys/types.h && \
{ echo '/* DO NOT EDIT! GENERATED AUTOMATICALLY! */'; \
  sed -e 's|@''GUARD_PREFIX''@|GL|g' \
      -e 's|@''INCLUDE_NEXT''@|include_next|g' \
      -e 's|@''PRAGMA_SYSTEM_HEADER''@|#pragma GCC system_header|g' \
      -e 's|@''PRAGMA_COLUMNS''@||g' \
      -e 's|@''NEXT_SYS_TYPES_H''@|<sys/types.h>|g' \
      -e 's|@''WINDOWS_64_BIT_OFF_T''@|0|g' \
      < ./lib/sys_types.in.h; \
} > lib/sys/types.h-t && \
mv lib/sys/types.h-t lib/sys/types.h
rm -f lib/unistd.h-t lib/unistd.h && \
{ echo '/* DO NOT EDIT! GENERATED AUTOMATICALLY! */'; \
  sed -e 's|@''GUARD_PREFIX''@|GL|g' \
      -e 's|@''HAVE_UNISTD_H''@|1|g' \
      -e 's|@''INCLUDE_NEXT''@|include_next|g' \
      -e 's|@''PRAGMA_SYSTEM_HEADER''@|#pragma GCC system_header|g' \
      -e 's|@''PRAGMA_COLUMNS''@||g' \
      -e 's|@''NEXT_UNISTD_H''@|<unistd.h>|g' \
      -e 's|@''WINDOWS_64_BIT_OFF_T''@|0|g' \
      -e 's/@''GNULIB_CHDIR''@/0/g' \
      -e 's/@''GNULIB_CHOWN''@/0/g' \
      -e 's/@''GNULIB_CLOSE''@/0/g' \
      -e 's/@''GNULIB_DUP''@/0/g' \
      -e 's/@''GNULIB_DUP2''@/0/g' \
      -e 's/@''GNULIB_DUP3''@/0/g' \
      -e 's/@''GNULIB_ENVIRON''@/0/g' \
      -e 's/@''GNULIB_EUIDACCESS''@/0/g' \
      -e 's/@''GNULIB_FACCESSAT''@/0/g' \
      -e 's/@''GNULIB_FCHDIR''@/0/g' \
      -e 's/@''GNULIB_FCHOWNAT''@/0/g' \
      -e 's/@''GNULIB_FDATASYNC''@/0/g' \
      -e 's/@''GNULIB_FSYNC''@/0/g' \
      -e 's/@''GNULIB_FTRUNCATE''@/0/g' \
      -e 's/@''GNULIB_GETCWD''@/0/g' \
      -e 's/@''GNULIB_GETDOMAINNAME''@/0/g' \
      -e 's/@''GNULIB_GETDTABLESIZE''@/0/g' \
      -e 's/@''GNULIB_GETGROUPS''@/0/g' \
      -e 's/@''GNULIB_GETHOSTNAME''@/0/g' \
      -e 's/@''GNULIB_GETLOGIN''@/0/g' \
      -e 's/@''GNULIB_GETLOGIN_R''@/0/g' \
      -e 's/@''GNULIB_GETPAGESIZE''@/0/g' \
      -e 's/@''GNULIB_GETUSERSHELL''@/0/g' \
      -e 's/@''GNULIB_GROUP_MEMBER''@/0/g' \
      -e 's/@''GNULIB_ISATTY''@/0/g' \
      -e 's/@''GNULIB_LCHOWN''@/0/g' \
      -e 's/@''GNULIB_LINK''@/0/g' \
      -e 's/@''GNULIB_LINKAT''@/0/g' \
      -e 's/@''GNULIB_LSEEK''@/0/g' \
      -e 's/@''GNULIB_PIPE''@/0/g' \
      -e 's/@''GNULIB_PIPE2''@/0/g' \
      -e 's/@''GNULIB_PREAD''@/0/g' \
      -e 's/@''GNULIB_PWRITE''@/0/g' \
      -e 's/@''GNULIB_READ''@/0/g' \
      -e 's/@''GNULIB_READLINK''@/0/g' \
      -e 's/@''GNULIB_READLINKAT''@/0/g' \
      -e 's/@''GNULIB_RMDIR''@/0/g' \
      -e 's/@''GNULIB_SETHOSTNAME''@/0/g' \
      -e 's/@''GNULIB_SLEEP''@/0/g' \
      -e 's/@''GNULIB_SYMLINK''@/0/g' \
      -e 's/@''GNULIB_SYMLINKAT''@/0/g' \
      -e 's/@''GNULIB_TTYNAME_R''@/0/g' \
      -e 's/@''GNULIB_UNISTD_H_GETOPT''@/0/g' \
      -e 's/@''GNULIB_UNISTD_H_NONBLOCKING''@/0/g' \
      -e 's/@''GNULIB_UNISTD_H_SIGPIPE''@/0/g' \
      -e 's/@''GNULIB_UNLINK''@/0/g' \
      -e 's/@''GNULIB_UNLINKAT''@/0/g' \
      -e 's/@''GNULIB_USLEEP''@/0/g' \
      -e 's/@''GNULIB_WRITE''@/0/g' \
      < ./lib/unistd.in.h | \
  sed -e 's|@''HAVE_CHOWN''@|1|g' \
      -e 's|@''HAVE_DUP2''@|1|g' \
      -e 's|@''HAVE_DUP3''@|1|g' \
      -e 's|@''HAVE_EUIDACCESS''@|1|g' \
      -e 's|@''HAVE_FACCESSAT''@|1|g' \
      -e 's|@''HAVE_FCHDIR''@|1|g' \
      -e 's|@''HAVE_FCHOWNAT''@|1|g' \
      -e 's|@''HAVE_FDATASYNC''@|1|g' \
      -e 's|@''HAVE_FSYNC''@|1|g' \
      -e 's|@''HAVE_FTRUNCATE''@|1|g' \
      -e 's|@''HAVE_GETDTABLESIZE''@|1|g' \
      -e 's|@''HAVE_GETGROUPS''@|1|g' \
      -e 's|@''HAVE_GETHOSTNAME''@|1|g' \
      -e 's|@''HAVE_GETLOGIN''@|1|g' \
      -e 's|@''HAVE_GETPAGESIZE''@|1|g' \
      -e 's|@''HAVE_GROUP_MEMBER''@|1|g' \
      -e 's|@''HAVE_LCHOWN''@|1|g' \
      -e 's|@''HAVE_LINK''@|1|g' \
      -e 's|@''HAVE_LINKAT''@|1|g' \
      -e 's|@''HAVE_PIPE''@|1|g' \
      -e 's|@''HAVE_PIPE2''@|1|g' \
      -e 's|@''HAVE_PREAD''@|1|g' \
      -e 's|@''HAVE_PWRITE''@|1|g' \
      -e 's|@''HAVE_READLINK''@|1|g' \
      -e 's|@''HAVE_READLINKAT''@|1|g' \
      -e 's|@''HAVE_SETHOSTNAME''@|1|g' \
      -e 's|@''HAVE_SLEEP''@|1|g' \
      -e 's|@''HAVE_SYMLINK''@|1|g' \
      -e 's|@''HAVE_SYMLINKAT''@|1|g' \
      -e 's|@''HAVE_UNLINKAT''@|1|g' \
      -e 's|@''HAVE_USLEEP''@|1|g' \
      -e 's|@''HAVE_DECL_ENVIRON''@|1|g' \
      -e 's|@''HAVE_DECL_FCHDIR''@|1|g' \
      -e 's|@''HAVE_DECL_FDATASYNC''@|1|g' \
      -e 's|@''HAVE_DECL_GETDOMAINNAME''@|1|g' \
      -e 's|@''HAVE_DECL_GETLOGIN_R''@|1|g' \
      -e 's|@''HAVE_DECL_GETPAGESIZE''@|1|g' \
      -e 's|@''HAVE_DECL_GETUSERSHELL''@|1|g' \
      -e 's|@''HAVE_DECL_SETHOSTNAME''@|1|g' \
      -e 's|@''HAVE_DECL_TTYNAME_R''@|1|g' \
      -e 's|@''HAVE_OS_H''@|0|g' \
      -e 's|@''HAVE_SYS_PARAM_H''@|0|g' \
  | \
  sed -e 's|@''REPLACE_CHOWN''@|0|g' \
      -e 's|@''REPLACE_CLOSE''@|0|g' \
      -e 's|@''REPLACE_DUP''@|0|g' \
      -e 's|@''REPLACE_DUP2''@|0|g' \
      -e 's|@''REPLACE_FCHOWNAT''@|0|g' \
      -e 's|@''REPLACE_FTRUNCATE''@|0|g' \
      -e 's|@''REPLACE_GETCWD''@|0|g' \
      -e 's|@''REPLACE_GETDOMAINNAME''@|0|g' \
      -e 's|@''REPLACE_GETDTABLESIZE''@|0|g' \
      -e 's|@''REPLACE_GETLOGIN_R''@|0|g' \
      -e 's|@''REPLACE_GETGROUPS''@|0|g' \
      -e 's|@''REPLACE_GETPAGESIZE''@|0|g' \
      -e 's|@''REPLACE_ISATTY''@|0|g' \
      -e 's|@''REPLACE_LCHOWN''@|0|g' \
      -e 's|@''REPLACE_LINK''@|0|g' \
      -e 's|@''REPLACE_LINKAT''@|0|g' \
      -e 's|@''REPLACE_LSEEK''@|0|g' \
      -e 's|@''REPLACE_PREAD''@|0|g' \
      -e 's|@''REPLACE_PWRITE''@|0|g' \
      -e 's|@''REPLACE_READ''@|0|g' \
      -e 's|@''REPLACE_READLINK''@|0|g' \
      -e 's|@''REPLACE_READLINKAT''@|0|g' \
      -e 's|@''REPLACE_RMDIR''@|0|g' \
      -e 's|@''REPLACE_SLEEP''@|0|g' \
      -e 's|@''REPLACE_SYMLINK''@|0|g' \
      -e 's|@''REPLACE_SYMLINKAT''@|0|g' \
      -e 's|@''REPLACE_TTYNAME_R''@|0|g' \
      -e 's|@''REPLACE_UNLINK''@|0|g' \
      -e 's|@''REPLACE_UNLINKAT''@|0|g' \
      -e 's|@''REPLACE_USLEEP''@|0|g' \
      -e 's|@''REPLACE_WRITE''@|0|g' \
      -e 's|@''UNISTD_H_HAVE_WINSOCK2_H''@|0|g' \
      -e 's|@''UNISTD_H_HAVE_WINSOCK2_H_AND_USE_SOCKETS''@|0|g' \
      -e '/definitions of _GL_FUNCDECL_RPL/r lib/c++defs.h' \
      -e '/definition of _GL_ARG_NONNULL/r lib/arg-nonnull.h' \
      -e '/definition of _GL_WARN_ON_USE/r lib/warn-on-use.h'; \
} > lib/unistd.h-t && \
mv lib/unistd.h-t lib/unistd.h
rm -f lib/wchar.h-t lib/wchar.h && \
{ echo '/* DO NOT EDIT! GENERATED AUTOMATICALLY! */'; \
  sed -e 's|@''GUARD_PREFIX''@|GL|g' \
      -e 's|@''INCLUDE_NEXT''@|include_next|g' \
      -e 's|@''PRAGMA_SYSTEM_HEADER''@|#pragma GCC system_header|g' \
      -e 's|@''PRAGMA_COLUMNS''@||g' \
      -e 's|@''HAVE_FEATURES_H''@|1|g' \
      -e 's|@''NEXT_WCHAR_H''@|<wchar.h>|g' \
      -e 's|@''HAVE_WCHAR_H''@|1|g' \
      -e 's/@''GNULIB_BTOWC''@/0/g' \
      -e 's/@''GNULIB_WCTOB''@/0/g' \
      -e 's/@''GNULIB_MBSINIT''@/1/g' \
      -e 's/@''GNULIB_MBRTOWC''@/1/g' \
      -e 's/@''GNULIB_MBRLEN''@/0/g' \
      -e 's/@''GNULIB_MBSRTOWCS''@/1/g' \
      -e 's/@''GNULIB_MBSNRTOWCS''@/0/g' \
      -e 's/@''GNULIB_WCRTOMB''@/0/g' \
      -e 's/@''GNULIB_WCSRTOMBS''@/0/g' \
      -e 's/@''GNULIB_WCSNRTOMBS''@/0/g' \
      -e 's/@''GNULIB_WCWIDTH''@/0/g' \
      -e 's/@''GNULIB_WMEMCHR''@/0/g' \
      -e 's/@''GNULIB_WMEMCMP''@/0/g' \
      -e 's/@''GNULIB_WMEMCPY''@/0/g' \
      -e 's/@''GNULIB_WMEMMOVE''@/0/g' \
      -e 's/@''GNULIB_WMEMSET''@/0/g' \
      -e 's/@''GNULIB_WCSLEN''@/0/g' \
      -e 's/@''GNULIB_WCSNLEN''@/0/g' \
      -e 's/@''GNULIB_WCSCPY''@/0/g' \
      -e 's/@''GNULIB_WCPCPY''@/0/g' \
      -e 's/@''GNULIB_WCSNCPY''@/0/g' \
      -e 's/@''GNULIB_WCPNCPY''@/0/g' \
      -e 's/@''GNULIB_WCSCAT''@/0/g' \
      -e 's/@''GNULIB_WCSNCAT''@/0/g' \
      -e 's/@''GNULIB_WCSCMP''@/0/g' \
      -e 's/@''GNULIB_WCSNCMP''@/0/g' \
      -e 's/@''GNULIB_WCSCASECMP''@/0/g' \
      -e 's/@''GNULIB_WCSNCASECMP''@/0/g' \
      -e 's/@''GNULIB_WCSCOLL''@/0/g' \
      -e 's/@''GNULIB_WCSXFRM''@/0/g' \
      -e 's/@''GNULIB_WCSDUP''@/0/g' \
      -e 's/@''GNULIB_WCSCHR''@/0/g' \
      -e 's/@''GNULIB_WCSRCHR''@/0/g' \
      -e 's/@''GNULIB_WCSCSPN''@/0/g' \
      -e 's/@''GNULIB_WCSSPN''@/0/g' \
      -e 's/@''GNULIB_WCSPBRK''@/0/g' \
      -e 's/@''GNULIB_WCSSTR''@/0/g' \
      -e 's/@''GNULIB_WCSTOK''@/0/g' \
      -e 's/@''GNULIB_WCSWIDTH''@/0/g' \
      < ./lib/wchar.in.h | \
  sed -e 's|@''HAVE_WINT_T''@|1|g' \
      -e 's|@''HAVE_BTOWC''@|1|g' \
      -e 's|@''HAVE_MBSINIT''@|1|g' \
      -e 's|@''HAVE_MBRTOWC''@|1|g' \
      -e 's|@''HAVE_MBRLEN''@|1|g' \
      -e 's|@''HAVE_MBSRTOWCS''@|1|g' \
      -e 's|@''HAVE_MBSNRTOWCS''@|1|g' \
      -e 's|@''HAVE_WCRTOMB''@|1|g' \
      -e 's|@''HAVE_WCSRTOMBS''@|1|g' \
      -e 's|@''HAVE_WCSNRTOMBS''@|1|g' \
      -e 's|@''HAVE_WMEMCHR''@|1|g' \
      -e 's|@''HAVE_WMEMCMP''@|1|g' \
      -e 's|@''HAVE_WMEMCPY''@|1|g' \
      -e 's|@''HAVE_WMEMMOVE''@|1|g' \
      -e 's|@''HAVE_WMEMSET''@|1|g' \
      -e 's|@''HAVE_WCSLEN''@|1|g' \
      -e 's|@''HAVE_WCSNLEN''@|1|g' \
      -e 's|@''HAVE_WCSCPY''@|1|g' \
      -e 's|@''HAVE_WCPCPY''@|1|g' \
      -e 's|@''HAVE_WCSNCPY''@|1|g' \
      -e 's|@''HAVE_WCPNCPY''@|1|g' \
      -e 's|@''HAVE_WCSCAT''@|1|g' \
      -e 's|@''HAVE_WCSNCAT''@|1|g' \
      -e 's|@''HAVE_WCSCMP''@|1|g' \
      -e 's|@''HAVE_WCSNCMP''@|1|g' \
      -e 's|@''HAVE_WCSCASECMP''@|1|g' \
      -e 's|@''HAVE_WCSNCASECMP''@|1|g' \
      -e 's|@''HAVE_WCSCOLL''@|1|g' \
      -e 's|@''HAVE_WCSXFRM''@|1|g' \
      -e 's|@''HAVE_WCSDUP''@|1|g' \
      -e 's|@''HAVE_WCSCHR''@|1|g' \
      -e 's|@''HAVE_WCSRCHR''@|1|g' \
      -e 's|@''HAVE_WCSCSPN''@|1|g' \
      -e 's|@''HAVE_WCSSPN''@|1|g' \
      -e 's|@''HAVE_WCSPBRK''@|1|g' \
      -e 's|@''HAVE_WCSSTR''@|1|g' \
      -e 's|@''HAVE_WCSTOK''@|1|g' \
      -e 's|@''HAVE_WCSWIDTH''@|1|g' \
      -e 's|@''HAVE_DECL_WCTOB''@|1|g' \
      -e 's|@''HAVE_DECL_WCWIDTH''@|1|g' \
  | \
  sed -e 's|@''REPLACE_MBSTATE_T''@|0|g' \
      -e 's|@''REPLACE_BTOWC''@|0|g' \
      -e 's|@''REPLACE_WCTOB''@|0|g' \
      -e 's|@''REPLACE_MBSINIT''@|0|g' \
      -e 's|@''REPLACE_MBRTOWC''@|0|g' \
      -e 's|@''REPLACE_MBRLEN''@|0|g' \
      -e 's|@''REPLACE_MBSRTOWCS''@|0|g' \
      -e 's|@''REPLACE_MBSNRTOWCS''@|0|g' \
      -e 's|@''REPLACE_WCRTOMB''@|0|g' \
      -e 's|@''REPLACE_WCSRTOMBS''@|0|g' \
      -e 's|@''REPLACE_WCSNRTOMBS''@|0|g' \
      -e 's|@''REPLACE_WCWIDTH''@|0|g' \
      -e 's|@''REPLACE_WCSWIDTH''@|0|g' \
      -e '/definitions of _GL_FUNCDECL_RPL/r lib/c++defs.h' \
      -e '/definition of _GL_ARG_NONNULL/r lib/arg-nonnull.h' \
      -e '/definition of _GL_WARN_ON_USE/r lib/warn-on-use.h'; \
} > lib/wchar.h-t && \
mv lib/wchar.h-t lib/wchar.h
rm -f lib/wctype.h-t lib/wctype.h && \
{ echo '/* DO NOT EDIT! GENERATED AUTOMATICALLY! */'; \
  sed -e 's|@''GUARD_PREFIX''@|GL|g' \
      -e 's/@''HAVE_WCTYPE_H''@/1/g' \
      -e 's|@''INCLUDE_NEXT''@|include_next|g' \
      -e 's|@''PRAGMA_SYSTEM_HEADER''@|#pragma GCC system_header|g' \
      -e 's|@''PRAGMA_COLUMNS''@||g' \
      -e 's|@''NEXT_WCTYPE_H''@|<wctype.h>|g' \
      -e 's/@''GNULIB_ISWBLANK''@/0/g' \
      -e 's/@''GNULIB_WCTYPE''@/0/g' \
      -e 's/@''GNULIB_ISWCTYPE''@/0/g' \
      -e 's/@''GNULIB_WCTRANS''@/0/g' \
      -e 's/@''GNULIB_TOWCTRANS''@/0/g' \
      -e 's/@''HAVE_ISWBLANK''@/1/g' \
      -e 's/@''HAVE_ISWCNTRL''@/1/g' \
      -e 's/@''HAVE_WCTYPE_T''@/1/g' \
      -e 's/@''HAVE_WCTRANS_T''@/1/g' \
      -e 's/@''HAVE_WINT_T''@/1/g' \
      -e 's/@''REPLACE_ISWBLANK''@/0/g' \
      -e 's/@''REPLACE_ISWCNTRL''@/0/g' \
      -e 's/@''REPLACE_TOWLOWER''@/0/g' \
      -e '/definitions of _GL_FUNCDECL_RPL/r lib/c++defs.h' \
      -e '/definition of _GL_WARN_ON_USE/r lib/warn-on-use.h' \
      < ./lib/wctype.in.h; \
} > lib/wctype.h-t && \
mv lib/wctype.h-t lib/wctype.h
make  all-recursive
make[2]: Entering directory '/run/user/1000/tmprp0m6vev/src'
Making all in po
make[3]: Entering directory '/run/user/1000/tmprp0m6vev/src/po'
make[3]: Nothing to be done for 'all'.
make[3]: Leaving directory '/run/user/1000/tmprp0m6vev/src/po'
make[3]: Entering directory '/run/user/1000/tmprp0m6vev/src'
depbase=`echo lib/c-ctype.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/c-ctype.o -MD -MP -MF $depbase.Tpo -c -o lib/c-ctype.o lib/c-ctype.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/c-strcasecmp.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/c-strcasecmp.o -MD -MP -MF $depbase.Tpo -c -o lib/c-strcasecmp.o lib/c-strcasecmp.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/c-strncasecmp.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/c-strncasecmp.o -MD -MP -MF $depbase.Tpo -c -o lib/c-strncasecmp.o lib/c-strncasecmp.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/close-stream.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/close-stream.o -MD -MP -MF $depbase.Tpo -c -o lib/close-stream.o lib/close-stream.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/closeout.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/closeout.o -MD -MP -MF $depbase.Tpo -c -o lib/closeout.o lib/closeout.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/dirname.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/dirname.o -MD -MP -MF $depbase.Tpo -c -o lib/dirname.o lib/dirname.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/basename.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/basename.o -MD -MP -MF $depbase.Tpo -c -o lib/basename.o lib/basename.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/dirname-lgpl.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/dirname-lgpl.o -MD -MP -MF $depbase.Tpo -c -o lib/dirname-lgpl.o lib/dirname-lgpl.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/basename-lgpl.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/basename-lgpl.o -MD -MP -MF $depbase.Tpo -c -o lib/basename-lgpl.o lib/basename-lgpl.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/stripslash.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/stripslash.o -MD -MP -MF $depbase.Tpo -c -o lib/stripslash.o lib/stripslash.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/exitfail.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/exitfail.o -MD -MP -MF $depbase.Tpo -c -o lib/exitfail.o lib/exitfail.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/localcharset.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/localcharset.o -MD -MP -MF $depbase.Tpo -c -o lib/localcharset.o lib/localcharset.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/progname.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/progname.o -MD -MP -MF $depbase.Tpo -c -o lib/progname.o lib/progname.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/quotearg.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/quotearg.o -MD -MP -MF $depbase.Tpo -c -o lib/quotearg.o lib/quotearg.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/strnlen1.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/strnlen1.o -MD -MP -MF $depbase.Tpo -c -o lib/strnlen1.o lib/strnlen1.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/unistd.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/unistd.o -MD -MP -MF $depbase.Tpo -c -o lib/unistd.o lib/unistd.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/wctype-h.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/wctype-h.o -MD -MP -MF $depbase.Tpo -c -o lib/wctype-h.o lib/wctype-h.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/xmalloc.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/xmalloc.o -MD -MP -MF $depbase.Tpo -c -o lib/xmalloc.o lib/xmalloc.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/xalloc-die.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/xalloc-die.o -MD -MP -MF $depbase.Tpo -c -o lib/xalloc-die.o lib/xalloc-die.c &&\
mv -f $depbase.Tpo $depbase.Po
depbase=`echo lib/xstrndup.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT lib/xstrndup.o -MD -MP -MF $depbase.Tpo -c -o lib/xstrndup.o lib/xstrndup.c &&\
mv -f $depbase.Tpo $depbase.Po
rm -f lib/libhello.a
ar cru lib/libhello.a lib/c-ctype.o lib/c-strcasecmp.o lib/c-strncasecmp.o lib/close-stream.o lib/closeout.o lib/dirname.o lib/basename.o lib/dirname-lgpl.o lib/basename-lgpl.o lib/stripslash.o lib/exitfail.o lib/localcharset.o lib/progname.o lib/quotearg.o lib/strnlen1.o lib/unistd.o lib/wctype-h.o lib/xmalloc.o lib/xalloc-die.o lib/xstrndup.o 
ranlib lib/libhello.a
depbase=`echo src/hello.o | sed 's|[^/]*$|.deps/&|;s|\.o$||'`;\
gcc -DLOCALEDIR=\"/usr/share/locale\" -DHAVE_CONFIG_H -I.  -Ilib -I./lib -Isrc -I./src   -g -O2 -MT src/hello.o -MD -MP -MF $depbase.Tpo -c -o src/hello.o src/hello.c &&\
mv -f $depbase.Tpo $depbase.Po
gcc  -g -O2   -o hello src/hello.o  ./lib/libhello.a 
rm -f lib/charset.alias-t lib/charset.alias && \
/nix/store/hrpvwkjz04s9i4nmli843hyw9z4pwhww-bash-4.4-p23/bin/bash ./lib/config.charset 'x86_64-unknown-linux-gnu' > lib/charset.alias-t && \
mv lib/charset.alias-t lib/charset.alias
rm -f lib/ref-add.sed-t lib/ref-add.sed && \
sed -e '/^#/d' -e 's/@''PACKAGE''@/hello/g' lib/ref-add.sin > lib/ref-add.sed-t && \
mv lib/ref-add.sed-t lib/ref-add.sed
rm -f lib/ref-del.sed-t lib/ref-del.sed && \
sed -e '/^#/d' -e 's/@''PACKAGE''@/hello/g' lib/ref-del.sin > lib/ref-del.sed-t && \
mv lib/ref-del.sed-t lib/ref-del.sed
make[3]: Leaving directory '/run/user/1000/tmprp0m6vev/src'
make[2]: Leaving directory '/run/user/1000/tmprp0m6vev/src'
make[1]: выход из каталога «/run/user/1000/tmprp0m6vev/src»
make[1]: вход в каталог «/run/user/1000/tmprp0m6vev/src»
make  install-recursive
make[2]: Entering directory '/run/user/1000/tmprp0m6vev/src'
Making install in po
make[3]: Entering directory '/run/user/1000/tmprp0m6vev/src/po'
installing bg.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/bg/LC_MESSAGES/hello.mo
installing ca.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/ca/LC_MESSAGES/hello.mo
installing da.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/da/LC_MESSAGES/hello.mo
installing de.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/de/LC_MESSAGES/hello.mo
installing el.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/el/LC_MESSAGES/hello.mo
installing eo.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/eo/LC_MESSAGES/hello.mo
installing es.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/es/LC_MESSAGES/hello.mo
installing et.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/et/LC_MESSAGES/hello.mo
installing eu.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/eu/LC_MESSAGES/hello.mo
installing fa.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/fa/LC_MESSAGES/hello.mo
installing fi.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/fi/LC_MESSAGES/hello.mo
installing fr.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/fr/LC_MESSAGES/hello.mo
installing ga.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/ga/LC_MESSAGES/hello.mo
installing gl.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/gl/LC_MESSAGES/hello.mo
installing he.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/he/LC_MESSAGES/hello.mo
installing hr.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/hr/LC_MESSAGES/hello.mo
installing hu.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/hu/LC_MESSAGES/hello.mo
installing id.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/id/LC_MESSAGES/hello.mo
installing it.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/it/LC_MESSAGES/hello.mo
installing ja.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/ja/LC_MESSAGES/hello.mo
installing ka.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/ka/LC_MESSAGES/hello.mo
installing ko.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/ko/LC_MESSAGES/hello.mo
installing lv.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/lv/LC_MESSAGES/hello.mo
installing ms.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/ms/LC_MESSAGES/hello.mo
installing nb.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/nb/LC_MESSAGES/hello.mo
installing nl.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/nl/LC_MESSAGES/hello.mo
installing nn.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/nn/LC_MESSAGES/hello.mo
installing pl.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/pl/LC_MESSAGES/hello.mo
installing pt.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/pt/LC_MESSAGES/hello.mo
installing pt_BR.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/pt_BR/LC_MESSAGES/hello.mo
installing ro.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/ro/LC_MESSAGES/hello.mo
installing ru.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/ru/LC_MESSAGES/hello.mo
installing sk.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/sk/LC_MESSAGES/hello.mo
installing sl.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/sl/LC_MESSAGES/hello.mo
installing sr.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/sr/LC_MESSAGES/hello.mo
installing sv.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/sv/LC_MESSAGES/hello.mo
installing th.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/th/LC_MESSAGES/hello.mo
installing tr.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/tr/LC_MESSAGES/hello.mo
installing uk.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/uk/LC_MESSAGES/hello.mo
installing vi.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/vi/LC_MESSAGES/hello.mo
installing zh_CN.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/zh_CN/LC_MESSAGES/hello.mo
installing zh_TW.gmo as /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/locale/zh_TW/LC_MESSAGES/hello.mo
if test "hello" = "gettext-tools"; then \
  /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/mkdir -p /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/gettext/po; \
  for file in Makefile.in.in remove-potcdate.sin quot.sed boldquot.sed en@quot.header en@boldquot.header insert-header.sin Rules-quot   Makevars.template; do \
    /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/install -c -m 644 ./$file \
            /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/gettext/po/$file; \
  done; \
  for file in Makevars; do \
    rm -f /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/gettext/po/$file; \
  done; \
else \
  : ; \
fi
make[3]: Leaving directory '/run/user/1000/tmprp0m6vev/src/po'
make[3]: Entering directory '/run/user/1000/tmprp0m6vev/src'
make[4]: Entering directory '/run/user/1000/tmprp0m6vev/src'
 /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/mkdir -p '/tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/bin'
  /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/install -c hello '/tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/bin'
if test yes = no; then \
  case 'linux-gnu' in \
    darwin[56]*) \
      need_charset_alias=true ;; \
    darwin* | cygwin* | mingw* | pw32* | cegcc*) \
      need_charset_alias=false ;; \
    *) \
      need_charset_alias=true ;; \
  esac ; \
else \
  need_charset_alias=false ; \
fi ; \
if $need_charset_alias; then \
  /nix/store/hrpvwkjz04s9i4nmli843hyw9z4pwhww-bash-4.4-p23/bin/bash /run/user/1000/tmprp0m6vev/src/build-aux/install-sh -d /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/lib ; \
fi ; \
if test -f /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/lib/charset.alias; then \
  sed -f lib/ref-add.sed /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/lib/charset.alias > /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/lib/charset.tmp ; \
  /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/install -c -m 644 /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/lib/charset.tmp /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/lib/charset.alias ; \
  rm -f /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/lib/charset.tmp ; \
else \
  if $need_charset_alias; then \
    sed -f lib/ref-add.sed lib/charset.alias > /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/lib/charset.tmp ; \
    /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/install -c -m 644 /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/lib/charset.tmp /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/lib/charset.alias ; \
    rm -f /tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/lib/charset.tmp ; \
  fi ; \
fi
 /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/mkdir -p '/tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/info'
 /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/install -c -m 644 ./doc/hello.info '/tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/info'
 install-info --info-dir='/tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/info' '/tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/info/hello.info'
 /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/mkdir -p '/tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/man/man1'
 /nix/store/x0jla3hpxrwz76hy9yckg1iyc9hns81k-coreutils-8.31/bin/install -c -m 644 hello.1 '/tmp/pylightnix_hello_demo/tmp/210825-02:21:24:021813+0300_b2a453f8_v2pzuxi2/usr/share/man/man1'
make[4]: Leaving directory '/run/user/1000/tmprp0m6vev/src'
make[3]: Leaving directory '/run/user/1000/tmprp0m6vev/src'
make[2]: Leaving directory '/run/user/1000/tmprp0m6vev/src'
make[1]: выход из каталога «/run/user/1000/tmprp0m6vev/src»
rref:59314967adafce14db967cd3029d0851-b2a453f8cef994367d10b903236d06ef-hello-bin
```

``` stderr
ar: `u' modifier ignored since `D' is the default (see `U')
```

Now we could convert RRef to the system path and run the GNU Hello
binary.

``` python
hello_bin=join(rref2path(rref),'usr/bin/hello')
print(Popen([hello_bin], stdout=PIPE, shell=True).stdout.read()) # type:ignore
```

``` stdout
b'Hello, world!\n'
```
