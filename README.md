# Kribi Backend (FastAPI)

Simple FastAPI starter.

## Quick Start

1. Create & activate a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
```
2. Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
3. Run the dev server (auto-reload):
```bash
uvicorn main:app --reload --port 8000
```
4. Open in browser:
- Root: http://127.0.0.1:8000/
- Interactive docs (Swagger UI): http://127.0.0.1:8000/docs
- ReDoc docs: http://127.0.0.1:8000/redoc

## Example Requests
```bash
curl http://127.0.0.1:8000/
curl "http://127.0.0.1:8000/items/42?q=test"
```

## Project Structure
```
main.py            # FastAPI application
requirements.txt   # Python dependencies
README.md          # This file
```

## Production Tip
Use a proper ASGI server process manager (e.g. uvicorn with --workers, or run under gunicorn with uvicorn workers). Example:
```bash
gunicorn -k uvicorn.workers.UvicornWorker -w 4 main:app
```

