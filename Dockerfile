FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt
RUN apt-get update

RUN apt-get install -y binutils libproj-dev gdal-bin
RUN apt-get install -y libgeos++
RUN apt-get install -y proj-bin

RUN pip install -r requirements.txt