from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<link>[\w-]+)', views.article, name='article'),
]
