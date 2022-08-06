FROM python:3.9-alpine

WORKDIR /app

COPY ./requirements.txt .
COPY ./resolver.py .

RUN apk update                                           && \
    apk add --no-cache bind-tools                        && \
    chmod +x resolver.py                                 && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password -s /bin/bash resolver    && \
    chown resolver /app

USER resolver

COPY . .

ENTRYPOINT ["python3", "resolver.py", "-p", "55053", "-a", "0.0.0.0"]
