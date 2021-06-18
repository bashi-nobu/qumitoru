import django
django.setup()

from uploader.tests.factories import UserFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

import json
from io import StringIO

class FileUploadTests(APITestCase):
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
