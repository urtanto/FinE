from django import forms
from fine.models import User

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