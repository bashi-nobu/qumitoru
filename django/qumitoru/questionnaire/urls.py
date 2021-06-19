from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from questionnaire import views
from django.conf.urls import include

router = DefaultRouter()
router.register('questionnaire', views.QuestionareScoreViewSet)

urlpatterns = router.urls
