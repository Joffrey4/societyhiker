from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from articles.models import Article


def index(request):
    try:
        article_list = Article.objects.order_by('-date')[:6]
    except:
        raise Http404("This page does not exist.")
    else:
        context = {'video': 'header', 'article_list': article_list}
        return render(request, 'homepage/base.html', context)
