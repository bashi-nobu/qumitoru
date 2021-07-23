###### README

## アプリケーション名
qumitoru(クミトル)<br><br>
<img width="475" alt="qumitoru-logo" src="https://user-images.githubusercontent.com/41232320/125572069-bf5982c5-3a23-4a60-8bf4-6e2f598d416c.png">


## アプリケーション概要

紙のアンケートをOCR機能を使って集計するアプリです。

## URL

https://qumitoru.net/
<br><br> ※ アプリケーションの利用にはログインが必須となっておりますのでお手数ですが下記のアカウント情報をご入力ください。

## テスト用アカウント

メールアドレス：admin<br>
パスワード：aktest23453

## アプリケーション機能一覧
- ユーザー管理機能(CRUD)
- アンケート用紙ダウンロード機能(PDFデータ)
- ダッシュボード機能
- OCR機能
- 集計データ管理機能(RU)
- ページネーション機能


## 使用技術
### Back
|  Name  |  Version  |  Packager  |  Note  |
| ---- | ---- | ---- | ---- |
|  python  |  3.7.0  |  pyenv  |    |
|  Django  |  2.2.24  |  pip  |    |
|  boto3  |  1.17.90  |  pip  |  Django側からs3操作  |
|  django-pandas  |  0.6.4  |  pip  |  ダッシュボードに表示するデータの整形  |
|  numpy  |  1.21.0  |  pip  |  ダッシュボードに表示するデータの整形  |
|  django-storages  |  1.11.1  |  pip  |  画像アップロード  |
|  Django REST framework  |  3.12.0  |  pip  |  RESTful API  |
|  djangorestframework-jwt  |  1.11.0  |  pip  |  API認証  |
|  pytest  |  6.2.4  |  pip  |    |
|  pytest-django  |  4.4.0  |  pip  |    |


### Front
|  Name  |  Version  |  Packager  |  Note  |
| ---- | ---- | ---- | ---- |
|  npm  |  6.14.6  |    |    |
|  VueCLI  |  3.5.0  |  npm  |    |
|  vuetify  |  2.4.0  |  npm  |  UI実装の効率化  |
|  sass  |  1.32.0  |  npm  |    |
|  axios  |  0.21.1  |  npm  |  BackendAPIとの非同期通信  |
|  vue-js-modal  |  2.0.0  |  npm  |  モーダル実装の効率化  |
|  vue-loading-template  |  1.3.2  |  npm  |    |
|  vue-session  |  1.0.0  |  npm  |  ユーザーセッションの管理  |
|  vue-google-charts  |  0.3.3  |  npm  |    |
|  @vue/cli-plugin-unit-jest  |  4.5.0  |  npm  |  ユニットテスト  |
|  @vue/cli-plugin-e2e-nightwatch  |  4.5.0  |  npm  |  E2Eテスト  |


### Database
|  Name  |  Version  |  Env  |
| ---- | ---- | ---- |
|  Aurora MySQL  |  5.7  |  Amazon Aurora(Production)  |
|  Aurora MySQL  |  5.7  |  Amazon Aurora(Staging)  |
|  MySQL  |  5.7  |  Docker(Dev)  |


### Back(Lambda)
|  Name  |  Version  |  Packager  |  Note  |
| ---- | ---- | ---- | ---- |
|  python  |  3.7.0  |    |    |
|  boto3  |  1.17.90  |  pip  |  Lambdaからs3操作  |
|  numpy  |  1.19.0  |  pip  |    |
|  PyMySQL  |  1.0.2  |  pip  |    |
|  opencv-python  |  4.4.0.40  |  pip  |  傾き補正・ノイズ除去・二値化処理  |
|  tensorflow  |  1.15.0  |  pip  |  画像認識処理  |

### ML(Generate prediction model)
|  Name  |  Version  |  Packager  |  Note  |
| ---- | ---- | ---- | ---- |
|  Tensorflow  |  1.14.0  |  conda  |    |
|  Keras  |  2.2.4  |  conda  |    |
|  Cuda  |  8.0  |  conda  |    |
|  cuDNN  |  5.1  |  conda  |    |
|  OpenCV  |  2.0  |  conda  |  傾き補正・ノイズ除去・二値化処理  |
|  numpy  |  1.19.0  |  conda  |    |

※ OCR処理で画像認識を行う機械学習モデルに関しては、[こちらの記事](https://qiita.com/ba--shi/items/09f5f2f119ffbd9bb316)にて詳細を説明しております。

## デプロイ構成

### 使用リソース
|  Name  |  Role  |
| ---- | ---- |
|  GitHub  |  ソースコードリポジトリ、ビルドイメージの元となるソース管理  |
|  GitHub Actions  |  Nginx、Django コンテナのBuild、ECRへのPush、<br>CLI経由でECSクラスター上のサービスおよびタスクの更新  |
|  ECR  |  コンテナリポジトリ  |
|  ECS(Fargate)  |  サーバーレスでコンテナを実行するデータプレーン  |

## 本番&ステージング環境(AWS)
- アプリケーションの作成・デプロイにDockerを使用するため、Amazon ECS を採用
- コンテナ管理効率化のためECS Fargateタイプを採用
- AWSの各リソースはTerraformによりコード管理
  - ※コードは`docker/terraform/src/`配下に設置
### 使用リソース
|  Name  |  Role  |
| ---- | ---- |
|  IAM  |  ユーザに対する権限設定・ロールの管理  |
|  Route 53  |	Domain Name Server<br>※ドメインは お名前.com で取得  |
|  VPC  |  仮想ネットワーク  |
|  -- VPC Endpoint  |  コンテナからS3やAPI Gatewayへアクセスする際のエンドポイント  |
|  S3  |  画像ファイルの保存  |
|  RDS(Aurora)  |  データベース  |
|  ECR  |  コンテナリポジトリ  |
|  ECS  |  コンテナデプロイ  |
|  -- Fargate  |  サーバーレスでコンテナを実行するデータプレーン  |
|  -- Auto Scaling  |  コンテナのオートスケーリング  |
|  -- ALB  |  ロードバランシング  |
|  -- InternetGateway  |  ゲートウェイ(VPC&インターネット間通信)  |
|  API Gateway  |  API作成・管理  |
|  Lambda  |  サーバレスなコード実行(OCR処理の実行)  |
|  -- RDS Proxy  |  LambdaからAuroraへのアクセスを効率化  |

## システム構成図
![システム構成図(5)](https://user-images.githubusercontent.com/41232320/125717320-d1aadad9-213f-4a81-9e45-06ec83d924ff.png)

## ローカル開発環境

### Host Machine
|  Name  |  Version  |
| ---- | ---- |
|  macOS Catalina  |  10.15.7  |
|  docker  |  18.09.2  |
|  docker-compose  |  1.29.1  |

### Host Machine (for ML Prediction Model Generation)
|  Name  |  Spec  |
| ---- | ---- |
|  OS  |  Windows10 Home 64bit  |
|  CPU  |  Intel Core i7  |
|  GPU  |  NVIDIA Geforce GTX 1070 8GB  |
|  HDD  |  １TB  |

## コンテナ一覧
|  Container Name  |  Role  |  Env  |
| ---- | ---- | ---- |
|  Nginx  |  Web  |  Development, Staging, Production  |
|  Vue  |   Frontend  |  Development  |
|  Django(&uWSGI)  |  Backend API  |  Development, Staging, Production  |
|  MySQL  |  DB  |  Development  |
|  json-server  |  Mock server  |  Development, Test  |
|  Lambda  |  Backend API  |  Development, Staging, Production  |
|  Terraform  |  IaC  |  Staging, Production  |

