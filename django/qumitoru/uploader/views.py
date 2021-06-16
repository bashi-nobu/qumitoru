from rest_framework.permissions import AllowAny
import datetime
import json
import requests
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from django.http import JsonResponse
from questionnaire.models import QuestionareScore, Questionare

import boto3
from boto3.session import Session
import os

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
IMAGE_SCAN_API_URL = os.environ['IMAGE_SCAN_API_URL']
BUCKET_NAME = os.environ['BUCKET_NAME']

class UploadFile(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES['file']
            user_id = str(request.POST.get('user_id'))
            if user_id != 'None':
                dt_now = datetime.datetime.now()
                file_path = user_id + '/tmp/img_'+ dt_now.strftime('%Y_%m_%d_%H_%M_%S') +'.jpg'
                default_storage.save(file_path, file) # ファイル保存
                reading_result = self.request_read_file(file_path)
                if reading_result == 'success':
                    uploaded_imgs = self.uploadedImgData(user_id)
                    return JsonResponse({'result': 'SUCCESS', 'uploadFilesCount': self.uploadedImgsCount(uploaded_imgs)})
                else:
                    default_storage.delete(file_path)
                    return JsonResponse({'result': 'FAIL'})
            else:
                return JsonResponse({'result': 'FAIL'})
        except Exception as e:
            responseData = {'result': str(e), 'status': False}
            return JsonResponse(responseData)

    def get(self, request, *args, **kwargs):
        uploaded_imgs = self.uploadedImgData(request.GET.get("id"))
        uploaded_img_count = self.uploadedImgsCount(uploaded_imgs)
        responseData = {'count': uploaded_img_count}
        return JsonResponse(responseData)

    def put(self, request, *args, **kwargs):
        user_id = str(request.POST.get('user_id'))
        take_at = self.convertStrDate(str(request.POST.get('take_at')))
        # move from tmp dir to new dir
        file_path_list = self.copyImgFromTmpToCalculateDir(user_id, request.POST.get('take_at'))
        active_questionare = Questionare.objects.filter(is_active=1, user=user_id).first()
        # save db
        self.insertQuestionareData(user_id, take_at, active_questionare, file_path_list)
        return JsonResponse({'result': 'SUCCESS'})

    """
    modules
    """
    def request_read_file(self, file_path):
        json_data = json.dumps({"file_path": file_path})
        url = IMAGE_SCAN_API_URL
        headers = {"Content-Type" : "application/json"}
        try:
            response = requests.post(url, headers=headers, data=json_data, verify=False)
            res_body = json.loads(response.text)['body']
            result = json.loads(res_body)['reading_result']
        except Exception as e:
            print(e)
            result = 'error'
        return result

    def uploadedImgData(self, user_id):
        session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3 = session.resource('s3')
        bucket = s3.Bucket(BUCKET_NAME)
        uploaded_imgs = bucket.objects.filter(Prefix=str(user_id)+'/tmp')
        return uploaded_imgs

    def uploadedImgsCount(self, imgs):
        uploaded_img_count = 0
        for b in imgs:
            uploaded_img_count += 1
        return uploaded_img_count

    def copyImgFromTmpToCalculateDir(self, user_id, take_at):
        uploaded_imgs = self.uploadedImgData(user_id)
        file_path_list = []
        for img in uploaded_imgs:
            idx = img.key.find("/tmp/")
            file_name = img.key[idx+len("/tmp/"):]
            new_file_path = user_id + '/' + take_at + '/' + file_name
            s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            s3.Object(BUCKET_NAME, new_file_path).copy_from(CopySource={'Bucket': BUCKET_NAME, 'Key': img.key})
            s3.Object(BUCKET_NAME, img.key).delete()
            file_path_list.append(new_file_path)
        return file_path_list

    def convertStrDate(self, take_at):
        take_at = [int(i) for i in take_at.split('-')]
        take_at = datetime.date(take_at[0], take_at[1], take_at[2])
        return take_at

    def insertQuestionareData(self, user_id, take_at, active_questionare, file_path_list):
        questionareScores = []
        for file in file_path_list:
            questionareScore = QuestionareScore(
              questionare_id=active_questionare.id,
              file_path=file,
              take_at=take_at,
              day_of_week=take_at.weekday(),
              user_id=user_id
            )
            questionareScores.append(questionareScore)
        QuestionareScore.objects.bulk_create(questionareScores)

