from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms
from django.forms import modelform_factory
from .models import *
from datetime import datetime
from django.core import exceptions


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
        self.fields['account'].queryset = Account.objects.filter(pk=kwargs['initial']['id_account'])


class AddTransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=datetime.now())
    comments = forms.CharField(required=False)

    class Meta:
        model = Transaction
        fields = ('account', 'user', 'date', 'envelope', 'type', 'description', 'sum', 'comments')

    def __init__(self, *args, **kwargs):
        super(AddTransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(pk=kwargs['initial']['id_account'])
        self.fields['account'].widget = forms.HiddenInput()
        self.fields['user'].queryset = User.objects.filter(pk=kwargs['initial']['id_user'])
        self.fields['user'].widget = forms.HiddenInput()

    def save(self):
        transaction = super(AddTransactionForm, self).save()
        if transaction is not None:
            transaction.update_envelope()
        return transaction
    
    def is_valid(self):
        if super(AddTransactionForm, self).is_valid():
            if self.fields['type'] == Transaction.TYPE_INCOME:
                return True
            envelope = self.cleaned_data['envelope']
            transaction_sum = self.cleaned_data['sum']
            if transaction_sum <= 0:
                self.add_error('sum', exceptions.ValidationError)
                return False
            if envelope.check_sufficient_funds(transaction_sum):
                return True
            else:
                self.add_error('sum', exceptions.ValidationError)
        return False
        

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


TransactionForm = modelform_factory(Transaction, fields=('date', 'envelope', 'type', 'description', 'sum', 'comments'))
