from django.db import models


class Users (models.Model):
    userName = models.EmailField()
    userPass = models.CharField(max_length=200)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)

    def __str__(self):
        return self.firstName + " " + self.lastName


class Accounts (models.Model):
    accountName = models.CharField(max_length=400)
    budget = models.BigIntegerField()
    resetDate = models.IntegerField()

    def __str__(self):
        return self.accountName


class Categories (models.Model):
    categoryName = models.CharField(max_length=400)

    def __str__(self):
        return self.categoryName


class Permissions (models.Model):
    permissionName = models.CharField(max_length=400)

    def __str__(self):
        return self.permissionName


class UserAccounts (models.Model):
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
    accountID = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    permissionID = models.ForeignKey(Permissions, on_delete=models.CASCADE)
    isDefault = models.BooleanField(default=False)

    def __str__(self):
        return "AccountId " + str(self.id)


class Envelopes (models.Model):
    accountID = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Categories, on_delete=models.CASCADE)
    envelopeName = models.CharField(max_length=200)
    envelopeBudget = models.IntegerField()
    currentSum = models.FloatField()

    def __str__(self):
        return self.envelopeName


class ActivityLogs (models.Model):
    accountID = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
    envelopeID = models.ForeignKey(Envelopes, on_delete=models.CASCADE)
    date = models.DateTimeField()
    type = models.IntegerField()
    description = models.CharField(max_length=200)
    sum = models.FloatField()
    comments = models.CharField(max_length=400)

    def __str__(self):
        return self.description + " " + str(self.sum)


class ScheduledTransactions (models.Model):
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
    envelopeID = models.ForeignKey(Envelopes, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    lastUpdate = models.DateField()
    type = models.IntegerField()
    description = models.CharField(max_length=200)
    sum = models.FloatField()
    comments = models.CharField(max_length=400)

    def __str__(self):
        return self.description + " " + str(self.sum)
