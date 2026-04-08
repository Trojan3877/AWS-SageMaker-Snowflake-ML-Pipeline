# Dockerfile

# 1. Base image with Python
FROM python:3.9-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application code
COPY . .

# 5. Expose the port the Flask API listens on
EXPOSE 8080

# 6. Default command to launch the service
CMD ["python", "app.py"]
