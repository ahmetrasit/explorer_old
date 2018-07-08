FROM python:3.5-alpine

MAINTAINER Ahmet R Ozturk

RUN apk update && \
     apk add --virtual build-deps gcc python-dev musl-dev && \
     apk add shadow bash git vim

RUN mkdir /config  
ADD /config/requirements.txt /config/  
RUN pip install -r /config/requirements.txt
RUN mkdir /src
WORKDIR /src
