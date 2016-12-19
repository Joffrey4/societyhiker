from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {'video': 'header'}
    return render(request, 'homepage/base.html', context)
