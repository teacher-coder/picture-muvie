# Pull base image
FROM python:3.11.1-alpine
LABEL maintainer="github.com/Ridiealist"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work diretory
RUN mkdir -p /code
WORKDIR /code

# install dependencies
ADD requirements.txt /code/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf /root/.cache/

# copy project
COPY scripts/start*.sh /code/
ADD . /code/