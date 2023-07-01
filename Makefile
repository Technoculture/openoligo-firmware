LIBNAME:=openoligo
TESTDIR:=tests
EXAMPLEDIR:=examples
DOCSDIR:=docs
APIDIR:=api

EXECNAME:=./$(EXAMPLEDIR)/dna_synthesis.py
SERVER_EXECNAME:=./$(APIDIR)/server.py

TARGET_HOSTNAME?=arm.local
TARGET_USER?=ubuntu
TARGET_DIR?=/home/$(TARGET_USER)
LOCAL_DIR:=$(shell pwd)

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
	@echo "  server          Run the API server"
	@echo "  install         Install the package"
	@echo "  shell           Run a shell in the virtual environment"
	@echo "  jupyter         Start a tunnel to the Jupyter notebook server"
	@echo "  clean           Clean up the directory"
	@echo
	@echo "Category: Code delivery"
	@echo "  publish         Publish the package"
	@echo "  deploy          Deploy the code to BeagleBone"
	@echo "  pull            Get the deployed code from BeagleBone"
	@echo "  ssh             SSH to BeagleBone"
	@echo
	@echo "Category: Miscellaneous"
	@echo "  tree            Display the project directory structure"
	@echo "  help            Print this help message"
	@echo 

all: format lint test coverage

run:
	@poetry run python $(EXECNAME)

server:
	@poetry run python $(SERVER_EXECNAME)

format:
	@poetry run isort $(LIBNAME) $(TESTDIR) $(EXAMPLEDIR) $(EXECNAME)
	@poetry run black $(LIBNAME) $(TESTDIR) $(EXAMPLEDIR) $(APIDIR)

format-check:
	@poetry run black --check $(LIBNAME) $(TESTDIR) $(EXAMPLEDIR)

lint:
	@poetry run pylint $(LIBNAME)
	@poetry run flake8 $(LIBNAME)

type:
	@poetry run mypy $(LIBNAME) $(EXAMPLEDIR) --check-untyped-defs

test: type
	@poetry run pytest 

docs:
	@poetry run pdocs as_html $(LIBNAME) --overwrite
	mv site/* $(DOCSDIR)

publish:
	@poetry publish --build

clean:
	rm *.log *.log.*

coverage:
	@poetry run coverage-badge -o .github/coverage.svg -f

req:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

install:
	@poetry lock
	@if [ -f /proc/cpuinfo ] && grep -q AM33XX /proc/cpuinfo; then \
		poetry install --extras "bb"; \
	elif [ -f /proc/cpuinfo ] && grep -q Raspberry /proc/cpuinfo; then \
		poetry install --extras "rpi"; \
	else \
		poetry install; \
	fi
	poetry run mypy --install-types

shell:
	@poetry shell

ssh:
	ssh $(TARGET_USER)@$(TARGET_HOSTNAME)

jupyter:
	@echo
	@echo "This will only open a tunnel to the Jupyter notebook server running on the Raspberry Pi"
	@echo
	@echo "To run the notebook server, run the following command on the Raspberry Pi:"
	@echo "  jupyter notebook --no-browser --port=8888"
	@echo
	@echo "Open http://localhost:8080/notebooks/scratch/api_scratchpad.ipynb in your browser"
	@echo
	ssh -N -L 8880:localhost:8888 $(TARGET_USER)@$(TARGET_HOSTNAME)

deploy-setup:
	@ansible-playbook -i $(TARGET_USER), deploy/setup.yml --ask-pass --ask-become-pass

deploy:
	rsync -avz $(LOCAL_DIR) $(TARGET_USER)@$(TARGET_HOSTNAME):$(TARGET_DIR)

pull:
	rsync -avz $(TARGET_USER)@$(TARGET_HOSTNAME):$(TARGET_DIR) $(LOCAL_DIR)

tree:
	@tre -E '__pycache__|.git|.DS_Store|build|dist|.github|.flake8|__init__.py|scratch|docs'

.PHONY: ghtest lint type help run test publish install ssh deploy deploy_init get_from_pi t docs
