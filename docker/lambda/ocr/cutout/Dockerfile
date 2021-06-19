FROM python:3.7-buster

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  libsm6 \
  libxrender1 \
  libxtst6

# install openGL modules
RUN apt-get update && apt-get install -y libgl1-mesa-dev

# pip install awslambdaric
RUN pip install --upgrade pip && \
    pip install awslambdaric

# pip install requirements.txt
COPY ./docker/lambda/ocr/cutout/requirements.txt ./
RUN pip install -r ./requirements.txt

# Include global arg
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG BUCKET_NAME
ARG DB_HOST
ARG DB_NAME
ARG DB_USER
ARG DB_PASS

ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}
ENV BUCKET_NAME ${BUCKET_NAME}
ENV DB_HOST ${DB_HOST}
ENV DB_NAME ${DB_NAME}
ENV DB_USER ${DB_USER}
ENV DB_PASS ${DB_PASS}

# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie
COPY ./docker/lambda/ocr/cutout/entry.sh /entry.sh
RUN chmod 755 /entry.sh

ARG APP_DIR="/home/app/"
WORKDIR ${APP_DIR}
COPY ./docker/lambda/ocr/cutout/api/* ${APP_DIR}

# download cascade file from s3
RUN aws s3 cp --region ap-northeast-1 s3://qumitoru-dev/modules/cascade.xml ${APP_DIR}

ENTRYPOINT [ "/entry.sh" ]
CMD [ "app.handler" ]
