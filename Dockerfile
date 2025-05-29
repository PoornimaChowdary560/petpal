# Use official Python image as base
FROM python:3.12-slim

# Install system packages needed for mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Create and activate virtual environment
RUN python -m venv --copies /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the whole project
COPY . .

# Expose port (adjust if needed)
EXPOSE 8000

# Command to run your Django app
CMD ["gunicorn", "petpal.wsgi:application", "--bind", "0.0.0.0:8000"]
