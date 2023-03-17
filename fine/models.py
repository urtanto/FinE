from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Класс пользователя

    :param status: если честно хз :class:`django.contrib.auth.models.AbstractUser`
    """
    status = models.CharField(max_length=255)
