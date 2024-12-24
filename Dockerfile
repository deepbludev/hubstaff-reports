## --- BASE
FROM python:3.12-slim-bookworm AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project into `/app`
WORKDIR /app

# Copy in pyproject.toml, uv.lock 
COPY pyproject.toml uv.lock /app/

# Install the project's dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev --no-install-project

# Add the rest of the project source code
COPY . /app

# Install project separately from its dependencies to optimize layer caching
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev 

## --- RUNNER
FROM builder AS runner

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app
# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"


EXPOSE 8000
CMD ["uv", "run", "fastapi", "dev", "app/main.py"]
