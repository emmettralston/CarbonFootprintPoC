FROM python:3.11-slim
WORKDIR /app

# Install deps
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY app ./app

# Ensure /app is on sys.path so "import app.*" works
ENV PYTHONPATH=/app

EXPOSE 8000
# Run using the package entrypoint
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
