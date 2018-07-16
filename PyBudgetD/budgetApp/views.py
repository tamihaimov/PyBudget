from django.http import HttpResponse
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.views.generic.edit import UpdateView, CreateView, DeleteView


# Landing page
@login_required
def welcome(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    default_account = UserAccount.objects.filter(user_id=user.id, is_default=True)
    context = {'user': user, 'default_account': default_account}
    return render(request, 'budgetApp/welcome.html', context)


# Authentication views
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user_name, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('budget:welcome'))
    else:
        form = SignUpForm()
    return render(request, 'budgetApp/form.html', {'form': form, 'header': 'Sign Up'})


def logout_view(request):
    logout(request)
    return  HttpResponseRedirect(reverse('budget:welcome'))


# User settings main view and actions
@login_required
def user_settings(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save()
            user_account = UserAccount()
            user_account.user = request.user
            user_account.account = new_account
            user_account.permission = Permission.objects.filter(name='owner').first()
            default_account = UserAccount.objects.filter(user=request.user, is_default=1).first()
            if default_account is None:
                user_account.is_default = 1
            user_account.save()
        return HttpResponseRedirect(reverse('budget:user_settings'))
    user = request.user
    accounts = user.useraccount_set.order_by('-is_default')
    default_account = accounts.first()
    context = {'user': user, 'default_account': default_account, 'accounts': accounts}
    return render(request, 'budgetApp/user-settings.html', context)


class ChangeUserInfo(UpdateView):
    model = User
    template_name = 'budgetApp/form.html'
    success_url = reverse_lazy('budget:user_settings')
    form_class = ChangeUserInfoForm

    def get_object(self, queryset=None):
        '''This method will load the object
           that will be used to load the form
           that will be edited'''
        return self.request.user


# Account settings and actions view
class ChangeAccountInfo (UpdateView):
    model = Account
    template_name = 'budgetApp/form.html'
    form_class = AccountForm

    def get_success_url(self):
        user_account = UserAccount.objects.filter(user=self.request.user, account_id=self.kwargs['pk']).first()
        return reverse('budget:account_settings', kwargs={'user_account_id': user_account.id})


class ChangeEnvelopeInfo (UpdateView):
    model = Envelope
    template_name = 'budgetApp/form.html'
    form_class = EnvelopeForm

    def get_success_url(self):
        user_account = UserAccount.objects.filter(user=self.request.user, account_id=self.object.account_id).first()
        return reverse('budget:account_settings', kwargs={'user_account_id': user_account.id})


class ChangeUserAccountInfo (UpdateView):
    model = UserAccount
    template_name = 'budgetApp/form.html'
    form_class = UserAccountForm

    def get_success_url(self):
        user_account = UserAccount.objects.filter(user=self.request.user, account_id=self.object.account_id).first()
        return reverse('budget:account_settings', kwargs={'user_account_id': user_account.id})


class AddEnvelope (CreateView):
    form_class = AddEnvelopeForm
    template_name = 'budgetApp/form.html'

    def get_success_url(self):
        user_account = UserAccount.objects.filter(user=self.request.user, account_id=self.object.account_id).first()
        return reverse('budget:account_settings', kwargs={'user_account_id': user_account.id})

    def get_initial(self):
        account = get_object_or_404(Account, pk=self.kwargs.pop('account_id'))
        return {
            'account': account,
            'id_account': account.id,
            'current_sum': 0
        }


class DeleteEnvelope (DeleteView):
    model = Envelope
    template_name = 'budgetApp/delete-form.html'

    def get_success_url(self):
        user_account = UserAccount.objects.filter(user=self.request.user, account_id=self.object.account_id).first()
        return reverse('budget:account_settings', kwargs={'user_account_id': user_account.id})

    def get_context_data(self, **kwargs):
        context = super(DeleteEnvelope, self).get_context_data()
        context['object_type'] = 'Envelope'
        return context


@login_required
def account_view(request, user_account_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_account = get_object_or_404(UserAccount, pk=user_account_id)
    context = {'user_account': user_account}
    return render(request, 'budgetApp/account-view.html', context)


@login_required
def account_settings(request, user_account_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_account = get_object_or_404(UserAccount, pk=user_account_id)
    envelopes = user_account.account.envelope_set.all()
    other_users = UserAccount.objects.filter(account=user_account.account).exclude(id=user_account_id)
    context = {'user_account': user_account, 'envelopes': envelopes, 'other_users': other_users}
    return render(request, 'budgetApp/account-settings.html', context)


@login_required
def transaction(request, user_account_id):
    user_account = get_object_or_404(UserAccount, pk=user_account_id)
    envelopes = user_account.account.envelope_set.all()
    other_users = UserAccount.objects.filter(account=user_account.account).exclude(id=user_account_id)
    context = {'user_account': user_account, 'envelopes': envelopes, 'other_users': other_users}
    return render(request, 'budgetApp/transaction.html', context)


@login_required
def add_transaction(request, user_account_id):
    user_account = get_object_or_404(UserAccount, pk=user_account_id)
    try:
        envelope = user_account.account.envelope_set.get(pk=request.POST['envelope'])
    except {KeyError, Envelope.DoesNotExist}:
        return render(request, 'budgetApp/transaction.html', {
            'user_account': user_account,
            'error_message': "Invalid envelope"
        })
    else:
        transaction = Transaction.objects.create(account=user_account.account, user=user_account.user,
                                                 envelope=envelope, date=request.POST['date'],
                                                 type=int(request.POST['type']), description=request.POST['description'],
                                                 sum=float(request.POST['sum']), comments=request.POST['comment'])
        if transaction:
            if transaction.type == 1:
                envelope.current_sum -= transaction.sum
            else:
                envelope.current_sum += transaction.sum
            envelope.save()
    return HttpResponseRedirect(reverse('budget:welcome'))


@login_required
def history(request, user_account_id):
    user_account = get_object_or_404(UserAccount, pk=user_account_id)
    transactions = user_account.account.transaction_set.order_by('date').all()
    context = {'user_account': user_account, 'transactions': transactions}
    return render(request, 'budgetApp/history.html', context)


@login_required
def statistics(request, user_account_id):
    return HttpResponse("Got to statistics page. hurray!")


def scheduled_transactions(request, user_account_id):
    return HttpResponse("Got to scheduled transactions page. hurray!")
