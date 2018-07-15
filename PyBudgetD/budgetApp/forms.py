from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms
from django.forms import modelform_factory
from .models import *


# Creation Forms

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name', 'email',)
        field_classes = {'username': UsernameField}

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AddEnvelopeForm(forms.ModelForm):

    class Meta:
        model = Envelope
        fields = ('account', 'category', 'name', 'budget', 'current_sum')

    def __init__(self, *args, **kwargs):
        super(AddEnvelopeForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(pk= kwargs['initial']['id_account'])

# Change Forms


class ChangeUserInfoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ChangeAccountForm(forms.ModelForm):
    name = forms.CharField(max_length=400)
    budget = forms.IntegerField()
    reset_date = forms.IntegerField()

    class Meta:
        model = Account
        fields = ('name', 'budget', 'reset_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ChangeEnvelopeForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    budget = forms.IntegerField()

    class Meta:
        model = Account
        fields = ('name', 'budget')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# General Forms

AccountForm = modelform_factory(Account, fields=('name', 'budget', 'reset_date'))


EnvelopeForm = modelform_factory(Envelope, fields=('account', 'category', 'name', 'budget', 'current_sum'))


UserAccountForm = modelform_factory(UserAccount, fields=('user', 'account', 'permission', 'is_default'))
