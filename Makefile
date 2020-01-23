
SRC = $(shell find src -name '*\.py')
TESTS = $(shell find tests -name '*\.py')

.stamp_check: $(SRC) $(TESTS) docs/demos/MNIST.pmd
	if ! which pydoc-markdown >/dev/null 2>&1 ; then \
		echo "pydoc-markdown not found. Please install it with"; \
		echo "> sudo -H pip3 install git+https://github.com/stagedml/pydoc-markdown.git@develop" ;\
		exit 1 ;\
	fi
	if ! which pweave >/dev/null 2>&1 ; then \
		echo "pweave not found. Please install it with" ; \
		echo "> sudo -H pip3 install pweave" ; \
		exit 1 ; \
	fi
	if ! test -f '.codecovrc' ; then \
		echo "Need .codecovrc file containing a codecov token." ;\
		echo "Go and get it at https://codecov.io/gh/stagedml/pylightnix/settings" >&2 ;\
		exit 1 ;\
	fi
	if ! which coverage >/dev/null ; then \
		echo "coverage not found. Install it with 'sudo -H pip3 install coverage'" ;\
		exit 1 ;\
	fi
	if ! which codecov >/dev/null ; then \
		echo "codecov not found. Install it with 'sudo -H pip3 install codecov'" ;\
		exit 1 ;\
	fi
	touch $@

.PHONY: check
check: .stamp_check

./docs/Reference.md: $(SRC) .stamp_check
	pydoc-markdown \
		--modules \
			pylightnix.types pylightnix.core pylightnix.stages \
		--search-path  \
			src /usr/lib/python3.6/ > $@

.PHONY: docs
docs: ./docs/Reference.md

.stamp_coverage: $(SRC) $(TESTS) .stamp_check
	rm coverage.xml || true
	coverage run -m pytest
	coverage report -m
	codecov -t `cat .codecovrc`
	touch $@

.PHONY: coverage
coverage: .stamp_coverage

docs/demos/MNIST.md: docs/demos/MNIST.pmd .stamp_check
	pweave -f markdown $<

docs/demos/MNIST.py: docs/demos/MNIST.pmd .stamp_check
	ptangle $<

.PHONY: demos
demos: docs/demos/MNIST.md docs/demos/MNIST.py

all:
	echo 'all'



