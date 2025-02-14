import requests
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import permission_required, login_required
from .models import Services, Clients, Questions, Video, Files, Answers, Comments, Links
from django.template.defaultfilters import register
from dotenv import load_dotenv
import os


main_user = "popov"

@register.filter(name='get_attr')
def get_attr(dictionary, key):
    try:
        res = dictionary[key]
    except:
        res = ''
    return res


def index(request):
    all_services = Services.objects.all()
    vk_link = Links.objects.get(name="vkcom").link
    youtube_link = Links.objects.get(name="youtube").link
    rutube_link = Links.objects.get(name="rutube").link
    telegram_link = Links.objects.get(name="telegram").link
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
        'vk_link': vk_link,
        'youtube_link': youtube_link,
        'rutube_link': rutube_link,
        'telegram_link': telegram_link,

    })


def services(request):
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
                return redirect('services')
    return render(request, 'main/services.html', {
        'all_services': all_services,
        'form_auth': form_auth
    })


def sent_message(request):
    message_text = 'test2'

    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message_text
    }
    requests.post(send_message_url, data=payload)

    return redirect('main')


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


def comments(request):
    comments = Comments.objects.all().order_by('-id')
    if request.user.is_authenticated:
        client = Clients.objects.get(login=request.user.username)
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
                return redirect('comments')
        if request.user.is_authenticated:
            new_comment = request.POST.get('new_comment')
            if new_comment != "Ваш текст...":
                new_comment_obj = Comments(comment=new_comment, client=client)
                new_comment_obj.save()
                return redirect('comments')
            else: return redirect('comments')

    return render(request, 'main/comments.html', {
        'title': 'Комментарии',
        'comments': comments,
        'form_auth': form_auth,
    })


def anketa(request):
    questions = Questions.objects.all()
    client = Clients.objects.get(login=request.user.username)
    answers = Answers.objects.filter(client=client)
    dict_answers = {}


    if request.method == "POST":
        for question in questions:
            answer = request.POST.get(f"{question.id}")
            if Answers.objects.filter(client=client, question=question).exists():
                new_answer = Answers.objects.get(client=client, question=question)
                new_answer.answer = answer
                new_answer.save()

            else:
                new_answer = Answers(
                    client=client,
                    question=question,
                    answer=answer
                )
                new_answer.save()

    for i in answers:
        dict_answers[i.question.id] = i.answer

    return render(request, 'main/anketa.html', {
        'title': 'Анкета',
        'questions': questions,
        'answers': answers,
        'dict_answers': dict_answers,
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


def administration_anketa(request):
    questions = Questions.objects.all()

    if request.method == 'POST':
        new_question = request.POST.get('new_question')
        new_question_obj = Questions(question=new_question)
        new_question_obj.save()

    return render(request, 'main/administration_anketa.html', {
        'title': 'Анкета',
        'questions': questions,
    })


def edit_question(request, id):
    question = Questions.objects.get(id=id)
    if request.method == 'POST':
        new_question = request.POST.get('new_text_question')
        question.question = new_question
        question.save()
        return redirect('administration_anketa')
    return render(request, 'main/administration_question.html', {
        'title': 'Редактирование вопроса',
        'question': question,
    })


def delete_question(request, id):
    question = Questions.objects.get(id=id)
    question.delete()
    return redirect('administration_anketa')


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


def administration_links(request):
    links = Links.objects.all()

    if request.method == 'POST':
        for link in links:
            new_link = request.POST.get(f"link_{link.id}")
            print(new_link)
            link.link = new_link
            link.save()
            return redirect('administration_links')

    return render(request, 'main/administration_links.html', {
        'title': 'Ссылки',
        'links': links,
    })


def administration_promotions(request):

    return render(request, 'main/administration_promotions.html', {
        'title': 'Акции',
    })


def administration_comments(request):
    return render(request, 'main/administration_comments.html', {
        'title': 'Комментарии',
    })


def edit_client(request, id):
    client = Clients.objects.get(id=id)
    video_list = Video.objects.filter(client=client)
    files = Files.objects.filter(client=client)
    anketa_list = Answers.objects.filter(client=client)
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
        'anketa_list': anketa_list,
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


def administration_about(request):
    return render(request, 'main/administration_about.html', {
        'title': 'Заказы'
    })


def administration_comments(request):
    all_comments = Comments.objects.all().order_by('-id')
    return render(request, 'main/administration_comments.html', {
        'title': 'Комментарии',
        'all_comments': all_comments,
    })

def delete_comment(request, id):
    item = Comments.objects.get(id=id)
    item.delete()
    return redirect('/administration_comments')