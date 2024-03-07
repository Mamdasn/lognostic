# syntax=docker/dockerfile:1

FROM python:3.11-alpine

# Set the working directory inside the container
WORKDIR /app

# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Install Git, Poetry, and set Poetry configuration in one layer
RUN apk update && apk add --no-cache git && \
    pip install --user --no-cache-dir poetry && \
    poetry config virtualenvs.create false

# Copy the content of the local src directory to the working directory
COPY . .

# Using the --no-root option to avoid installing the main package
RUN poetry install --no-root

# Execute pre-commit checks, install the package in editable mode, and run tests
# This serves as the default command when the container starts
CMD ["sh", "-c", "poetry run pre-commit run --all-files && pip install -e . && pytest tests/"]
