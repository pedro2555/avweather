PHONY: help prepare-dev test lint run doc

PYTHON_VER=3.6
VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python${PYTHON_VER}

.DEFAULT: help
help:
	@echo "make prepare-dev"
	@echo "       prepare development environment, use only once"
	@echo "make test"
	@echo "       run tests"
	@echo "make lint"
	@echo "       run pylint and mypy"
	@echo "make run"
	@echo "       run project"
	@echo "make doc"
	@echo "       build sphinx documentation"

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: requirements.txt
	test -d $(VENV_NAME) || virtualenv -p python${PYTHON_VER} $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt
	touch $(VENV_NAME)/bin/activate

prepare-dev:
	sudo apt-get -y install python3.7 python3-pip
	python3 -m pip install virtualenv
	make venv

test: venv
	${PYTHON} -m pytest tests

lint: venv
	${PYTHON} -m pylint avweather

