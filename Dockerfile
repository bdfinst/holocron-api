FROM python:slim

WORKDIR /app

RUN apt-get -y update && \
    apt-get -y install \
    gcc \
    psql

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
