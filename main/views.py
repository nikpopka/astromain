from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User


def index(request):
    print(request.user.username)


    return render(request, 'main/index.html', {
        'title': 'Ведическая астрология'
    })


def administrator(request):
    return 11