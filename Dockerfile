FROM python:3.13-slim

WORKDIR /workspace

# Install uv (fast Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project files and install dependencies
COPY . .
RUN uv sync --no-dev

# Flask app port
EXPOSE 5000

# Helpful default for local Docker runs
ENV FLASK_DEBUG=true

# Run the root-level run.py Flask app and bind to all interfaces
CMD ["uv", "run", "flask", "--app", "run.py", "run", "--host=0.0.0.0", "--port=5000"]