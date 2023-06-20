help:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  help 		print this help"
	@echo "  run 		run the application"
	@echo "  lint 		run linter"
	@echo "  type 		run type checker"

run:
	@poetry run openoligo

lint:
	poetry run flake8 openoligo
	poetry run black openoligo
	poetry run isort openoligo

type:
	poetry run mypy openoligo

.PHONY: ghtest lint type help
