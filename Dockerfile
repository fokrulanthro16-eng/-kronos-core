FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim AS runtime

LABEL maintainer="KRONOS CORE Team"
LABEL version="1.0.0"
LABEL description="Autonomous Security & Prompt Architecture Gateway"

RUN groupadd --gid 10001 kronos \
    && useradd --uid 10001 --gid kronos --no-create-home --shell /sbin/nologin kronos

WORKDIR /app

COPY --from=builder /install /usr/local
COPY app/ ./app/

RUN chown -R kronos:kronos /app \
    && chmod -R 550 /app

USER kronos

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--no-access-log"]
