FROM python:3.7.5

ADD . /usr/hnews

WORKDIR /usr/hnews

COPY . .

RUN apt-get install libxml2-dev libxslt-dev libpq-dev && apt-get update

RUN pip install pipenv && pipenv install --system --deploy

EXPOSE 8888:8888

CMD ["/bin/bash", "deploy/run.sh"]
