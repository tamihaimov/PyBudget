from django.urls import path, include
from . import views

app_name = 'budget'


# Main windows
urlpatterns = [
    # ex: /budget/
    path('', views.welcome, name='welcome'),
    path('welcome/', views.welcome, name='welcome'),
    # ex: /budget/settings/
    path('settings/', views.user_settings, name='user_settings'),
    # ex: /budget/account/1515/
    path('account/<int:user_account_id>/', views.account_view, name='account_view'),
    # ex: /budget/account/1515/settings
    path('account/<int:user_account_id>/settings/', views.account_settings, name='account_settings'),
    # ex: /budget/transaction/1515/
    path('transaction/<int:user_account_id>/', views.transaction, name='transaction'),
    # ex: /budget/history/1515/
    path('history/<int:user_account_id>/', views.history, name='history'),
    # ex: /budget/statistics/1515/
    path('statistics/<int:user_account_id>/', views.statistics, name='statistics'),
    # ex: /budget/scheduled/1515/
    path('scheduled/<int:user_account_id>/', views.scheduled_transactions, name='scheduled'),
]

# Actions
urlpatterns += [
    # ex: /budget/sign_up/
    path('sign_up/', views.sign_up, name='sign_up'),
    # ex: /budget/change-user-info/
    path('change-user-info/', views.ChangeUserInfo.as_view(), name='change_user_info'),
    # ex: /budget/change-account-info/1515
    path('change-account-info/<int:pk>', views.ChangeAccountInfo.as_view(), name='change_account_info'),
    # ex: /budget/change-envelope-info/1515
    path('change-envelope-info/<int:pk>', views.ChangeEnvelopeInfo.as_view(), name='change_envelope_info'),
    # ex: /budget/add-envelope/1515
    path('add-envelope/<int:account_id>', views.AddEnvelope.as_view(), name='add-envelope'),
    # ex: /budget/delete-envelope/1515
    path('delete-envelope/<int:pk>', views.DeleteEnvelope.as_view(), name='delete-envelope'),
    # ex: /budget/transaction/1515/
    path('addTransaction/<int:user_account_id>/', views.add_transaction, name='add_transaction'),
]


# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    # ex: /budgetApp/logout
    path('logout/', views.logout_view, name='log-out'),
    # ex: /budgetApp/auth
    path('auth/', include('django.contrib.auth.urls')),

]