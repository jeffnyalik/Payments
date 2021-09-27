from django.contrib import admin
from .models import BaseModel, PaymentTransaction, Wallet, PayBillPayment


# admin.site.register(PaymentTransaction)
admin.site.register(Wallet)
# admin.site.register(PayBillPayment)


class PayTransactionAdmin(admin.ModelAdmin):

    list_display = (
        'phone_number',
        'amount',
        'trans_id',
        'order_id',
    )

    list_filter = ('phone_number',)
admin.site.register(PaymentTransaction, PayTransactionAdmin)

class PayBillModelAdmin(admin.ModelAdmin):

    list_display = (
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
        'LastName',
    )

    list_filter = ('BillRefNumber', 'OrgAccountBalance', 'BusinessShortCode', )
admin.site.register(PayBillPayment, PayBillModelAdmin)