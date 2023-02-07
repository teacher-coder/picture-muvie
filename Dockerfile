FROM python:3.11.1-alpine
LABEL maintainer="github.com/Ridiealist"

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN mkdir -p app/
WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache &&\
    rm 

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "picture_muvie.wsgi:application"]