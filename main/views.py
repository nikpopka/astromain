from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import permission_required
from . models import Services, Clients, Orders, Video, Files

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
                return redirect('personal_account')
            else:
                return redirect('main')


    return render(request, 'main/index.html', {
        'title': 'Ведическая астрология',
        'all_services': all_services,
        'form_auth': form_auth,
    })


def personal_account(request):
    if request.user.is_authenticated:
        username = request.user.username
        client = Clients.objects.get(login=username)
        video_list = Video.objects.filter(client=client)
        files = Files.objects.filter(client=client)
        return render(request, 'main/lk.html', {
            'title': 'Личный кабинет',
            'client': client,
            'video_list': video_list,
            'files': files,
        })
    return render(request, 'main/lk.html', {
        'title': 'Личный кабинет',
    })


def anketa(request):
    return render(request, 'main/anketa.html', {
        'title': 'Анкета',
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

    clients = Clients.objects.all()

    if request.method == "POST":
        fio = request.POST.get('fio')
        log = request.POST.get('login')
        passw = request.POST.get('passw')

        new_user = User.objects.create_user(
            username=log,
            password=passw
        )

        new_client = Clients(login=log,
                             fio=fio)
        new_client.save()


    return render(request, 'main/administration_client.html', {
        'title': 'Клиенты',
        'clients': clients,
    })

def edit_client(request, id):
    client = Clients.objects.get(id=id)
    video_list = Video.objects.filter(client=client)
    files = Files.objects.filter(client=client)
    if request.method == "POST":
        new_video_name = request.POST.get('new_video_name')
        new_file_name = request.POST.get('new_file_name')

        if new_video_name is not None:
            new_video_src = request.POST.get('new_video_src')
            new_video = Video(client=client, video_name=new_video_name, src=new_video_src)
            new_video.save()

        if new_file_name  is not None:
            new_file_src = request.POST.get('new_file_src')
            new_file = Files(client=client, file_name=new_file_name, src=new_file_src)
            new_file.save()

    return render(request, 'main/administration_client_edit.html', {
        'title': client.fio,
        'client': client,
        'video_list': video_list,
        'files': files,
    })

def delete_video(request, id):
    video = Video.objects.get(id=id)
    client = Clients.objects.get(id=video.client.id)
    video_list = Video.objects.filter(client=client)
    files = Files.objects.filter(client=client)
    video.delete()
    return redirect(f'/edit_client/{client.id}', {
        'title': client.fio,
        'client': client,
        'video_list': video_list,
        'files': files,
    })


def delete_file(request, id):
    File = Files.objects.get(id=id)
    client = Clients.objects.get(id=File.client.id)
    video_list = Video.objects.filter(client=client)
    files = Files.objects.filter(client=client)
    File.delete()
    return redirect(f'/edit_client/{client.id}', {
        'title': client.fio,
        'client': client,
        'video_list': video_list,
        'files': files,
    })


def administration_order(request):
    return render(request, 'main/administration_order.html', {
        'title': 'Заказы'
    })