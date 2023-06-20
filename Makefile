LIBNAME:=openoligo

help:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  help 		print this help"
	@echo "  run 		run the application"
	@echo "  lint 		run linter"
	@echo "  type 		run type checker"
	@echo "  test 		run tests"

run:
	@poetry run python main.py

lint:
	poetry run flake8 $(LIBNAME)
	poetry run black $(LIBNAME)
	poetry run isort $(LIBNAME)

type:
	poetry run mypy $(LIBNAME)

test: type
	poetry run pytest 

.PHONY: ghtest lint type help run test
