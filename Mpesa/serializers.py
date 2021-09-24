from .models import PayBillPayment
from rest_framework import serializers


class PayBillSerialzer(serializers.ModelSerializer):
    class Meta:
        model = PayBillPayment
        fields = [
        'id', 
        'TransactionType', 
        'TransID', 
        'TransAmount',
        'BusinessShortCode',
        'BillRefNumber',
        'InvoiceNumber',
        'OrgAccountBalance',
        'ThirdPartyTransID',
        'phone_number',
        'firstName',
        'middleName',
        'lastName'
        ]
