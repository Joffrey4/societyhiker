from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .models import Category, Article, Comment
from django.contrib.auth.models import User


# Create your views here.
def article(request, link):
    try:
        article = Article.objects.get(link=link)
    except Article.DoesNotExist:
        raise Http404("This article does not exist.")
    else:
        context = {'article': article}
        return render(request, 'articles/article_video.html', context)
