# Stage 1: Builder 
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# DS-0029: minimize image size.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Fix CVE-2026-0861: upgrade libc-bin and libc6
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY . .

RUN chmod +x entrypoint.sh

# DS-0002: run as non-root user
RUN useradd -r -u 1001 -s /sbin/nologin appuser
USER appuser

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]