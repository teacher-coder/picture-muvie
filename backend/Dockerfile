# Pull base image
FROM python:3.11.1-alpine as base
LABEL maintainer="github.com/Ridiealist"

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work diretory
RUN mkdir -p /code
WORKDIR /code

FROM base as builder
# Set PIP environment variables
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.3.2

# Install dependencies
RUN apk add --no-cache gcc libffi-dev musl-dev && \
    pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /code/
RUN python -m venv /.venv &&\
    poetry export -f requirements.txt | /.venv/bin/pip install -r /dev/stdin

FROM base as final
# Copy dependency filled virtual environment
RUN apk add --no-cache libffi libpq
COPY --from=builder /.venv /.venv

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
ADD . /code/
EXPOSE 8000

# PATH parmas setting
ENV PATH="/scripts:/.venv/bin:$PATH"

# user settings
USER django-user