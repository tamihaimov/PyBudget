from django import forms
from .models import Users


class UserForm(forms.ModelForm):
    userPass = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('userName', 'userPass', 'firstName', 'lastName')
