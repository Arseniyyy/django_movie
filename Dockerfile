# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt update && \
    apt install -y --no-install-recommends \
    gcc \
    apt-utils \
    make \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app
COPY Makefile /app
# RUN make collectstatic

# Expose port 8000 to the outside world
EXPOSE 8000
