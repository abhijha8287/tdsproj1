# Use a Python base image
FROM python:3.11-slim

# Install Node.js and npm (which includes npx)
RUN apt-get update && apt-get install -y \
    curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose port 8000
EXPOSE 8000

# Set the entrypoint to run the Flask app
CMD ["python", "app.py"]
