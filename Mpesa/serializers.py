from .models import PayBillPayment
from rest_framework import serializers


class PayBillSerialzer(serializers.ModelSerializer):
    class Meta:
        model = PayBillPayment
        fields = ['id',]
