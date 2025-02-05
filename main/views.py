from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from . models import Services, Clients, Orders


def index(request):
    all_services = Services.objects.all()


    return render(request, 'main/index.html', {
        'title': 'Ведическая астрология',
        'all_services': all_services,
    })

@permission_required('main.view_services')
def administration_service(request):
    all_services = Services.objects.all()

    if request.method == "POST":
        new_name = request.POST.get('service_name')
        new_description = request.POST.get('service_description')
        new_price = request.POST.get('service_price')

        new_service = Services(
            name=new_name,
            description=new_description,
            price=new_price
        )
        new_service.save()
        return redirect("administration_service")


    return render(request, 'main/administration_service.html', {
        'title': 'Услуги',
        'all_services': all_services,
    })


def edit_service(request, id):
    service = Services.objects.get(id=id)
    if request.method == 'POST':
        new_name = request.POST.get('service_name')
        new_description = request.POST.get('service_description')
        new_price = request.POST.get('service_price')
        service.name = new_name
        service.description = new_description
        service.price = new_price
        service.save()

        return redirect('administration_service')


    return render(request, 'main/administration_service_edit.html', {
        'title': service.name,
        'service': service
    })


def delete_service(request, id):
    service = Services.objects.get(id=id)
    service.delete()
    return redirect('administration_service')



def administration_client(request):
    return render(request, 'main/administration_client.html', {
        'title': 'Клиенты'
    })

def administration_order(request):
    return render(request, 'main/administration_order.html', {
        'title': 'Заказы'
    })