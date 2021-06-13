# develop or build
FROM node:12.18.3-buster

WORKDIR /app
RUN npm install -g @vue/cli@3.5.0
ADD ./vue/app/package.json package.json
ADD ./vue/app/package-lock.json package-lock.json
RUN apt-get update -qq && apt-get install -y libnss3-dev

# chromeをインストール
RUN apt-get update && \
    sh -c 'wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -' && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable


ADD ./docker/vue/start.sh /scripts/start.sh
RUN chmod +x /scripts/*

ENTRYPOINT [ "/scripts/start.sh" ]
