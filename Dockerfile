FROM python:latest

RUN pip3 install Flask

COPY ./entrypoint.sh /entrypoint.sh

COPY ./Projekt /app

ENTRYPOINT /entrypoint.sh

