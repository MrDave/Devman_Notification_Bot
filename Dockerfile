# syntax=docker/dockerfile:1

FROM python:3.11
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN	python3 -m venv venv && \
	venv/bin/pip install -r requirements.txt --no-cache-dir
COPY . /opt/app/
CMD venv/bin/python3 main.py
