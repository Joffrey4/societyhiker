from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from .models import Profile
from articles.models import Article


def author(request, link):
    try:
        author_data = Profile.objects.get(link=link)
        article_list = Article.objects.filter(author__profile__link=link).order_by('-date')[:6]
    except Profile.DoesNotExist:
        raise Http404("This page does not exist.")
    else:
        context = {'author': author_data, 'article_list': article_list}
        return render(request, 'account/author.html', context)


def author_list(request):
    try:
        author_list_data = Profile.objects.all()[:6]
    except:
        raise Http404("This page does not exist.")
    else:
        context = {'author_list': author_list_data}
        return render(request, 'account/author_list.html', context)