.DEFAULT_GOAL = all
VERSION = $(shell python3 setup.py --version)
WHEEL = dist/pylightnix-$(VERSION)-py3-none-any.whl
SRC = $(shell find src -name '*\.py' | grep -v version.py)
TEX = $(shell find docs -name '*\.tex')
TESTS = $(shell find tests -name '*\.py')

.stamp_check: $(SRC) $(TESTS)
	# @if ! which pydoc-markdown >/dev/null 2>&1 ; then \
	# 	echo "pydoc-markdown not found. Please install it with"; \
	# 	echo "> sudo -H pip3 install git+https://github.com/stagedml/pydoc-markdown.git@develop" ;\
	# 	exit 1 ;\
	# fi
	@if ! which coverage >/dev/null ; then \
		echo "coverage not found. Install it with 'sudo -H pip3 install coverage'" ;\
		exit 1 ;\
	fi
	touch $@

.stamp_check_codecovrc:
	@if ! test -f '_codecovrc' ; then \
		echo "The '_codecovrc' file must contain a codecov token." ;\
		echo "Go and get it at https://codecov.io/gh/stagedml/pylightnix/settings" >&2 ;\
		exit 1 ;\
	fi
	touch $@

./docs/Reference.md: $(SRC) .stamp_check Makefile
	pydoc-markdown \
		--modules \
			pylightnix.types pylightnix.core pylightnix.build \
			pylightnix.repl pylightnix.stages pylightnix.bashlike pylightnix.lens \
			pylightnix.either pylightnix.arch pylightnix.deco \
		--search-path \
			$(shell python3 -c "import sys; print(' '.join(sys.path))") >$@  # "

.PHONY: docs_readme
docs_readme: README.md
README.md: README.md.in Makefile
	codebraid pandoc \
		-f markdown -t markdown --no-cache --overwrite --standalone \
		--self-contained --to=markdown-smart-simple_tables-multiline_tables-grid_tables-fenced_code_attributes-inline_code_attributes-raw_attribute-pandoc_title_block-yaml_metadata_block -o $@ $< 2>&1 | tee _codebraid.log
	! grep Traceback _codebraid.log
	# pandoc -f markdown \
	# 	--to=markdown-smart-simple_tables-multiline_tables-grid_tables-fenced_code_attributes-inline_code_attributes-raw_attribute-pandoc_title_block-yaml_metadata_block \
	# 	--toc -s _tmp.md -o $@

.PHONY: docs_reference dr
docs_reference: ./docs/Reference.md
dr: docs_reference

.PHONY: docs_quickstart
docs_quickstart: docs/QuickStart.pdf
docs/QuickStart.pdf: $(SRC) $(TEX) ./docs/compile.sh .stamp_check
	/bin/sh ./docs/compile.sh docs/QuickStart.tex

.PHONY: docs_manual
docs_manual: docs/Manual.pdf
docs/Manual.pdf: $(SRC) $(TEX) ./docs/compile.sh .stamp_check
	/bin/sh ./docs/compile.sh docs/Manual.tex

.PHONY: docs
docs: docs_readme docs_manual docs_quickstart # docs_reference


.PHONY: publish-quickstart
publish-quickstart: docs/QuickStart.pdf
	/bin/sh ./docs/publish.sh docs/QuickStart.pdf $(VERSION)

.PHONY: publish-manual
publish-manual: docs/Manual.pdf
	/bin/sh ./docs/publish.sh docs/Manual.pdf $(VERSION)

.PHONY: publish-docs
publish-docs: publish-manual publish-quickstart

_coverage.xml: $(SRC) $(TESTS) .stamp_check
	rm _coverage.xml || true
	coverage run -m pytest -n 10
	coverage xml -o $@
	touch $@

.PHONY: typecheck tc
typecheck:
	pytest --mypy -m mypy
tc: typecheck

.PHONY: coverage test
coverage: _coverage.xml
	coverage report -m
test: coverage

.stamp_codecov: .stamp_check .stamp_check_codecovrc _coverage.xml _codecovrc
	codecov --required -t `cat _codecovrc` -f _coverage.xml
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

docs/demos/HELLO.md: docs/demos/HELLO.md.in $(SRC) .stamp_check
	./docs/demos/compile.sh $< $@

docs/demos/HELLO.py: docs/demos/HELLO.md ./docs/demos/tangle.sh
	./docs/demos/tangle.sh $< $@

.PHONY: demo_hello
demo_hello: docs/demos/HELLO.md docs/demos/HELLO.py

docs/demos/REPL.md: docs/demos/REPL.pmd $(SRC) .stamp_check_$(HOSTNAME)
	pweave -f markdown $<
	! cat $@ | grep -i traceback | tail -n +2 | grep -i traceback

docs/demos/REPL.py: docs/demos/REPL.pmd $(SRC) .stamp_check_$(HOSTNAME)
	ptangle $<

.PHONY: demo_repl
demo_repl: docs/demos/REPL.md docs/demos/REPL.py

.PHONY: demo_mdrun
demo_mdrun: docs/demos/MDRUN_test.md

docs/demos/MDRUN_test.md: docs/demos/MDRUN_test.md.in docs/demos/MDRUN.py $(SRC) .stamp_check
	python docs/demos/MDRUN.py -r $< $@

.PHONY: demos
demos: demo_hello demo_mdrun

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
	test -f $(WHEEL) || ( echo 'run `make wheel` first'; exit 1; )
	pip3 install --force $(WHEEL)
	pip3 hash $(WHEEL) > .stamp_installhash_$(HOSTNAME)

.PHONY: check
check: .stamp_check

# .PHONY: check
# check: $(WHEEL)
# 	pip3 hash $(WHEEL) > .stamp_piphash_$(HOSTNAME)
# 	@diff -u .stamp_piphash_$(HOSTNAME) .stamp_installhash_$(HOSTNAME) || ( \
# 		echo 'Did you install pylightnix systemwide by running `sudo -H make install` ?' ; exit 1 ; )

.PHONY: all
all: coverage docs demos wheel



