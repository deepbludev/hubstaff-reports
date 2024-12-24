# Hubstaff Reports

This is a simple FastAPI application that generates reports from Hubstaff data.

It runs as a cron job every day at midnight and generates an activity report of the previous day for each member of the organization.

It also exposes an API endpoint to retrieve the report for a specific date in JSON format: 
- `GET /v1/reports/activity/?report_date={date}`

as well as as an endpoint to get the HTML-rendered report:
- `GET /reports/activity/?report_date={date}`

For both endpoints, the `report_date` parameter is optional and defaults to the current date.

## Requirements

- Python 3.12
- uv
- Docker

## Installation

Sync the dependencies using uv and create a config.yaml file from config.example.yaml:
```bash
make install
```

## Running the application

Make sure to set the correct values in the config.yaml file:
- Hubstaff API key
- Hubstaff App Token
- Hubstaff Organization ID
- Hubstaff user credentials
- SendGrid API key
- SendGrid verified sender email address
- Recipients email addresses

```bash
# Run application
make run

# Run dev server with hot reloading
make dev
```
## Running using Docker

To run using docker compose, you can use the following commands:

```bash
# Spin up a docker container with the application and build the image
make build
# Spin up a docker container with the application
make up
# Spin down the docker container
make down
# Stop the docker container
make stop
```

## Linting and formatting

```bash
# Run linter
make lint

# Run formatter
make format
```


