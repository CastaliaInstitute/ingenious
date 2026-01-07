FROM python:3.13-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ src/

# Install dependencies
RUN pip install --no-cache-dir .

EXPOSE 8001

CMD ["uvicorn", "soca.main:app", "--host", "0.0.0.0", "--port", "8001"]
