ARG PYTHON_VERSION=3.7
ARG ALPINE_VERSION=3.7
FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

WORKDIR /app

COPY supervisord.conf /etc/
COPY . /app

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV BUILD_LIST git gcc make musl-dev

RUN apk add --update $BUILD_LIST \
    && apk add --update supervisor \
    && pip install --upgrade pip \
    && pip3 install pipenv \
    && pipenv install \
    && apk del $BUILD_LIST \
    && rm -rf /tmp/* /var/cache/apk/*

# Run processes with supervisord
ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]