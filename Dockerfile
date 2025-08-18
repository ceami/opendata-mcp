# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ADD . /app

WORKDIR /app
RUN uv sync && uv pip install -e .

ENTRYPOINT ["uv", "run", "open-data-mcp"]
CMD ["--transport", "http"]
