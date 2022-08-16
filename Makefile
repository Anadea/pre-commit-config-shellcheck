.ONESHELL:
PHONY: install tox test bumpversion build check check-build check-upload upload coveralls release help
NAME ?= pre-commit-config-shellcheck
TEST_PYPI_URL ?= https://test.pypi.org/legacy/
BUILD_TYPES ?= bdist_wheel sdist
VERSION ?= `python -c "import configparser; config = configparser.ConfigParser(); config.read('setup.cfg'); print(config['metadata']['version']);"`


install:
	python -m pip install .[test];\


tox:
	tox;\


test:
	py.test -v tests --cov=pre_commit_config_shellcheck --color=yes --instafail $(TESTS);\


bumpversion:
	git tag -a $(VERSION) -m "v$(VERSION)";\

build:
	python setup.py $(BUILD_TYPES);\


check:
	bash -c 'NAME="$(NAME)" pre-commit run --all-files';\


check-build:
	twine check dist/*;\


check-upload:
	twine upload --skip-existing --repository-url $(TEST_PYPI_URL) -u __token__ -p $${TEST_TWINE_PASSWORD} dist/*;\


upload:
	twine upload --skip-existing dist/*;\


coveralls:
	coveralls;\


release:
	make bumpversion && \
	git push && \
	git push --tags && \
	make build -B && \
	make check-build && \
	make check-upload && \
	make upload;\


help:
	@echo "    help:"
	@echo "        Show this help."
	@echo "    install:"
	@echo "        Install requirements."
	@echo "    tox:"
	@echo "        Run tox."
	@echo "    test:"
	@echo "        Run tests, can specify tests with 'TESTS' variable."
	@echo "    bumpversion:"
	@echo "        Tag current code revision with version."
	@echo "    build:"
	@echo "        Build python packages, can specify packages types with 'BUILD_TYPES' variable."
	@echo "    check:"
	@echo "        Perform some code checks."
	@echo "    check-build:"
	@echo "        Run twine checks."
	@echo "    check-upload:"
	@echo "        Upload package to test PyPi using twine."
	@echo "    upload:"
	@echo "        Upload package to PyPi using twine."
	@echo "    coveralls:"
	@echo "        Upload coverage report to Coveralls."
	@echo "    release:"
	@echo "        Release code."
