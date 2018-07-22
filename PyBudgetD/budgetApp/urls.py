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
    path('account/<int:user_budget_id>/', views.budget_view, name='budget_view'),
    # ex: /budget/account/1515/settings
    path('account/<int:user_budget_id>/settings/', views.budget_settings, name='budget_settings'),
    # ex: /budget/history/1515/
    path('history/<int:user_budget_id>/', views.history, name='history'),
    # ex: /budget/statistics/1515/
    path('statistics/<int:user_budget_id>/', views.statistics, name='statistics'),
    # ex: /budget/scheduled/1515/
    path('scheduled/<int:user_budget_id>/', views.scheduled_transactions, name='scheduled'),
]

# Actions
urlpatterns += [
    # ex: /budget/sign_up/
    path('sign_up/', views.sign_up, name='sign_up'),
    # ex: /budget/change-user-info/
    path('change-user-info/', views.ChangeUserInfo.as_view(), name='change_user_info'),
    # ex: /budget/change-budget-info/1515
    path('change-budget-info/<int:pk>', views.ChangeBudgetInfo.as_view(), name='change_budget_info'),
    # ex: /budget/change-envelope-info/1515
    path('change-envelope-info/<int:pk>', views.ChangeEnvelopeInfo.as_view(), name='change_envelope_info'),
    # ex: /budget/add-envelope/1515
    path('add-envelope/<int:budget_id>', views.AddEnvelope.as_view(), name='add-envelope'),
    # ex: /budget/delete-envelope/1515
    path('delete-envelope/<int:pk>', views.DeleteEnvelope.as_view(), name='delete-envelope'),
    # ex: /budget/add-transaction/1515/
    path('add-transaction/<int:budget_id>/', views.AddTransaction.as_view(), name='add-transaction'),
]


# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    # ex: /budgetApp/logout
    path('logout/', views.logout_view, name='log-out'),
    # ex: /budgetApp/auth
    path('auth/', include('django.contrib.auth.urls')),

]