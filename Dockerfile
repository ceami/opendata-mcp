# Dockerfile 예시 - MCP 서버용
FROM python:3.12-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir .

# 서비스 키 환경변수로 전달 (예: SMITHERY_SERVICE_KEY 사용)
ENV SMITHERY_SERVICE_KEY=YOUR_SERVICE_KEY_HERE

ENTRYPOINT ["open-data-mcp", "--transport", "http", "--service-key", "${SMITHERY_SERVICE_KEY}"]
