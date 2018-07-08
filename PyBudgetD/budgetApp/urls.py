from django.urls import path, include
from . import views

app_name = 'budget'

urlpatterns = [
    # ex: /budget/
    path('', views.welcome, name='welcome'),
    # ex: /budget/
    path('sign_up/', views.sign_up, name='sign_up'),
    # # ex: /budget/555
    # path('<int:user_id>/', views.welcome, name='welcome'),
    # ex: /budget/555/settings/
    path('<int:user_id>/settings/', views.user_settings, name='user_settings'),
    # ex: /budget/account/1515/
    path('account/<int:user_account_id>/', views.account_settings, name='account_settings'),
    # ex: /budget/transaction/1515/
    path('transaction/<int:user_account_id>/', views.transaction, name='transaction'),
    # ex: /budget/transaction/1515/
    path('addTransaction/<int:user_account_id>/', views.add_transaction, name='add_transaction'),
    # ex: /budget/history/1515/
    path('history/<int:user_account_id>/', views.history, name='history'),
    # ex: /budget/statistics/1515/
    path('statistics/<int:user_account_id>/', views.statistics, name='statistics'),
    # ex: /budget/scheduled/1515/
    path('scheduled/<int:user_account_id>/', views.scheduled_transactions, name='scheduled'),
]


# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    # ex: /budgetApp/auth
    path('auth/', include('django.contrib.auth.urls')),
]