.PHONY: help install test clean dev-install format lint type-check build upload-test upload

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install the package and dependencies"
	@echo "  dev-install  - Install in development mode with dev dependencies"
	@echo "  test         - Run tests"
	@echo "  format       - Format code with black"
	@echo "  lint         - Run flake8 linter"
	@echo "  type-check   - Run mypy type checker"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build distribution packages"
	@echo "  upload-test  - Upload to test PyPI"
	@echo "  upload       - Upload to PyPI"
	@echo "  setup        - Run setup script"

# Setup virtual environment and install
install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

# Development installation
dev-install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e ".[dev]"

# Run tests
test:
	.venv/bin/python -m pytest tests/ -v

# Format code
format:
	.venv/bin/black .
	.venv/bin/black tests/

# Lint code
lint:
	.venv/bin/flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	.venv/bin/flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

# Type checking
type-check:
	.venv/bin/mypy rundeck_mcp_server.py

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build distribution packages
build: clean
	.venv/bin/python -m build

# Upload to test PyPI
upload-test: build
	.venv/bin/python -m twine upload --repository testpypi dist/*

# Upload to PyPI
upload: build
	.venv/bin/python -m twine upload dist/*

# Run setup script
setup:
	chmod +x setup.sh
	./setup.sh

# Test connection
test-connection:
	.venv/bin/python tests/test_server.py

# Test multi-server
test-multi:
	.venv/bin/python tests/test_multi_server.py

# Debug jobs
debug-jobs:
	.venv/bin/python tests/debug_jobs.py

# Configure Claude Desktop
configure-claude:
	.venv/bin/python tests/get_claude_config.py

# All quality checks
check: format lint type-check test

# Full development setup
dev-setup: dev-install configure-claude test-connection
	@echo "Development setup complete!"