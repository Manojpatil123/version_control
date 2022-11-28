###
### ~ Outgrow Dockerfile
###
FROM python:3.9.2-slim-buster
ARG VERSION

# Install dependancies
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/* 

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app


COPY boot.sh /
RUN chmod +x /boot.sh

ADD requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ADD . /app
RUN echo "${VERSION}" > version


EXPOSE 80
ENV WORKERS 1
ENV THREADS 1
ENV TIMEOUT 3000
CMD gunicorn --workers=4 --bind 0.0.0.0:5000 app:app
