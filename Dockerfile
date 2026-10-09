FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libfreetype6-dev pkg-config && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy both backend and frontend folders
COPY . .

# Run uvicorn pointing to the backend module
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
