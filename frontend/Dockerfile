FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Command will be overridden by docker-compose
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
