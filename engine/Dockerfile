# Dockerfile
FROM python:3.10

WORKDIR /api

COPY api/requirements.txt /api/
RUN pip install -r requirements.txt

COPY api /api

# Run Uvicorn with reload enabled
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]
