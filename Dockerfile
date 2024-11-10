# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code and static files into the container
COPY app.py .
COPY static ./static
COPY ssl ./ssl
COPY src ./src

# Expose the port the app runs on
EXPOSE 5020

# Run the application
CMD ["python", "app.py"]
