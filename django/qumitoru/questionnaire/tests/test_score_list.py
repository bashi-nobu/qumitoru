import django
django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from questionnaire.models import QuestionareScore
from questionnaire.tests.factories import MakeQuestionDataFactory

import datetime
import json

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

    def test_update_score_data(self):
        q = MakeQuestionDataFactory.makeData(self)
        scoredata = QuestionareScore.objects.create(q1=10,q2=10,q3=5,q4=4,q5=4,q6=4,q7=4,day_of_week=1,is_finished=True,take_at=datetime.date.today(),user_id=q.user.id,questionare_id=q.id)
        url = reverse('questionnaire:questionarescore-score-update', kwargs=dict(pk=u'1'))
        resp = self.client.post(url, {'scoreList': ['1,1,1,1,1,1,1'], 'target_id': [str(scoredata.id)]})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(QuestionareScore.objects.filter(pk=scoredata.id).first().q1, 1)
        self.assertEqual(json.loads(resp.content)['result'], 'SUCCESS')

    def test_get_dashboard_data_none_data(self):
        q = MakeQuestionDataFactory.makeData(self)
        url = reverse('questionnaire:questionarescore-make-dashboard-data', kwargs=dict(pk=u'1'))
        resp = self.client.get(url, {'userid': q.user.id, 'periodStart': datetime.date.today().strftime('%Y-%m-%d')}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.content)['categoryAveList'], [0, 0, 0, 0, 0, 0])
        self.assertEqual(json.loads(resp.content)['dailyScoreData'], [])

    def test_get_dashboard_data(self):
        q = MakeQuestionDataFactory.makeData(self)
        QuestionareScore.objects.create(q1=10,q2=10,q3=5,q4=4,q5=4,q6=4,q7=4,day_of_week=1,is_finished=True,take_at=datetime.date.today(),user_id=q.user.id,questionare_id=q.id)
        QuestionareScore.objects.create(q1=8,q2=8,q3=5,q4=4,q5=4,q6=4,q7=4,day_of_week=1,is_finished=True,take_at=datetime.date.today(),user_id=q.user.id,questionare_id=q.id)
        url = reverse('questionnaire:questionarescore-make-dashboard-data', kwargs=dict(pk=u'1'))
        resp = self.client.get(url, {'userid': q.user.id, 'periodStart': datetime.date.today().strftime('%Y-%m-%d')}, format='json')
        take_at_date = datetime.date.today().strftime('%m-%d')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.content)['categoryAveList'], [9.0, 9.0, 5.0, 4.0, 4.0, 4.0, 4.0])
        self.assertEqual(
          json.loads(resp.content)['dailyScoreData'],
          [
            [
              ['take_at', 'category_0'],
              [take_at_date, 9.0]
            ],
            [
              ['take_at', 'category_1'],
              [take_at_date, 9.0]
            ],
            [
              ['take_at', 'category_2'],
              [take_at_date, 5.0]
            ],
            [
              ['take_at', 'category_3'],
              [take_at_date, 4.0]
            ],
            [
              ['take_at', 'category_4'],
              [take_at_date, 4.0]
            ],
            [
              ['take_at', 'category_5'],
              [take_at_date, 4.0]
            ],
            [
              ['take_at', 'category_6'],
              [take_at_date, 4.0]
            ],
            [
              ['take_at', 'take_at'],
              [take_at_date, take_at_date]
            ]
          ]
        )
