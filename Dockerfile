# Base image with Python
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./

# Install the required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose a default port (not mandatory but good practice)
EXPOSE 5000

# Set the default command to run the script
CMD ["python", "main.py"]
