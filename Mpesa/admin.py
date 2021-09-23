from django.contrib import admin
from .models import BaseModel, PaymentTransaction, Wallet


admin.site.register(PaymentTransaction)
admin.site.register(Wallet)