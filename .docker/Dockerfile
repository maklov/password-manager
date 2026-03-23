FROM python:3.11-slim

# uv compiler
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# global package installation
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache
COPY . .

EXPOSE 8000

CMD ["uvicorn", "server:server", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
