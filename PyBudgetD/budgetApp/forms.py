from django import forms
from .models import User


class UserForm(forms.ModelForm):
    userPass = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('userName', 'userPass', 'firstName', 'lastName')
