FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app
COPY learn-lao-8394d-firebase-adminsdk-w7adf-6f97d34e38.json /app/learn-lao-8394d-firebase-adminsdk-w7adf-6f97d34e38.json


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8080

# Start the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]