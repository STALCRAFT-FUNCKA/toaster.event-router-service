# Use Python 3.10 base image
FROM python:3.10.0

# Metadata
LABEL author="Oidaho" email="oidahomain@gmail.com"

# Set build arguments
ARG TOKEN
ARG GROUPID

# Set environment variables
ENV TOKEN $TOKEN
ENV GROUPID $GROUPID

# Set working directory
WORKDIR /service

# Install poetry
RUN pip install poetry

# Copy only the dependency information
COPY pyproject.toml poetry.lock ./

# Install dependencies using poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "start.py"]