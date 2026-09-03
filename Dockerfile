FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install system libraries required by the Python image-processing dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    imagemagick \
    libmagickwand-dev \
    && rm -rf /var/lib/apt/lists/*

# Install third-party dependencies before copying app code so Docker can reuse
# this layer when only templates, CSS, or Python modules change.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY . .
RUN uv sync --locked --no-dev

RUN addgroup --system gest && adduser --system --ingroup gest gest
RUN mkdir -p /app/public/static /app/public/media && chown -R gest:gest /app/public

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER gest

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["fastpysgi", "core.wsgi:application", "--host", "0.0.0.0", "--port", "8000"]
