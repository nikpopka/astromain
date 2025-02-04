from django.db import models


class Services(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.CharField("Описание", max_length=1000, default="")
    price = models.IntegerField("Цена", default=0)


class Clients(models.Model):
    login = models.CharField("Имя пользователя", max_length=100)
    fio = models.CharField("ФИО", max_length=200)
    video = models.CharField("Ссылка на видео", max_length=100)