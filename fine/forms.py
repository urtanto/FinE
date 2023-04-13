from django import forms
from django.forms import FileInput, TextInput

from fine.models import User, Event
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class RegistrationForm(UserCreationForm):
    """
    Форма регистрации
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CreateEvent(ModelForm):
    """
    Форма создания ивента
    """
    class Meta:
        model = Event
        fields = ['name', 'type', 'address', 'start_day', 'finish_day', 'description', 'entertainment_type']

class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'avatar']

class InterestsForm(forms.Form):
    OPTIONS = ((0, 'Спорт'),
        (1, 'Квесты'),
        (2, 'Видеоигры'),
        (3, 'Фильмы'))

    Interests = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)