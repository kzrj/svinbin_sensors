FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /sensors_code
WORKDIR /sensors_code
ADD requirements.txt /sensors_code/
RUN pip install -r requirements.txt
ADD . /sensors_code/ 
EXPOSE 8001