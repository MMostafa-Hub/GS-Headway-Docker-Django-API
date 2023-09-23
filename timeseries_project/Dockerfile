# Use an official Python runtime as the base image
FROM python:3.9

# Set environment variables for Python 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /timeseries_project

# Install dependencies
COPY requirements.txt /timeseries_project/
RUN pip install -r requirements.txt

# Copy the rest of the timeseries_project to the container
COPY . /timeseries_project/
