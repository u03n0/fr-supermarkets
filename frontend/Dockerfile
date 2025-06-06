FROM python:3.9-slim
WORKDIR /app

# Copy requirements from root (no ../ needed since context is root)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy frontend code
COPY frontend/ ./frontend/

CMD ["streamlit", "run", "frontend/main.py", "--server.address", "0.0.0.0"]
