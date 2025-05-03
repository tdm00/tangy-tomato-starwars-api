# Star Wars Quotes API

A versioned FastAPI application that returns a random Star Wars quote.

## Running Locally

```bash
# Create virtual environment and activate
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn starwars_api.main:app --reload
```

## Running Tests

```bash
pytest
```

## Using Docker

```bash
docker build -t starwars-api .
docker run -d -p 8000:8000 starwars-api
```
