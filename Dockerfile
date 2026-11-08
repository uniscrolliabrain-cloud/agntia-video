FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg fonts-dejavu-core && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml README.md ./
COPY agntia ./agntia
RUN pip install --no-cache-dir . && useradd --create-home --uid 10001 agntia && mkdir -p /app/data /app/inbox && chown -R agntia:agntia /app
USER agntia
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "agntia.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
