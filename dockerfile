FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app
COPY main.py .
COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh

EXPOSE 80

# Run uvicorn after waiting for DB
CMD ["./wait-for-it.sh", "db:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
