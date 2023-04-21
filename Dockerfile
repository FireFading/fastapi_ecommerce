FROM python:3.11.0-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
ADD ./requirements.txt /code/

RUN pip install --upgrade -r ./requirements.txt
