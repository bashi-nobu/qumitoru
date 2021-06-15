import django
django.setup()

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
        resp = self.client.post(url, {'file': StringIO('test')})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.content)['result'], 'FAIL')

    def test_invalid_file_upload_error(self):
        url = reverse('uploader:upload')
        resp = self.client.post(url, {'file': StringIO('test'), 'user_id': 2})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.content)['result'], 'FAIL')

