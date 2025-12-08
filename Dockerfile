# Use Python 3.13 slim image
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.6.8 /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY uv.lock ./


RUN uv sync --no-dev --frozen
ENV PATH="/messages/.venv/bin:$PATH"

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 8888

# Command to run the application
CMD ["uv", "run", "python", "main.py"]
