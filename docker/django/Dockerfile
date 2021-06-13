FROM python:3.7
ENV PYTHONUNBUFFERED 1

ENV APP_ROOT /api
WORKDIR $APP_ROOT

COPY ./docker/django/requirements.txt $APP_ROOT/requirements.txt
RUN pip install -r $APP_ROOT/requirements.txt

COPY ./django/qumitoru $APP_ROOT
