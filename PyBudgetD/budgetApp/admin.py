from django.contrib import admin

from .models import *

admin.site.register(Users)
admin.site.register(Accounts)
admin.site.register(Categories)
admin.site.register(Permissions)
admin.site.register(UserAccounts)
admin.site.register(Envelopes)
admin.site.register(ActivityLogs)
admin.site.register(ScheduledTransactions)