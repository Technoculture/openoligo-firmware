LIBNAME:=openoligo
EXECNAME:=server.py
TESTDIR:=tests
EXAMPLEDIR:=examples

help:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  all 		Run linting, type checking and tests 	<== If in doubt, use this target"
	@echo "  install 	Install the package"
	@echo "  run 		run the application"
	@echo "  format 	Format the code"
	@echo "  lint 		run linter"
	@echo "  type 		run type checker"
	@echo "  test 		run tests"
	@echo "  help 		print this help"

all: lint test coverage

run:
	@poetry run python $(EXECNAME)

format:
	poetry run black $(LIBNAME) $(TESTDIR) $(EXAMPLEDIR)
	poetry run isort $(LIBNAME) $(TESTDIR) $(EXAMPLEDIR)

lint: format
	poetry run pylint $(LIBNAME)
	poetry run flake8 $(LIBNAME) $(TESTDIR)

type:
	poetry run mypy $(LIBNAME)

test: type
	poetry run pytest 

publish:
	poetry publish --build

coverage:
	poetry run coverage-badge -o .github/coverage.svg

install:
	poetry lock
	@if [ -f /proc/cpuinfo ] && grep -q Raspberry /proc/cpuinfo; then \
		poetry install --extras "rpi"; \
	else \
		poetry install; \
	fi

.PHONY: ghtest lint type help run test publish install
