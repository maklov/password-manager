FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-cache

RUN uv pip install psycopg2-binary

COPY . .

EXPOSE 8000

# Strzał bezpośrednio ze środowiska .venv
CMD ["/app/.venv/bin/python", "-m", "uvicorn", "server:server", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]