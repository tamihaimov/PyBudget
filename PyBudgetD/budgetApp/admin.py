from django.contrib import admin

from .models import *

admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Permission)
admin.site.register(UserAccount)
admin.site.register(Envelope)
admin.site.register(Transaction)
admin.site.register(ScheduledTransaction)


