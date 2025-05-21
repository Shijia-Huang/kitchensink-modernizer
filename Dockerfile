# Use official Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN python -m ensurepip --upgrade && pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Set default environment variable (can be overridden at runtime)
ENV GOOGLE_API_KEY=your_key_here

# Set default entrypoint for CLI mode (can override when running)
ENTRYPOINT ["python", "analyze_code.py"]
