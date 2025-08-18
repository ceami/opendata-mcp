FROM python:3.12-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir .

ENTRYPOINT ["open-data-mcp"]
CMD ["--transport", "http"]
