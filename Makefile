LIBNAME:=openoligo
EXECNAME:=server.py
TESTDIR:=tests
EXAMPLEDIR:=examples

RPI_HOSTNAME?=openoligo.local
RPI_USER?=admin

LOCAL_DIR:=$(shell pwd)
REMOTE_DIR:=/home/$(RPI_USER)

# Using .DEFAULT_GOAL to explicitly define the default target
.DEFAULT_GOAL := help

help:
	@echo "     ___          ___                                  ___          ___       ";
	@echo "    /  /\        /  /\                    ___         /  /\        /  /\      ";
	@echo "   /  /::\      /  /::\                  /  /\       /  /:/_      /  /::\     ";
	@echo "  /  /:/\:\    /  /:/\:\   ___     ___  /  /:/      /  /:/ /\    /  /:/\:\    ";
	@echo " /  /:/  \:\  /  /:/  \:\ /__/\   /  /\/__/::\     /  /:/_/::\  /  /:/  \:\   ";
	@echo "/__/:/ \__\:\/__/:/ \__\:\\  \:\ /  /:/\__\/\:\__ /__/:/__\/\:\/__/:/ \__\:\  ";
	@echo "\  \:\ /  /:/\  \:\ /  /:/ \  \:\  /:/    \  \:\/\\  \:\ /~~/:/\  \:\ /  /:/  ";
	@echo " \  \:\  /:/  \  \:\  /:/   \  \:\/:/      \__\::/ \  \:\  /:/  \  \:\  /:/   ";
	@echo "  \  \:\/:/    \  \:\/:/     \  \::/       /__/:/   \  \:\/:/    \  \:\/:/    ";
	@echo "   \  \::/      \  \::/       \__\/        \__\/     \  \::/      \  \::/     ";
	@echo "    \__\/        \__\/                                \__\/        \__\/      ";
	@echo
	@echo "Usage: make [target]"
	@echo
	@echo "Category: Code quality checks"
	@echo "  format          Format the code"
	@echo "  lint            Run linter"
	@echo "  type            Run type checker"
	@echo "  test            Run tests"
	@echo "  docs            Generate documentation"
	@echo
	@echo "Category: Build and run"
	@echo "  all             Run format, lint, type checks, tests, and generate coverage report"
	@echo "  run             Run the application"
	@echo "  install         Install the package"
	@echo "  shell           Run a shell in the virtual environment"
	@echo "  jupyter         Start a tunnel to the Jupyter notebook server"
	@echo
	@echo "Category: Code delivery"
	@echo "  publish         Publish the package"
	@echo "  deploy          Deploy the code to Raspberry Pi"
	@echo "  get_from_pi     Get the deployed code from Raspberry Pi"
	@echo "  ssh             SSH to Raspberry Pi"
	@echo
	@echo "Category: Miscellaneous"
	@echo "  tree            Display the project directory structure"
	@echo "  help            Print this help message"
	@echo 

all: format lint test coverage

run:
	@poetry run python $(EXECNAME)

format:
	@poetry run black $(LIBNAME) $(TESTDIR) $(EXAMPLEDIR)

format_check:
	@poetry run black --check $(LIBNAME) $(TESTDIR) $(EXAMPLEDIR)

lint:
	@poetry run pylint $(LIBNAME)
	@poetry run flake8 $(LIBNAME) $(TESTDIR)

type:
	@poetry run mypy $(LIBNAME) $(TESTDIR) $(EXAMPLEDIR)

test: type
	@poetry run pytest 

docs:
	@poetry run pdocs as_html $(LIBNAME)

publish:
	@poetry publish --build

coverage:
	@poetry run coverage-badge -o .github/coverage.svg -f

install:
	@poetry lock
	@if [ -f /proc/cpuinfo ] && grep -q Raspberry /proc/cpuinfo; then \
		@poetry install --extras "rpi"; \
	else \
		@poetry install; \
	fi

shell:
	@poetry shell

ssh:
	ssh $(RPI_USER)@$(RPI_HOSTNAME)

jupyter:
	@echo
	@echo "This will only open a tunnel to the Jupyter notebook server running on the Raspberry Pi"
	@echo
	@echo "To run the notebook server, run the following command on the Raspberry Pi:"
	@echo "  jupyter notebook --no-browser --port=8888"
	@echo
	@echo "Open http://localhost:8080/notebooks/scratch/api_scratchpad.ipynb in your browser"
	@echo
	ssh -N -L 8880:localhost:8888 $(RPI_USER)@$(RPI_HOSTNAME)

deploy:
	rsync -avz $(LOCAL_DIR) $(RPI_USER)@$(RPI_HOSTNAME):$(REMOTE_DIR)

get_from_pi:
	rsync -avz $(RPI_USER)@$(RPI_HOSTNAME):$(REMOTE_DIR) $(LOCAL_DIR)

tree:
	@tre -E '__pycache__|.git|.DS_Store|build|dist|.github|.flake8|__init__.py|scratch|tests'

.PHONY: ghtest lint type help run test publish install ssh deploy deploy_init get_from_pi t
