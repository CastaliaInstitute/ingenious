FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY src/ src/

# Install dependencies
RUN uv sync --frozen || uv pip install -e .

EXPOSE 8001

CMD ["uv", "run", "uvicorn", "soca.main:app", "--host", "0.0.0.0", "--port", "8001"]
