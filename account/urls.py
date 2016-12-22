from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^auteur/(?P<link>[\w-]+)', views.author, name='author'),
    url(r'^auteur/', views.author_list, name='author_list')
]
