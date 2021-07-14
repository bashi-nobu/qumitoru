from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^v1/upload/(?P<id>.+)/$', views.UploadFile.as_view(), name='upload'),
    url(r'^v1/upload/$', views.UploadFile.as_view(), name='upload'),
]
