import django
django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from questionnaire.models import QuestionareScore
from questionnaire.tests.factories import MakeQuestionDataFactory

import datetime

class QuestionareScoreListTests(APITestCase):

    def test_get_no_data(self):
        url = reverse('questionnaire:questionarescore-list')
        resp = self.client.get(url, {'userid': 0, 'periodStart': datetime.date.today().strftime('%Y-%m-%d')}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 0)
        self.assertEqual(resp.data['results'], [])

    def test_get_data(self):
        q = MakeQuestionDataFactory.makeData(self)
        scoredata = QuestionareScore.objects.create(q1=10,q2=10,q3=5,q4=4,q5=4,q6=4,q7=4,day_of_week=1,is_finished=True,take_at=datetime.date.today(),user_id=q.user.id,questionare_id=q.id)
        url = reverse('questionnaire:questionarescore-list')
        resp = self.client.get(url, {'userid': q.user.id, 'periodStart': datetime.date.today().strftime('%Y-%m-%d')}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['results'][0]['id'], scoredata.id)
