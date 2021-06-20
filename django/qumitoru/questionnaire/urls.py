from rest_framework.routers import DefaultRouter
from questionnaire import views

router = DefaultRouter()
router.register('questionnaire', views.QuestionareScoreViewSet)

urlpatterns = router.urls
