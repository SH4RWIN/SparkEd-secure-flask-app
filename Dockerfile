# Use a slim Python 3.12 image as the base
FROM python:3.12-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt ./

# Install the Python dependencies
# Use --no-cache-dir to avoid storing cache data, reducing image size
# Installing system dependencies required for building Python packages
# libpq-dev is required for PostgreSQL support in Python
# apt-get update/upgrade and clean are good practices for slim images
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the necessary application files and directories into the container
COPY app.py ./
COPY database_init.py ./
COPY dbm.py ./
COPY smtp.py ./
COPY templates/ templates/
COPY static/ static/

# Expose the port the application will run on
EXPOSE 5000

# Command to run the application using gunicorn
# "app:app" refers to the 'app' Flask instance within the 'app.py' file
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
