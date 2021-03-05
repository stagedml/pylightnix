.DEFAULT_GOAL = all
VERSION = $(shell python3 setup.py --version)
WHEEL = dist/pylightnix-$(VERSION)-py3-none-any.whl
SRC = $(shell find src -name '*\.py')
TEX = $(shell find docs -name '*\.tex')
TESTS = $(shell find tests -name '*\.py')

.stamp_check: $(SRC) $(TESTS) docs/demos/MNIST.pmd
	@if ! which pydoc-markdown >/dev/null 2>&1 ; then \
		echo "pydoc-markdown not found. Please install it with"; \
		echo "> sudo -H pip3 install git+https://github.com/stagedml/pydoc-markdown.git@develop" ;\
		exit 1 ;\
	fi
	@if ! which pweave >/dev/null 2>&1 ; then \
		echo "pweave not found. Please install it with" ; \
		echo "> sudo -H pip3 install pweave" ; \
		exit 1 ; \
	fi
	@if ! which coverage >/dev/null ; then \
		echo "coverage not found. Install it with 'sudo -H pip3 install coverage'" ;\
		exit 1 ;\
	fi
	touch $@

./docs/Reference.md: $(SRC) .stamp_check
	pydoc-markdown \
		--modules \
			pylightnix.types pylightnix.core pylightnix.build \
			pylightnix.inplace pylightnix.repl pylightnix.stages \
			pylightnix.bashlike pylightnix.lens pylightnix.either \
		--search-path \
			$(shell python3 -c "import sys; print(' '.join(sys.path))") >$@  # "

.PHONY: docs-reference
docs-reference: ./docs/Reference.md

.PHONY: docs-quickstart
docs-quickstart: docs/QuickStart.pdf
docs/QuickStart.pdf: $(SRC) $(TEX) ./docs/compile.sh .stamp_check
	/bin/sh ./docs/compile.sh docs/QuickStart.tex

.PHONY: docs-manual
docs-manual: docs/Manual.pdf
docs/Manual.pdf: $(SRC) $(TEX) ./docs/compile.sh .stamp_check
	/bin/sh ./docs/compile.sh docs/Manual.tex

.PHONY: publish-quickstart
publish-quickstart: docs/QuickStart.pdf
	/bin/sh ./docs/publish.sh docs/QuickStart.pdf $(VERSION)

.PHONY: publish-manual
publish-manual: docs/Manual.pdf
	/bin/sh ./docs/publish.sh docs/Manual.pdf $(VERSION)


.coverage.xml: $(SRC) $(TESTS) .stamp_check
	rm coverage.xml || true
	coverage run -m pytest
	coverage xml -o $@
	touch $@

.PHONY: typecheck tc
typecheck:
	pytest --mypy -m mypy
tc: typecheck

.PHONY: coverage test
coverage: .coverage.xml
	coverage report -m
test: coverage

.stamp_codecov: .coverage.xml .stamp_check .codecovrc
	@if ! which codecov >/dev/null ; then \
		echo "codecov not found. Install it with 'sudo -H pip3 install codecov'" ;\
		exit 1 ;\
	fi
	@if ! test -f '.codecovrc' ; then \
		echo "Need .codecovrc file containing a codecov token." ;\
		echo "Go and get it at https://codecov.io/gh/stagedml/pylightnix/settings" >&2 ;\
		exit 1 ;\
	fi
	codecov -t `cat .codecovrc` -f $<
	touch $@

.PHONY: coverage-upload
coverage-upload: .stamp_codecov

docs/demos/MNIST.md: docs/demos/MNIST.pmd $(SRC) .stamp_check
	pweave -f markdown $<
	! grep -i traceback $@

docs/demos/MNIST.py: docs/demos/MNIST.pmd $(SRC) .stamp_check
	ptangle $<

.PHONY: demo_mnist
demo_mnist: docs/demos/MNIST.md docs/demos/MNIST.py

docs/demos/HELLO.md: docs/demos/HELLO.pmd $(SRC) .stamp_check
	pweave -f markdown $<
	! grep -i traceback $@

docs/demos/HELLO.py: docs/demos/HELLO.pmd $(SRC) .stamp_check
	ptangle $<

.PHONY: demo_hello
demo_hello: docs/demos/HELLO.md docs/demos/HELLO.py

docs/demos/REPL.md: docs/demos/REPL.pmd $(SRC) .stamp_check_$(HOSTNAME)
	pweave -f markdown $<
	! cat $@ | grep -i traceback | tail -n +2 | grep -i traceback

docs/demos/REPL.py: docs/demos/REPL.pmd $(SRC) .stamp_check_$(HOSTNAME)
	ptangle $<

.PHONY: demo_repl
demo_repl: docs/demos/REPL.md docs/demos/REPL.py

.PHONY: demos
demos: demo_mnist demo_hello demo_repl

$(WHEEL): $(SRC) $(TESTS)
	rm -rf build dist || true
	python3 setup.py sdist bdist_wheel
	test -f $@

.PHONY: wheel
wheel: $(WHEEL)
	@echo "To install, run \`sudo -H make install\`"

.PHONY: version
version:
	@echo $(VERSION)

.PHONY: install
install: # To be run by root
	test "$(shell whoami)" = "root"
	test -f $(WHEEL) || ( echo 'run `make wheels` first'; exit 1; )
	pip3 install --force $(WHEEL)
	pip3 hash $(WHEEL) > .stamp_installhash_$(HOSTNAME)

.PHONY: check
check: $(WHEEL)
	pip3 hash $(WHEEL) > .stamp_piphash_$(HOSTNAME)
	@diff -u .stamp_piphash_$(HOSTNAME) .stamp_installhash_$(HOSTNAME) || ( \
		echo 'Did you install pylightnix systemwide by running `sudo -H make install` ?' ; exit 1 ; )

.PHONY: all
all: wheels coverage demos docs



