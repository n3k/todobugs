FROM python:3.10.4-alpine

WORKDIR /app

COPY . .


RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update 
RUN apk add python3 python3-dev mariadb-dev build-base 
RUN pip3 install mysqlclient 
RUN apk del python3-dev mariadb-dev build-base

RUN apk add netcat-openbsd

RUN pip install -r requirements.txt

RUN chmod +x ./wait.sh