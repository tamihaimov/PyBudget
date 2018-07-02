from django.urls import path

from . import views

app_name = 'budgetApp'

urlpatterns = [
    # ex: /budgetApp/
    path('', views.login, name='login'),
    # ex: /budgetApp/555
    path('<int:user_id>/', views.welcome, name='welcome'),
    # ex: /budgetApp/555/settings/
    path('<int:user_id>/settings', views.userSettings, name='userSettings'),
    # ex: /budgetApp/account/1515/
    path('account/<int:user_account_id>/', views.accountSettings, name='accountSettings'),
    # ex: /budgetApp/transaction/1515/
    path('transaction/<int:user_account_id>/', views.transaction, name='transaction'),
    # ex: /budgetApp/history/1515/
    path('history/<int:user_account_id>/', views.history, name='history'),
    # ex: /budgetApp/statistics/1515/
    path('statistics/<int:user_account_id>/', views.statistics, name='statistics'),
    # ex: /budgetApp/scheduled/1515/
    path('scheduled/<int:user_account_id>/', views.scheduledTransactions, name='scheduled'),
]