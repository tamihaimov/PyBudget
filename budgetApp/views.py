from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import *


# Landing page
@login_required
def welcome(request):
    default_budget = UserBudget.objects.filter(user_id=request.user.id,
                                               is_default=True,
                                               budget__is_inactive=False).first()
    if default_budget is not None:
        default_budget.reset_user_budgets()  # Check if any of the users budget accounts needs to be reset
    context = {'user': request.user, 'user_budget': default_budget}
    return render(request, 'budgetApp/welcome.html', context)


# User settings - view and actions
@login_required
def user_settings(request):
    if request.method == 'POST':
        form = BudgetAccountForm(request.POST)
        if form.is_valid():
            new_budget = form.save()
            user_budget = UserBudget.objects.create(user=request.user, budget=new_budget,
                                                    permission=UserBudget.PERMISSION_OWNER)
            user_budget.check_and_set_default()
        return HttpResponseRedirect(reverse('budget:user_settings'))
    user_budgets = request.user.userbudget_set.order_by('-is_default')
    default_account = user_budgets.first()
    context = {'user': request.user, 'default_account': default_account, 'user_budgets': user_budgets}
    return render(request, 'budgetApp/user-settings.html', context)


class ChangeUserInfo(UpdateView):
    model = User
    template_name = 'budgetApp/form.html'
    success_url = reverse_lazy('budget:user_settings')
    form_class = ChangeUserInfoForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ChangeUserInfo, self).get_context_data()
        context['header'] = 'Change User Info'
        return context


# BudgetAccount settings and actions views
@login_required
def budget_settings(request, user_budget_id):
    user_budget = get_object_or_404(UserBudget, pk=user_budget_id)
    envelopes = user_budget.budget.envelope_set.exclude(is_inactive=True).all()
    other_users = UserBudget.objects.filter(budget=user_budget.budget).exclude(id=user_budget_id)
    context = {'user_budget': user_budget, 'envelopes': envelopes, 'other_users': other_users}
    return render(request, 'budgetApp/account-settings.html', context)


class BaseChangeInfo (UpdateView):
    template_name = 'budgetApp/form.html'

    def get_success_url(self):
        user_budget = UserBudget.objects.filter(user=self.request.user, budget_id=self.get_budget_id()).first()
        return reverse('budget:budget_settings', kwargs={'user_budget_id': user_budget.id})

    def form_type(self):
        return 'Base'

    def get_context_data(self, **kwargs):
        context = super(BaseChangeInfo, self).get_context_data()
        context['header'] = 'Change ' + self.form_type() + ' Info'
        return context

    def get_budget_id(self):
        return self.kwargs['pk']


class ChangeBudgetInfo (BaseChangeInfo):
    model = BudgetAccount
    form_class = BudgetAccountForm

    def form_type(self):
        return 'Budget'


class ChangeEnvelopeInfo (BaseChangeInfo):
    model = Envelope
    form_class = EnvelopeForm

    def form_type(self):
        return 'Envelope'

    def get_budget_id(self):
        return self.object.account_id


class ChangeUserBudgetInfo (BaseChangeInfo):
    model = UserBudget
    form_class = UserBudgetForm

    def form_type(self):
        return 'User Budget'


class AddEnvelope (CreateView):
    form_class = AddEnvelopeForm
    template_name = 'budgetApp/form.html'

    def get_success_url(self):
        user_account = UserBudget.objects.filter(user=self.request.user, budget_id=self.object.account_id).first()
        return reverse('budget:budget_settings', kwargs={'user_budget_id': user_account.id})

    def get_initial(self):
        account = get_object_or_404(BudgetAccount, pk=self.kwargs.pop('budget_id'))
        return {
            'account': account,
            'id_account': account.id,
            'current_sum': 0
        }

    def get_context_data(self, **kwargs):
        context = super(AddEnvelope, self).get_context_data()
        context['header'] = 'Add Envelope'
        return context


class DeleteEnvelope (DeleteView):
    model = Envelope
    template_name = 'budgetApp/delete-form.html'

    def get_success_url(self):
        user_budget = UserBudget.objects.filter(user=self.request.user, budget_id=self.object.account_id).first()
        return reverse('budget:budget_settings', kwargs={'user_budget_id': user_budget.id})

    def get_context_data(self, **kwargs):
        context = super(DeleteEnvelope, self).get_context_data()
        context['object_type'] = 'Envelope'
        return context


# BudgetAccount views
@login_required
def budget_view(request, user_budget_id):
    user_account = get_object_or_404(UserBudget, pk=user_budget_id)
    context = {'user_account': user_account}
    return render(request, 'budgetApp/account-view.html', context)


@login_required
def history(request, user_budget_id):
    user_budget = get_object_or_404(UserBudget, pk=user_budget_id)
    transactions = user_budget.budget.transaction_set.order_by('date').all()
    context = {'user_budget': user_budget, 'transactions': transactions}
    return render(request, 'budgetApp/history.html', context)


@login_required
def statistics(request, user_budget_id):  # TODO: activate this feature
    user_budget = get_object_or_404(UserBudget, pk=user_budget_id)
    return HttpResponse("Got to statistics page. hurray!")


@login_required
def scheduled_transactions(request, user_account_id):  # TODO: activate this feature
    return HttpResponse("Got to scheduled transactions page. hurray!")


# BudgetAccount actions
class AddTransaction (CreateView):
    form_class = AddTransactionForm
    template_name = 'budgetApp/form.html'

    def get_success_url(self):
        return reverse('budget:welcome')

    def get_initial(self):
        budget = get_object_or_404(BudgetAccount, pk=self.kwargs['budget_id'])
        return {
            'budget': budget,
            'id_budget': int(self.kwargs['budget_id']),
            'user': self.request.user,
            'id_user': self.request.user.id,
            'sum': 0
        }

    def get_context_data(self, **kwargs):
        context = super(AddTransaction, self).get_context_data()
        budget = get_object_or_404(BudgetAccount, pk=self.kwargs['budget_id'])
        context['header'] = 'Add Transaction To ' + budget.name
        return context


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
    return HttpResponseRedirect(reverse('budget:welcome'))
