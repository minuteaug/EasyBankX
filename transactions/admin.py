from django.contrib import admin

from transactions.models import Transaction
from transactions.models import User

admin.site.register(Transaction)
admin.site.register(User)
