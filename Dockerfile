# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies and SQLite
RUN apt-get update && \
    apt-get install -y sqlite3 libsqlite3-dev build-essential && \
    apt-get clean

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=multilang_site.settings
ENV PYTHONUNBUFFERED 1

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run database migrations
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Start the Django application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "multilang_site.wsgi:application"]
