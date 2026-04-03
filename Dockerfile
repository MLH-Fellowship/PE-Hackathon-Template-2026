FROM python:3.13-slim

WORKDIR /app

# Install uv (fast Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install dependencies first for better layer caching
COPY pyproject.toml .
RUN uv sync --no-dev

# Copy project files
COPY . .

# Flask app port
EXPOSE 5000

# Helpful defaults for local Docker runs
ENV FLASK_DEBUG=true
ENV DATABASE_HOST=host.docker.internal

# Run the Flask app and bind to all interfaces for container access
CMD ["uv", "run", "flask", "--app", "run:app", "run", "--host=0.0.0.0", "--port=8080"]