help:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  help 		print this help"
	@echo "  run 		run the application"
	@echo "  lint 		run linter"
	@echo "  type 		run type checker"
	@echo "  ghtest 	run the github action locally"

run:
	@poetry run openoligo

lint:
	poetry run flake8 openoligo
	poetry run black --check openoligo
	poetry run isort --check-only openoligo

type:
	poetry run mypy openoligo

ghtest:
	act --container-architecture linux/amd64

.PHONY: ghtest lint type help
