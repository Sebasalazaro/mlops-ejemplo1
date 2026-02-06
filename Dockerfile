FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and configuration
COPY ./api /app/api/
COPY ./config /app/config/
COPY ./outputs /app/outputs/

# Expose API port
EXPOSE 8080

# Run the FastAPI application
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8080"]
