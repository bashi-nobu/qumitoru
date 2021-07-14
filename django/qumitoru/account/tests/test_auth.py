import django
django.setup()

from account.models import User

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class UserAuthTests(APITestCase):
    def test_api_jwt(self):
        url = reverse('auth')
        u = User.objects.create_user(username='testusers', email='user@foo.com', password='password')
        u.is_active = False
        u.save()

        # activeではないユーザー情報では認証されない
        resp = self.client.post(url, {'username':'testusers', 'password':'password'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        u.is_active = True
        u.save()

        # activeなユーザー情報では認証される
        resp = self.client.post(url, {'username':'testusers', 'password':'password'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)

        # 登録されていないユーザー情報では認証されない
        resp = self.client.post(url, {'username':'faketestuser', 'password':'fakepasswords'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
