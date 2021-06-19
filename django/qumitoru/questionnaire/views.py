from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.http.response import HttpResponse
from .models import QuestionareScore
from .serializers import QuestionareScoreSerializer
from .paginations import CustomPagination
from django.http import JsonResponse

import datetime

# Create your views here.

class QuestionareScoreViewSet(ModelViewSet):
    serializer_class = QuestionareScoreSerializer
    pagination_class = CustomPagination
    queryset = QuestionareScore.objects.all()
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(QuestionareScore, user_id=self.request.query_params.get("user_id"))

    def get_queryset(self):
        user_id = self.request.query_params.get("userid")
        period = self.makePeriodList(self.request)
        return QuestionareScore.objects.filter(user_id=user_id, take_at__range=period, is_finished=True).order_by('-take_at').reverse()

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


