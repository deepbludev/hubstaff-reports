# Hubstaff Reports

This is a simple FastAPI application that generates reports from Hubstaff data.
It runs as a cron job every day at midnight and generates an activity report of the previous day for each member
of the organization.

## Requirements

- Python 3.12
- Hubstaff API key
- Hubstaff Organization ID
- Hubstaff user credentials

## Installation

Sync the dependencies using uv and create a config.yaml file:
```bash
make install
```

## Running the application

```bash
# Run application
make run

# Run dev server with hot reloading
make dev
```

## Linting and formatting

```bash
# Run linter
make lint

# Run formatter
make format
```
