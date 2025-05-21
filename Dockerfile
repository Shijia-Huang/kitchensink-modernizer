# Use official Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default environment variable (can be overridden at runtime)
ENV GOOGLE_API_KEY=your_key_here

# Set default entrypoint for CLI mode (can override when running)
ENTRYPOINT ["python", "analyze_code.py"]
