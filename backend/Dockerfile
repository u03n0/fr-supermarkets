FROM python:3.9-slim
WORKDIR /app

# Copy requirements from root (no ../ needed since context is root)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
