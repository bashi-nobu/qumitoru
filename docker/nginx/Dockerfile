# create dist directory (frontend build)
FROM node:12.18.3-buster as build-stage

WORKDIR /app

ADD ./vue/app/package.json package.json
ADD ./vue/app/package-lock.json package-lock.json

RUN apt-get update -qq && apt-get install -y libnss3-dev
RUN npm install

COPY /vue/app .
RUN npm run build

# start nginx
FROM nginx:1.18.0 as production-stage

# インクルード用のディレクトリ内を削除
RUN rm -R /etc/nginx/conf.d/*

RUN mkdir /var/www
RUN mkdir /var/www/static
RUN mkdir /var/www/html

ARG VUE_APP_API_ENDPOINT
ENV VUE_APP_API_ENDPOINT=${VUE_APP_API_ENDPOINT}

ADD ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
ADD ./docker/nginx/default.conf /etc/nginx/sites-available/default
ADD ./docker/nginx/default.conf /etc/nginx/sites-enabled/default
ADD ./django/qumitoru/uwsgi_params /etc/nginx/uwsgi_params
ADD ./django/qumitoru/static /var/www/static/
COPY --from=build-stage /app/dist /var/www/html/dist/
