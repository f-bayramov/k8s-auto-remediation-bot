# Use a lightweight Python base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the application logic
COPY main.py .

# Run unbuffered output to see logs in real-time in Kubernetes
CMD ["python", "-u", "main.py"]
