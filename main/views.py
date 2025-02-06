from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import permission_required
from . models import Services, Clients, Orders

main_user = "popov"

def index(request):
    all_services = Services.objects.all()
    form_auth = AuthenticationForm()
    if request.method == "POST":
        form_auth = AuthenticationForm(request, data=request.POST)
        if form_auth.is_valid():
            username = form_auth.cleaned_data.get("username")
            password = form_auth.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return redirect('main')


    return render(request, 'main/index.html', {
        'title': 'Ведическая астрология',
        'all_services': all_services,
        'form_auth': form_auth,
    })

@permission_required('main.view_services')
def administration_service(request):
    if request.user.username == main_user:
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
    else:
        return redirect('main')

def edit_service(request, id):
    if request.user.username == main_user:
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
    else:
        return redirect('main')



def delete_service(request, id):
    if request.user.username == main_user:
        service = Services.objects.get(id=id)
        service.delete()
        return redirect('administration_service')
    else:
        return redirect('main')




def administration_client(request):
    return render(request, 'main/administration_client.html', {
        'title': 'Клиенты'
    })

def administration_order(request):
    return render(request, 'main/administration_order.html', {
        'title': 'Заказы'
    })