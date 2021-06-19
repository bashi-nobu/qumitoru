import django
django.setup()

from uploader.tests.factories import UserFactory, QuestionareFactory
from questionnaire.models import QuestionareScore
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APISimpleTestCase

import requests
import json
from io import StringIO
import boto3

from django.contrib.auth import get_user_model
UserModel = get_user_model()

class FileUploadTests(APISimpleTestCase):
    databases = '__all__'

    def test_get_uploaded_file_data(self):
        url = reverse('uploader:upload', kwargs={'id': 1})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.content)['count'], 0)

    def test_none_user_upload_file_error(self):
        url = reverse('uploader:upload')
        resp = self.client.post(url, {'file': StringIO('test'), 'user_id': 0})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.content)['result'], 'FAIL')

    def test_invalid_file_upload_error(self):
        url = reverse('uploader:upload')
        resp = self.client.post(url, {'file': StringIO('test'), 'user_id': 1})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.content)['result'], 'FAIL')

    def test_invalid_file_upload_success(self):
        user1 = UserFactory()
        url = reverse('uploader:upload')
        image = "uploader/tests/files/invalid_upload_file.jpg"
        resp = self.client.post(url, {'file': (open(image, 'rb'), image), 'user_id': user1.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.content)['result'], 'FAIL')

    def test_valid_file_upload_success(self):
        user1 = UserFactory()
        url = reverse('uploader:upload')
        image = "uploader/tests/files/valid_upload_file.jpg"
        resp = self.client.post(url, {'file': (open(image, 'rb'), image), 'user_id': user1.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.content)['result'], 'SUCCESS')
        # delete upload file in s3
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('qumitoru-test')
        bucket.objects.filter(Prefix=str(user1.id)+"/").delete()

    def test_valid_file_upload_and_aggregate_success(self):
        q = QuestionareFactory()
        user1 = q.user

        # upload image file
        url = reverse('uploader:upload')
        ocr_lambda_entrypoint = 'http://172.17.0.1:9010/2015-03-31/functions/function/invocations'
        image = "uploader/tests/files/valid_upload_file.jpg"
        self.client.post(url, {'file': (open(image, 'rb'), image), 'user_id': user1.id})

        # start aggregate
        resp = self.client.put(url, {'take_at': '2021-06-17', 'user_id': user1.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.content)['result'], 'SUCCESS')

        # start ocr
        target_id = QuestionareScore.objects.all().first().id
        self.assertEqual(QuestionareScore.objects.all().first().is_finished, False)
        json_data = json.dumps({'target_id': target_id})
        headers = {"Content-Type" : "application/json"}
        requests.post(ocr_lambda_entrypoint, headers=headers, data=json_data, verify=False)
        self.assertEqual(QuestionareScore.objects.all().first().is_finished, True)

        # delete upload file in s3
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('qumitoru-test')
        bucket.objects.filter(Prefix=str(user1.id)+"/").delete()

