# Pull base image
FROM python:3.13-alpine AS base
LABEL maintainer="github.com/Ridiealist"

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work diretory
RUN mkdir -p /code
WORKDIR /code

FROM base AS builder
# Install build dependencies and uv
RUN apk add --no-cache gcc libffi-dev musl-dev
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock /code/
RUN uv sync --frozen --no-dev --no-install-project

FROM base AS final
# Copy dependency filled virtual environment
RUN apk add --no-cache libffi libpq
COPY --from=builder /code/.venv /.venv

# Set cmd commands authentication
COPY ./scripts /scripts
RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    # backend folder is owned by root. change permissions on all of our files
    chown -R django-user:django-user . && \
    # directory 안에서 scripts가 실행될 수 있게 세팅
    chmod -R +x /scripts

# copy project
COPY --chown=django-user:django-user . /code
RUN chown -R django-user /code
EXPOSE 8000

# PATH params setting
ENV PATH="/scripts:/.venv/bin:$PATH"

# user settings
USER django-user
