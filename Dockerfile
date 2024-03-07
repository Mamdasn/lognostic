# syntax=docker/dockerfile:1

FROM python:3.11-alpine

# Set the working directory inside the container
WORKDIR /app

# Install Git and any other dependencies you might need
RUN apk update && \
    apk add --no-cache git

# Install Poetry
RUN pip install --user --no-cache-dir poetry

# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Copy the content of the local src directory to the working directory
COPY . .

# Using the --no-root option to avoid installing the main package
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

CMD ["sh", "-c", "poetry run pre-commit run --all-files && pip install -e . && pytest tests/"]
