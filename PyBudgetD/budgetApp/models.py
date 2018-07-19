from django.db import models
from django.contrib.auth.models import User


class Account (models.Model):
    name = models.CharField(max_length=400)
    budget = models.BigIntegerField()
    reset_date = models.IntegerField()

    def __str__(self):
        return self.name
    
    def calc_balance (self):
        envelopes = self.envelope_set.all()
        balance = 0
        for envelope in envelopes:
            balance += envelope.current_sum
        return balance
    balance = property(calc_balance)


class Category (models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Permission (models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class UserAccount (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return "AccountId " + str(self.id)

    PERMISSION_OWNER = 1
    PERMISSION_USER = 2
    PERMISSION_VIEWER = 3
    PERMISSION_CHOICES = [
        (PERMISSION_OWNER, 'owner'),
        (PERMISSION_USER, 'user'),
        (PERMISSION_VIEWER, 'viewer')
    ]


class Envelope (models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    budget = models.IntegerField()
    current_sum = models.FloatField()

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
    CATEGORY_CHOICES = [
        (CATEGORY_FOOD, 'Food and Dining'),
        (CATEGORY_BILLS, 'Bills and Utilities'),
        (CATEGORY_TRANSPORT, 'Auto and Transportation'),
        (CATEGORY_HOUSING, 'Housing'),
        (CATEGORY_HEALTH_CARE, 'HealthCare'),
        (CATEGORY_SAVINGS, 'Savings'),
        (CATEGORY_ENTERTAINMENT, 'Entertainment'),
        (CATEGORY_MISC, 'Miscellaneous'),
    ]


class Transaction (models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    envelope = models.ForeignKey(Envelope, on_delete=models.CASCADE)
    date = models.DateTimeField()
    type = models.IntegerField()
    description = models.CharField(max_length=200)
    sum = models.FloatField()
    comments = models.CharField(max_length=400)

    def __str__(self):
        return self.description + " " + str(self.sum)

    def type_to_string (self):
        if self.type == 1:
            return "Expense"
        return "Income"
    type_str = property(type_to_string)


class ScheduledTransaction (models.Model):
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
