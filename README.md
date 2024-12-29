# Car Search Application

## Overview

This FastAPI-based web application enables efficient car search functionality with specific technical criteria. The application provides comprehensive capabilities for managing car data, including addition, deletion, and search operations with both JSON and XML response formats. It is designed with a focus on performance, maintainability, and robust testing coverage.

## Technical Requirements

The application requires the following technical components:

- Python 3.11
- PostgreSQL
- Ubuntu Operating System

## Installation and Setup

### PostgreSQL Database Configuration

Begin by updating your system packages and installing PostgreSQL:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Configure the PostgreSQL user and database.

Create the required database table structure:

```bash
psql -d car_search -U abdul

# In PostgreSQL prompt:
CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    length FLOAT,
    weight FLOAT,
    velocity FLOAT,
    color VARCHAR(255)
);
\q
```

### Application Setup

Set up your Python environment and install the necessary dependencies:

```bash
python3.11 -m venv venv
source venv/bin/activate
git clone <repository-url>
cd car_search
pip install -r requirements.txt
```

Create a `.env` file in the project root with the following configuration:

```plaintext
DB_USER=abdul
DB_PASSWORD=Rehman123
DB_NAME=car_search
DB_HOST=localhost
DB_PORT=5432
```


### Test Configuration


Create a `pytest.ini` file in the project root:

```ini
[pytest]
pythonpath = .
```

### Running Tests

Execute the test suite using the following commands:

```bash
# Run all tests
pytest tests/

# Run tests with coverage report
pytest --cov=src tests/
```

## Application Deployment

Start the FastAPI server using:

```bash
uvicorn src.main:app --reload
```

The application will be accessible at http://localhost:8000

## API Usage

### Adding a New Car

```bash
curl -X POST "http://localhost:8000/api/v1/cars" \
     -H "Content-Type: application/json" \
     -d '{"length": 4.5, "weight": 1500, "velocity": 200, "color": "red"}'
```

### Searching Cars (JSON Response)

```bash
curl -X POST "http://localhost:8000/api/v1/cars/search" \
     -H "Content-Type: application/json" \
     -d '{"length": 4.5, "color": "red"}'
```

### Searching Cars (XML Response)

```bash
curl -X POST "http://localhost:8000/api/v1/cars/search/xml" \
     -H "Content-Type: application/json" \
     -d '{"length": 4.5, "color": "red"}'
```

### Deleting a Car

```bash
curl -X DELETE "http://localhost:8000/api/v1/cars/{car_id}"
```

## Project Architecture

The application follows a modular architecture designed for maintainability and scalability:

```
car_search/
├── src/
│   ├── api/
│   │   └── v1/
│   │       └── router.py
│   ├── models/
│   │   └── car.py
│   ├── schemas/
│   │   └── car.py
│   ├── services/
│   │   └── car_service.py
│   └── main.py
├── config/
│   ├── database.py
│   └── settings.py
├── utils/
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_services.py
├── requirements.txt
└── .env
```

## API Documentation

The application provides comprehensive API documentation through two interfaces:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc


