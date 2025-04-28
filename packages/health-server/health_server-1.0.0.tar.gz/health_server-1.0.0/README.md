# Health Server

A simple health check server built with FastAPI.

## Installation

1. Clone the repository.
2. Navigate to the `health-server` directory.
3. Install the dependencies using pip:

```bash
pip install .
```

## Running the server

To run the FastAPI application, use uvicorn:

```bash
uvicorn health_server:app --reload
```

This will start the server at `http://127.0.0.1:8000`.

## Health Check Endpoint

The health check endpoint is available at `/health`. You can access it using a web browser or a tool like `curl`:

```bash
curl http://127.0.0.1:8000/health
```

This endpoint will return a JSON response indicating the health status:

```json
{"status": "ok"}