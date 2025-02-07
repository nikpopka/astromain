from django.db import models


class Services(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.CharField("Описание", max_length=1000, default="")
    price = models.IntegerField("Цена", default=0)


class Clients(models.Model):
    login = models.CharField("Имя пользователя", max_length=100)
    fio = models.CharField("ФИО", max_length=200, default='')



class Orders(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)


class Video(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    video_name = models.CharField("Название", max_length=100, default='')
    src = models.CharField("Ссылка на видео", max_length=1000, default='')

class Files(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    file_name = models.CharField("Название", max_length=100, default='')
    src = models.CharField("Ссылка на файл", max_length=1000, default='')