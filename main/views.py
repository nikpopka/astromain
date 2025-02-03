from django.shortcuts import render, HttpResponse

def index(request):
    #return HttpResponse('111')
    return render(request, 'main/index.html', {
        'title': 'Ведическая астрология'
    })