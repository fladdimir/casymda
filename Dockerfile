# Dockerfile for test execution 

FROM python:3.7-stretch
WORKDIR /usr/src
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
