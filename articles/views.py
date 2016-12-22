from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .models import Category, Article, Comment
from django.contrib.auth.models import User


def article(request, link):
    try:
        article_data = Article.objects.get(link=link)
    except Article.DoesNotExist:
        raise Http404("This article does not exist.")
    else:
        context = {'article': article_data}
        if article_data.use_video:
            return render(request, 'articles/article_video.html', context)
        else:
            return render(request, 'articles/article_image.html', context)


def category(request, link):
    try:
        category_data = Category.objects.get(link=link)
        article_list = Article.objects.filter(category__link=link).order_by('-date')[:6]
    except Category.DoesNotExist:
        raise Http404("This page does not exist.")
    else:
        context = {'category': category_data, 'article_list': article_list}
        return render(request, 'articles/category.html', context)


def category_list(request):
    try:
        category_list_data = Category.objects.all()
    except:
        raise Http404("This page does not exist.")
    else:
        context = {'category_list': category_list_data}
        return render(request, 'articles/category_list.html', context)
