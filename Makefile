help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  help - print this help"
	@echo "  lint - run linter"
	@echo "  type - run type checker"
	@echo "  ghtest - run the github action locally"

lint:
	poetry run flake8 openoligo
	poetry run black --check openoligo
	poetry run isort --check-only openoligo

type:
	poetry run mypy openoligo

ghtest:
	act --container-architecture linux/amd64

.PHONY: ghtest lint type help
