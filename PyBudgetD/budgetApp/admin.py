from django.contrib import admin

from .models import *

admin.site.register(BudgetAccount)
admin.site.register(UserBudget)
admin.site.register(Envelope)
admin.site.register(Transaction)
admin.site.register(ScheduledTransaction)
admin.site.register(SavingsHistory)
