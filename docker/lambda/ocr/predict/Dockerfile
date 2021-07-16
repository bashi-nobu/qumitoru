FROM tensorflow/tensorflow:1.15.0-py3

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

RUN pip install --upgrade pip && \
    pip install awslambdaric

COPY ./docker/lambda/ocr/predict/requirements.txt ./
RUN pip install -r ./requirements.txt

# Include global arg in this stage of the build
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG BUCKET_NAME

ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}
ENV BUCKET_NAME ${BUCKET_NAME}

# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie
COPY ./docker/lambda/ocr/predict/entry.sh /entry.sh
RUN chmod 755 /entry.sh

ARG APP_DIR="/home/app/"
WORKDIR ${APP_DIR}
COPY ./docker/lambda/ocr/predict/api/* ${APP_DIR}

# download predict model file from s3
RUN aws s3 cp --region ap-northeast-1 s3://qumitoru-dev/modules/scale1_predict_model.pb ${APP_DIR}
RUN aws s3 cp --region ap-northeast-1 s3://qumitoru-dev/modules/scale2_predict_model.pb ${APP_DIR}
RUN aws s3 cp --region ap-northeast-1 s3://qumitoru-dev/modules/scale1_none_check_predict_model.pb ${APP_DIR}
RUN aws s3 cp --region ap-northeast-1 s3://qumitoru-dev/modules/scale2_none_check_predict_model.pb ${APP_DIR}

ENTRYPOINT [ "/entry.sh" ]
CMD [ "app.handler" ]
