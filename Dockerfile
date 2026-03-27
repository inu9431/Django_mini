FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && \
    curl -Ls https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:/venv/bin:$PATH"
ENV UV_PROJECT_ENVIRONMENT=/venv

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
