# Stage 1: Build the application image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Stage 2: Run the unittests
# Run the unittests
RUN python -m unittest discover tests

# Stage 3: Final image with the application
# Expose the port
EXPOSE 8000

# Variables
ENV API_URL=https://api.spacexdata.com/v5/launches/

# Run app
CMD ["python", "main.py"]
