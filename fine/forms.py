from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from fine.models import User, Event


class RegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CreateEvent(ModelForm):
    """
    Форма создания ивента.
    """

    class Meta:
        model = Event
        fields = ['name', 'type', 'address', 'start_day', 'finish_day', 'description', 'entertainment_type']


class EditProfile(forms.ModelForm):
    """
    Форма для изменения основных данных профиля пользователя.
    """

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'avatar']


class SearchFriends(forms.Form):
    """
    Форма для поиска друзей.
    """
    search = forms.CharField(max_length=255)


class InterestsForm(forms.Form):
    """
    Форма для изменения интересов пользователя.
    """
    OPTIONS = ((0, 'Спорт'),
               (1, 'Квесты'),
               (2, 'Видеоигры'),
               (3, 'Фильмы'))

    Interests = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)

class CreateGroup(forms.Form):
    """
    Форма для создания пользовательской группы
    """
    title = forms.CharField(max_length=15, label='Название группы', help_text='')
    description = forms.CharField(max_length=255, label='Описание группы', help_text='')
