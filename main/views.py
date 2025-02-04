from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from . models import Services, Clients, Orders


def index(request):


    return render(request, 'main/index.html', {
        'title': 'Ведическая астрология'
    })

@permission_required('main.view_services')
def administration_service(request):
    all_services = Services.objects.all()
    return render(request, 'main/administration_service.html', {
        'title': 'Услуги',
        'all_services': all_services,
    })








def administration_client(request):
    return render(request, 'main/administration_client.html', {
        'title': 'Клиенты'
    })

def administration_order(request):
    return render(request, 'main/administration_order.html', {
        'title': 'Заказы'
    })