from django.http import HttpResponse
from .models import *
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
    return HttpResponse("Got to account settings page. hurray!")


def transaction(request, user_account_id):
    return HttpResponse("Got to transaction page. hurray!")


def history(request, user_account_id):
    return HttpResponse("Got to history page. hurray!")


def statistics(request, user_account_id):
    return HttpResponse("Got to statistics page. hurray!")


def login(request):
    return HttpResponse("Got to login page. hurray!")


def scheduledTransactions(request, user_account_id):
    return HttpResponse("Got to scheduled transactions page. hurray!")
