FROM python:3.11.4-slim-buster as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

FROM base as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100


COPY pyproject.toml poetry.lock ./
COPY src ./src

RUN touch README.md \
    && pip install "poetry==1.6.1" --no-cache-dir \
    && poetry config virtualenvs.create false \
    && poetry build -f wheel

FROM base as final

COPY --from=builder /app/dist/*.whl ./

RUN pip install ./*.whl --no-cache-dir \
    && rm -rf /app/*.whl

CMD ["gunicorn", "--bind", "0.0.0.0:5000",  "--workers", "1", "--threads", "1", "-k", "uvicorn.workers.UvicornWorker", "auth.entrypoints.fastapi_app.app:app"]