from django.http import HttpResponse
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate
from django.conf import settings


# Create your views here.
@login_required
def welcome(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    default_account = UserAccount.objects.filter(user_id=user.id, is_default=True)
    context = {'user': user, 'default_account': default_account}
    return render(request, 'budgetApp/welcome.html', context)


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


@login_required
def user_settings(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    accounts = user.useraccount_set.order_by('-is_default')
    default_account = accounts.first()
    context = {'user': user, 'default_account': default_account, 'accounts': accounts}
    return render(request, 'budgetApp/user-settings.html', context)


@login_required
def change_user_info(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('budget:user_settings'))
    else:
        form = UserChangeForm()
    return render(request, 'budgetApp/form.html', {'form': form, 'header': 'Change User Info'})


@login_required
def account_settings(request, user_account_id):
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
        transaction = Transaction.objects.create(account=user_account.account, user=user_account.user_id,
                                                 envelope=envelope, date=request.POST['date'],
                                                 type=int(request.POST['type']), description=request.POST['description'],
                                                 sum=float(request.POST['sum']), comments=request.POST['comment'])
        if transaction:
            if transaction.type == 1:
                envelope.currentSum -= transaction.sum
            else:
                envelope.currentSum += transaction.sum
            envelope.save()
    return HttpResponseRedirect(reverse('budget:welcome', args=(user_account.user_id,)))


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
