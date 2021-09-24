from django.contrib import admin
from .models import BaseModel, PaymentTransaction, Wallet, PayBillPayment


admin.site.register(PaymentTransaction)
admin.site.register(Wallet)
admin.site.register(PayBillPayment)