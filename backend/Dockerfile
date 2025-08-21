# Stage 1: Build stage - Install dependencies
FROM python:3.11-slim as builder

WORKDIR /usr/src/app

# Set environment variables to prevent generating .pyc files and to run python in unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt


# Stage 2: Final stage - Create the production image
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies from apt
# wkhtmltopdf is required for pdfkit
RUN apt-get update && \
    apt-get install -y wkhtmltopdf && \
    rm -rf /var/lib/apt/lists/*

# Copy pre-built wheels and requirements file from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

# Install the dependencies from the wheels, which is faster than building from source
RUN pip install --no-cache /wheels/*

# Copy the application code into the container
COPY . .

# The command to run the application will be specified in docker-compose.yml
# For a standalone run, the following command would be used:
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
