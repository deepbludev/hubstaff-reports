# Install dependencies and create config.yaml
install:
	uv sync
	cp config.example.yaml config.yaml

# Run application
run:
	uv run fastapi dev app/main.py

# Run dev server with hot reloading
dev:
	uv run fastapi dev app/main.py

# Run linter
lint:
	uv run ruff check .

# Run formatter
format:
	uv run ruff check --fix .


