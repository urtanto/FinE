FROM python:3.10
LABEL authors="urtanto"

RUN mkdir proj
WORKDIR /proj

ENV PYTHONUNBUFFERED 1
ENV Server_starts "true"

RUN apt update

ADD requirements.txt /proj/
RUN pip install -r requirements.txt
#dckr_pat_JTOIVXpL1XfDLpg0WwqwsW2FXa0
ADD . /proj/

ENTRYPOINT ./start.sh