from datetime import date
from calendar import monthrange
from dateutil import relativedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class BudgetAccount (models.Model):
    """ 
    This class represents a summary of the users' available funds,
    organized in separate envelopes.
    The budget account's total budget and balance are are
    the sum of those fields in the budget's envelopes.
    """
    name = models.CharField(max_length=400)
    reset_day = models.IntegerField()
    last_reset_date = models.DateField(default=timezone.now)
    is_inactive = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def calc_balance(self):
        envelopes = self.envelope_set.exclude(is_inactive=True).all()
        balance = 0
        for envelope in envelopes:
            balance += envelope.current_sum
        return balance
    balance = property(calc_balance)

    def calc_budget(self):
        envelopes = self.envelope_set.exclude(is_inactive=True).all()
        budget = 0
        for envelope in envelopes:
            budget += envelope.budget
        return budget
    budget = property(calc_budget)
    
    def calc_next_reset_date(self):
        reset_date = date.today()
        days_delta = self.reset_day - reset_date.day
        if reset_date.day > self.reset_day:
            reset_date += relativedelta.relativedelta(months=+1, day=self.reset_day)
        else:
            reset_date += days_delta
        return reset_date

    next_reset_date = property(calc_next_reset_date)

    def calc_countdown_to_reset(self):
        date_diff = self.calc_next_reset_date() - date.today()
        return date_diff.days

    countdown_to_reset = property(calc_countdown_to_reset)

    def get_envelopes(self):
        return self.envelope_set.exclude(is_inactive=True).all()

    envelopes = property(get_envelopes)

    def need_to_reset_budget(self):
        if date.today() == self.last_reset_date:
            return False
        elif date.today() == self.calc_next_reset_date():
            return True
        return False  # TODO: add conditions

    def reset_budget(self):
        if self.need_to_reset_budget() is False:
            return
        SavingsHistory.objects.create(budget=self, date=date.today(),
                                      saved_sum=self.calc_balance())
        for envelope in self.envelope_set.all():
            envelope.balance = envelope.budget
            envelope.save()
        self.last_reset_date = date.today()
        self.save()

    def set_inactive(self):
        self.is_inactive = True
        self.save()


class UserBudget (models.Model):
    """
    This class connects Django's User class to this application's BudgetAccount class.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(BudgetAccount, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return "BudgetId " + str(self.id)

    PERMISSION_OWNER = 1
    PERMISSION_USER = 2
    PERMISSION_VIEWER = 3
    PERMISSION_CHOICES = (
        (PERMISSION_OWNER, 'owner'),
        (PERMISSION_USER, 'user'),
        (PERMISSION_VIEWER, 'viewer')
    )

    permission = models.IntegerField(choices=PERMISSION_CHOICES)

    def permission_to_string(self):
        return self.get_permission_display()

    permission_str = property(permission_to_string)

    def reset_user_budgets(self):  # TODO: inherit from User and move this there
        """
        Find all user's budgets, check if they need to be reset and if so - reset.
        Since the budget is reset each month, the calculation compares the days from last
        login to the amount of days in that month.
        """
        days_from_login = date.today() - self.user.last_login.date()
        user_accounts = UserBudget.objects.filter(user=self.user, budget__is_inactive=False).all()
        for curr_user_account in user_accounts:
            last_reset_month = curr_user_account.budget.last_reset_date.month
            last_reset_year = curr_user_account.budget.last_reset_date.year
            dummy, days_in_last_reset_month = monthrange(last_reset_year, last_reset_month)
            if days_from_login.days >= days_in_last_reset_month:
                curr_user_account.budget.reset_budget()

    def check_and_set_default(self):
        """ Check if any budget is set default for this user. If not, set the current budget as default. """
        any_default_account = UserBudget.objects.filter(user=self.user, is_default=1).first()
        if any_default_account is None:
            self.is_default = True
            self.save()


class Envelope (models.Model):
    """
    This class represents a virtual compartment
    containing funds that were allocated for a certain type of purpose.
    The Envelope's purpose is represented by its name (Bills, Gas, etc)
    and its category.
    Each envelope contains an initial budget, and a balance field.
    Every month, the envelope balance is reset to its budget value,
    and is updated during the month with each reported transaction.
    """
    account = models.ForeignKey(BudgetAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    budget = models.IntegerField()
    current_sum = models.FloatField()
    is_inactive = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    CATEGORY_FOOD = 1
    CATEGORY_BILLS = 2
    CATEGORY_TRANSPORT = 3
    CATEGORY_HOUSING = 4
    CATEGORY_HEALTH_CARE = 5
    CATEGORY_SAVINGS = 6
    CATEGORY_ENTERTAINMENT = 7
    CATEGORY_MISC = 8
    CATEGORY_CHOICES = (
        (CATEGORY_FOOD, 'Food and Dining'),
        (CATEGORY_BILLS, 'Bills and Utilities'),
        (CATEGORY_TRANSPORT, 'Auto and Transportation'),
        (CATEGORY_HOUSING, 'Housing'),
        (CATEGORY_HEALTH_CARE, 'HealthCare'),
        (CATEGORY_SAVINGS, 'Savings'),
        (CATEGORY_ENTERTAINMENT, 'Entertainment'),
        (CATEGORY_MISC, 'Miscellaneous'),
    )

    category = models.IntegerField(choices=CATEGORY_CHOICES, default=CATEGORY_MISC)

    def check_sufficient_funds(self, transaction_sum):
        return self.current_sum >= transaction_sum

    def set_inactive(self):
        self.is_inactive = True
        self.save()

    def delete(self):
        self.set_inactive()

    def hard_delete(self):  # This is the actual delete
        super.delete()


class Transaction (models.Model):
    """
    This class represents logging a transaction made by an authorized user
    in a certain account.
    Adding a transaction both updates the current balance of the relevant budget account and envelope,
    and logs the action, for tracking purposes.
    """
    budget = models.ForeignKey(BudgetAccount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    envelope = models.ForeignKey(Envelope, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=200)
    sum = models.FloatField()
    comments = models.CharField(max_length=400)

    def __str__(self):
        return self.description + " " + str(self.sum)

    TYPE_EXPENSE = 1
    TYPE_INCOME = 2
    TYPE_CHOICES = [
        (TYPE_EXPENSE, "Expense"),
        (TYPE_INCOME, "Income"),
    ]
    type = models.IntegerField(choices=TYPE_CHOICES, default=TYPE_EXPENSE)

    def type_to_string(self):
        for numeric_choice, string_choice in self.TYPE_CHOICES:
            if numeric_choice == self.type:
                return string_choice
        return "unknown"

    type_str = property(type_to_string)

    def update_envelope(self):
        envelope = self.envelope
        if self.type == self.TYPE_EXPENSE:
            envelope.current_sum -= self.sum
        else:
            envelope.current_sum += self.sum
        envelope.save()


class ScheduledTransaction (models.Model):  # TODO implement usage of the class
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    envelope = models.ForeignKey(Envelope, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    last_update = models.DateField()
    type = models.IntegerField()
    description = models.CharField(max_length=200)
    sum = models.FloatField()
    comments = models.CharField(max_length=400)

    def __str__(self):
        return self.description + " " + str(self.sum)


class SavingsHistory (models.Model):  # TODO: implement usage of this class
    """ This class stores history of previous savings for BudgetAccount """
    budget = models.ForeignKey(BudgetAccount, on_delete=models.CASCADE)
    date = models.DateField()
    saved_sum = models.FloatField()
