from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^article/(?P<link>[\w-]+)', views.article, name='article'),
    url(r'^categorie/(?P<link>[\w-]+)', views.category, name='category'),
    url(r'^categorie/', views.category_list, name='category_list'),
]
