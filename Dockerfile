FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS python-base

ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    WORKDIR_PATH="/app" \
    VIRTUAL_ENV="/app/.venv"

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

FROM python-base AS builder-base

RUN apt-get update -qq && \
    apt-get install -y \
    build-essential

WORKDIR $WORKDIR_PATH

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable


FROM python-base AS production

COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV

WORKDIR $WORKDIR_PATH

ENTRYPOINT []

ENV HOST=0.0.0.0
ENV PORT=8000

CMD uvicorn --host $HOST --port $PORT pdf_service.api:app
