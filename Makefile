.PHONY: run format lint lint-fix check help

# Run using docker
up:
	docker compose up -d

# Stop docker compose
stop:
	docker-compose stop

# Remove docker images 
clean:
	docker-compose down --volumes --remove-orphans --rmi local && \
	docker image prune -f

# Run the application using UV
run:
	uv run python main.py

# Format code using ruff
format:
	uv run ruff format .

# Lints code with ruff linter
lint:
	uv run ruff check . --fix

# Checks linting issues
check-lint:
	uv run ruff check . 

# Run format and lint checks
check: format check-lint

# Display available commands
help:
	@echo "Available commands:"
	@echo "  make run       - Run the application using UV"
	@echo "  make format    - Format code using ruff"
	@echo "  make lint      - Check code with ruff linter"
	@echo "  make lint-fix  - Auto-fix linting issues"
	@echo "  make check     - Run format and lint checks"
	@echo "  make help      - Display this help message"
