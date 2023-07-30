## Description:

API Documentation and Schema available on title page (http://0.0.0.0:8000, 
http://localhost:8000 or http://127.0.0.1:8000 depending on operating system 
and software versions)

## Tech:

Based on:
- Python 3.10
- FastAPI 0.89.1
- SQLModel 0.0.8
- Alembic 1.9.2
- Uvicorn 0.20.0
- PostgreSQL 15.1
- Docker 20.10.22

## Setup Guide

## Running Docker container

```sh
docker-compose up -d
```
To run tests container use next command
```sh
docker-compose -f docker-compose.tests.yaml up -d
```

## Running locally

### Make .env file with database settings data in project root directory

```
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### Setup and activate venv

```sh
python3 -m venv venv
```

```sh
source venv/bin/activate
```

### Install requirements

```sh
pip install -r requirements.txt
```

### Create DB tables and apply migrations

```sh
alembic upgrade head
```

### Start App

```sh
python3 main.py
```