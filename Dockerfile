FROM python:3.10
LABEL authors="urtanto"

RUN mkdir proj
WORKDIR /proj

ENV PYTHONUNBUFFERED 1
ENV Server_starts "true"

COPY requirements.txt /proj/
RUN pip install -r requirements.txt
COPY . /proj/

ENTRYPOINT ./start.sh