# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements/base.txt ./requirements.txt
RUN pip install -r ./requirements.txt

# copy project
COPY . .

CMD gunicorn --bind 0.0.0.0:8000 config.wsgi:application
