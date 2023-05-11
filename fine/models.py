from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


class EntertainmentType(models.IntegerChoices):
    """
    Типы интересов
    """
    SPORT = 0
    QUEST = 1
    GAME = 2
    FILM = 3


class User(AbstractUser):
    """
    Класс пользователя

    :param status: если честно хз :class:`django.contrib.auth.models.AbstractUser`
    """
    status = models.CharField(max_length=255)
    phone_number = models.CharField(null=True, max_length=20)
    avatar = models.ImageField(upload_to='images/', blank=True, null=True)
    events = models.ManyToManyField("Event")
    theme = models.CharField(max_length=255, default="white")


class UserSettings(models.Model):
    """
    Настройки пользователя
    """
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)


class Event(models.Model):
    """
    Класс ивента
    """
    name = models.CharField(max_length=255)

    class Type(models.IntegerChoices):
        """
        Закрыт или открыт ивент
        """
        CLOSE = 0
        OPEN = 1

    type = models.IntegerField(choices=Type.choices)
    address = models.CharField(max_length=255)
    status = models.BooleanField(default=True)  # False - Close, True - Active
    start_day = models.DateField()
    finish_day = models.DateField()
    description = models.CharField(max_length=255)
    entertainment_type = models.IntegerField(choices=EntertainmentType.choices)
    author = models.ForeignKey(get_user_model(), models.CASCADE)


class Interests(models.Model):
    """
    Интересы у пользователя
    """
    interest = models.IntegerField(choices=EntertainmentType.choices)
    user = models.ForeignKey(get_user_model(), models.CASCADE)


class RegistrationEvents(models.Model):
    """
    Класс регистрации на ивент
    """
    event = models.ForeignKey(Event, models.CASCADE)
    user = models.ForeignKey(get_user_model(), models.CASCADE)


class Report(models.Model):
    """
    Класс репорта
    """

    class Type(models.IntegerChoices):
        """
        Закрыт репорт или нет
        """
        WAITING = 1
        CLOSE = 2

    author = models.ForeignKey(get_user_model(), models.CASCADE)
    report_text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    closed_at = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(choices=Type.choices)


class Friends(models.Model):
    """
    Запрос на друзья
    """
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='who_send')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='who_receive')
    waiting = models.BooleanField()


class UserGroups(models.Model):
    """
    Пользовательские группы
    """
    title = models.CharField(max_length=15)
    description = models.CharField(max_length=255)
    founder = models.ForeignKey(get_user_model(), models.CASCADE, related_name='founder')
    members = models.ManyToManyField(get_user_model(), related_name='members')
