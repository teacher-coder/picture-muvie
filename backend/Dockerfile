# Pull base image
FROM python:3.11.1-alpine
LABEL maintainer="github.com/Ridiealist"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt /tmp/requirements.txt
COPY ./scripts /scripts

# Set work diretory
RUN mkdir -p /code
WORKDIR /code
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/ && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    # backend folder is owned by root. change permissions on all of our files
    chown -R django-user:django-user . && \
    # directory 안에서 scripts가 실행될 수 있게 세팅
    chmod -R +x /scripts

# copy project
ADD . /code/

# PATH parmas setting
ENV PATH="/scripts:/py/bin:$PATH"

# user settings
USER django-user