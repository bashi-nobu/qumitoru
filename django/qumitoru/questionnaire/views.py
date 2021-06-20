from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
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
