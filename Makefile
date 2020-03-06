.DEFAULT_GOAL = all
VERSION = $(shell cat setup.py | sed -n 's/.*version="\(.*\)".*/\1/p')
WHEEL = dist/pylightnix-$(VERSION)-py3-none-any.whl
SRC = $(shell find src -name '*\.py')
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

.PHONY: check
check: .stamp_check

./docs/Reference.md: $(SRC) .stamp_check
	pydoc-markdown \
		--modules \
			pylightnix.types pylightnix.core pylightnix.inplace \
			pylightnix.repl pylightnix.stages pylightnix.bashlike \
			pylightnix.lens \
		--search-path  \
			src /usr/lib/python3.6/ > $@

.PHONY: docs
docs: ./docs/Reference.md

.coverage.xml: $(SRC) $(TESTS) .stamp_check
	rm coverage.xml || true
	coverage run -m pytest
	coverage xml -o $@
	touch $@

.PHONY: coverage
coverage: .coverage.xml
	coverage report -m

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

.PHONY: codecov
codecov: .stamp_codecov

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

docs/demos/REPL.md: docs/demos/REPL.pmd $(SRC) .stamp_check
	pweave -f markdown $<
	! cat $@ | grep -i traceback | tail -n +2 | grep -i traceback

docs/demos/REPL.py: docs/demos/REPL.pmd $(SRC) .stamp_check
	ptangle $<

.PHONY: demo_repl
demo_repl: docs/demos/REPL.md docs/demos/REPL.py

.PHONY: demos
demos: demo_mnist demo_hello demo_repl

$(WHEEL): $(SRC) $(TESTS)
	rm -rf build dist || true
	python3 setup.py sdist bdist_wheel
	test -f $@

.PHONY: wheels
wheels: $(WHEEL)
	@echo "To install, run \n> sudo pip3 install --force $@"

.PHONY: all
all: wheels coverage demos docs



