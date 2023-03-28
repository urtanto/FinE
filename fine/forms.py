from django import forms
from fine.models import User

class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'avatar']