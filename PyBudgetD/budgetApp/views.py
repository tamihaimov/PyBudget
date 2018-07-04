from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render

# Create your views here.
def welcome(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    default_account = UserAccounts.objects.filter(userID=user_id, isDefault=True)
    context = {'user': user, 'default_account': default_account}
    return render(request, 'budgetApp/welcome.html', context)


def userSettings(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    accounts = user.useraccounts_set.order_by('-isDefault')
    default_account = accounts.first()
    context = {'user': user, 'default_account': default_account, 'accounts': accounts}
    return render(request, 'budgetApp/user-settings.html', context)


def accountSettings(request, user_account_id):
    user_account = get_object_or_404(UserAccounts, pk=user_account_id)
    envelopes = user_account.accountID.envelopes_set.all()
    other_users = UserAccounts.objects.filter(accountID=user_account.accountID).exclude(id=user_account_id)
    context = {'user_account': user_account, 'envelopes': envelopes, 'other_users': other_users}
    return render(request, 'budgetApp/account-settings.html', context)


def transaction(request, user_account_id):
    user_account = get_object_or_404(UserAccounts, pk=user_account_id)
    envelopes = user_account.accountID.envelopes_set.all()
    other_users = UserAccounts.objects.filter(accountID=user_account.accountID).exclude(id=user_account_id)
    context = {'user_account': user_account, 'envelopes': envelopes, 'other_users': other_users}
    return render(request, 'budgetApp/transaction.html', context)


def addTransaction(request, user_account_id):
    user_account = get_object_or_404(UserAccounts, pk=user_account_id)
    try:
        envelope = user_account.accountID.envelopes_set.get(pk=request.POST['envelope'])
    except {KeyError, Envelopes.DoesNotExist}:
        return render(request, 'budgetApp/transaction.html', {
            'user_account': user_account,
            'error_message': "Invalid envelope"
        })
    else:
        transaction = ActivityLogs.objects.create(accountID=user_account.accountID, userID=user_account.userID,
                                                  envelopeID=envelope, date=request.POST['date'],
                                                  type=int(request.POST['type']), description=request.POST['description'],
                                                  sum=float(request.POST['sum']), comments=request.POST['comment'])
        if transaction:
            if transaction.type == 1:
                envelope.currentSum -= transaction.sum
            else:
                envelope.currentSum += transaction.sum
            envelope.save()
    return HttpResponseRedirect(reverse('budgetApp:welcome', args=(user_account.userID_id,)))


def history(request, user_account_id):
    return HttpResponse("Got to history page. hurray!")


def statistics(request, user_account_id):
    return HttpResponse("Got to statistics page. hurray!")


def login(request):
    return HttpResponse("Got to login page. hurray!")


def scheduledTransactions(request, user_account_id):
    return HttpResponse("Got to scheduled transactions page. hurray!")
