# Pull official base Python Docker image
FROM python:3.10.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Make entrypoint executable
COPY entrypoint.sh /code/
RUN chmod +x /code/entrypoint.sh

# Copy wait-for-it script and make it executable
COPY wait-for-it.sh /code/
RUN chmod +x /code/wait-for-it.sh

# Copy the Django project
COPY . /code/