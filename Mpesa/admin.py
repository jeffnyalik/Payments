from django.contrib import admin
from .models import BaseModel, PaymentTransaction, Wallet, PayBillPayment


admin.site.register(PaymentTransaction)
admin.site.register(Wallet)
# admin.site.register(PayBillPayment)


class PayBillPaymentModelAdmin(admin.ModelAdmin):
    fields = [
        'TransactionType',
        'TransAmount',
        'BusinessShortCode',
        'BillRefNumber',
        'InvoiceNumber',
        'OrgAccountBalance',
        'ThirdPartyTransID',
        'MSISDN',
        'TransID', 
        'FirstName',
        'MiddleName', 
        'LastName'
    ]

admin.site.register(PayBillPayment, PayBillPaymentModelAdmin)