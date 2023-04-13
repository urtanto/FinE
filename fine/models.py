from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


class EntertainmentType(models.IntegerChoices):
    Sport = 0
    Quest = 1
    Game = 2
    Film = 3


class User(AbstractUser):
    """
    Класс пользователя

    :param status: если честно хз :class:`django.contrib.auth.models.AbstractUser`
    """
    status = models.CharField(max_length=255)
    phone_number = models.CharField(null=True, max_length=20)
    avatar = models.ImageField(upload_to='images/', blank=True, null=True)


class UserSettings(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)


class Event(models.Model):
    name = models.CharField(max_length=255)

    class Type(models.IntegerChoices):
        Close = 0
        Open = 1

    type = models.IntegerField(choices=Type.choices)
    address = models.CharField(max_length=255)
    status = models.BooleanField(default=True)  # False - Close, True - Active
    start_day = models.DateField()
    finish_day = models.DateField()
    description = models.CharField(max_length=255)
    entertainment_type = models.IntegerField(choices=EntertainmentType.choices)
    author = models.ForeignKey(get_user_model(), models.CASCADE)


class Interests(models.Model):
    interest = models.IntegerField(choices=EntertainmentType.choices)
    user = models.ForeignKey(get_user_model(), models.CASCADE)


class RegistrationEvents(models.Model):
    event = models.ForeignKey(Event, models.CASCADE)
    user = models.ForeignKey(get_user_model(), models.CASCADE)


class Report(models.Model):
    class Type(models.IntegerChoices):
        Waiting = 1
        Close = 2

    author = models.ForeignKey(get_user_model(), models.CASCADE)
    report_text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    closed_at = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(choices=Type.choices)
