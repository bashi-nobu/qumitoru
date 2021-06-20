from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import QuestionareScore, Questionare, QuestionareQuestion
from .serializers import QuestionareScoreSerializer
from .paginations import CustomPagination
from django.http import JsonResponse
from django_pandas.io import read_frame
import numpy as np
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
import datetime

# Create your views here.

class QuestionareScoreViewSet(ModelViewSet):
    serializer_class = QuestionareScoreSerializer
    pagination_class = CustomPagination
    queryset = QuestionareScore.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.request.query_params.get("userid")
        period = self.makePeriodList(self.request)
        return QuestionareScore.objects.filter(user_id=user_id, take_at__range=period, is_finished=True).order_by('-take_at').reverse()

    @action(detail=True, methods=['post'])
    def score_update(self, request, *args, **kwargs):
        score_list = self.convertInt(request.POST.get('scoreList').split(','))
        target_id = request.POST.get('target_id')
        QuestionareScore.objects.filter(pk=int(target_id)).update(
            q1=score_list[0],
            q2=score_list[1],
            q3=score_list[2],
            q4=score_list[3],
            q5=score_list[4],
            q6=score_list[5],
            q7=score_list[6]
        )
        return JsonResponse({'result': 'SUCCESS'})

    @action(detail=True, methods=['get'])
    def make_dashboard_data(self, request, *args, **kwargs):
        user_id = self.request.query_params.get("userid")
        period = self.makePeriodList(self.request)
        scoreData = QuestionareScore.objects.filter(user_id=user_id, take_at__range=period, is_finished=True).order_by('-take_at').reverse()
        if len(scoreData) > 0:
            activeQuestionnare = Questionare.objects.filter(user_id=user_id, is_active=True).first()
            scoreDataDf = read_frame(scoreData)
            category_names, question_name_list, c_q_column_name_list, c_q_index_list = self.getQuestionareData(activeQuestionnare)
            categoryAveList = self.calcScoreAverage(question_name_list, c_q_column_name_list, scoreDataDf)
            dailyScoreData = self.makeDailyScoreData(scoreDataDf, c_q_column_name_list, category_names)
            return JsonResponse({'categoryAveList': categoryAveList, 'dailyScoreData': dailyScoreData})
        else:
            return JsonResponse({'categoryAveList': [0,0,0,0,0,0], 'dailyScoreData': []})


    """
    modules
    """
    def makePeriodList(self, request):
        periodStart = request.query_params.get("periodStart")
        periodEnd = request.query_params.get("periodEnd")
        if periodEnd is None:
            periodStart = datetime.datetime.strptime(periodStart, '%Y-%m-%d')
            periodEnd = periodStart
        else:
            periodStart = datetime.datetime.strptime(periodStart, '%Y-%m-%d')
            periodEnd = datetime.datetime.strptime(periodEnd, '%Y-%m-%d')
        period = [periodStart, periodEnd]
        return period

    def convertInt(self, list):
        convertesList = [int(i) if i.isdigit() else None for i in list]
        return convertesList

    def getQuestionareData(self, questionare):
        qq = QuestionareQuestion.objects.filter(questionare_id=questionare.id)
        question_list, question_name_list, categorys, category_names = self.makeQuestionDataList(qq)
        c_q_column_name_list = []
        c_q_index_list = []
        for c in categorys:
            c_q_cn_list = []
            c_q_i_list = []
            for i in range(0,len(question_list)):
                if c == question_list[i].category.id:
                    c_q_cn_list.append('q'+str(i+1))
                    c_q_i_list.append(i+1)
            c_q_column_name_list.append(c_q_cn_list)
            c_q_index_list.append(c_q_i_list)
        return category_names, question_name_list, c_q_column_name_list, c_q_index_list

    def makeQuestionDataList(self, qq):
        question_list = []
        question_name_list = []
        category_list = []
        category_name_list = []
        for q in qq:
            question_list.append(q.question)
            question_name_list.append(q.question.contents)
            category_list.append(q.question.category.id)
            category_name_list.append(q.question.category.contents)
        categorys = sorted(set(category_list), key=category_list.index)
        category_names = sorted(set(category_name_list), key=category_name_list.index)
        return question_list, question_name_list, categorys, category_names

    def calcScoreAverage(self, question_name_list, c_q_column_name_list, scoreDataDf):
        categoryAveList = []
        scoreDataDf = scoreDataDf[scoreDataDf[0:len(question_name_list)] != -1]
        for c in c_q_column_name_list:
            mean_val = np.nanmean(scoreDataDf[c].values.flatten())
            categoryAveList.append(float(Decimal(mean_val).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)))
        return categoryAveList

    def makeDailyScoreData(self, scoreDataDf, c_q_column_name_list, category_names):
        takeAtList = scoreDataDf['take_at'].unique()
        dailyScoreAveListDf = self.makeDailyScoreAveListDf(takeAtList, scoreDataDf, category_names, c_q_column_name_list)
        dailyScoreData = []
        dailyScoreAveListDf['take_at'] = dailyScoreAveListDf.apply(lambda x: x['take_at'].strftime('%m-%d'), axis=1)
        for c in category_names:
            dataList = dailyScoreAveListDf[['take_at',c]].values.tolist()
            dataList.insert(0, ['take_at', c])
            dailyScoreData.append(dataList)
        return dailyScoreData

    def makeDailyScoreAveListDf(self, takeAtList, scoreDataDf, category_names, c_q_column_name_list):
        dailyScoreAveList = []
        for take_at in takeAtList:
            df = scoreDataDf[scoreDataDf['take_at'] == take_at]
            aveList = []
            for c in c_q_column_name_list:
                mean_val = np.nanmean(df[c].values.flatten())
                aveList.append(float(Decimal(mean_val).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)))
            aveList.append(take_at)
            dailyScoreAveList.append(aveList)
        category_names.append('take_at')
        dailyScoreAveListDf = pd.DataFrame(dailyScoreAveList, columns=category_names)
        return dailyScoreAveListDf
