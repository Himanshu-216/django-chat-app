FROM python:3-slim

RUN apt update && apt install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential

WORKDIR /app

COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt

COPY . .


