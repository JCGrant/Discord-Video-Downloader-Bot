FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
COPY pyproject.toml .
RUN mkdir src && touch src/main.py
RUN pip install --no-cache-dir .

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/main.py"]
