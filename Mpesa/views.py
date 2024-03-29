# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .lipaNaMpesaOnline import stkPush, check_payment_status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from .models import PaymentTransaction
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from .customerPaybill import registerUrl, simulateTransaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .customerPaybill import getToken
from credentials import keys
import requests
from django.http import HttpResponse
from rest_framework.generics import CreateAPIView
from .models import PayBillPayment
from Mpesa.serializers import PayBillSerialzer
from rest_framework import status
from rest_framework.generics import CreateAPIView


class PaymentTranactionView(ListCreateAPIView):
    def post(self, request):
        return HttpResponse("OK", status=200)


class SubmitView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        phone_number = data['phone_number']
        amount = data['amount']

        entity_id = 0
        if data.get('entity_id'):
            entity_id = data.get('entity_id')

        transactionId = stkPush(phone_number, amount, entity_id)
        # b2c()
        message = {"status": "ok", "transaction_id": transactionId}
        return Response(message, status=HTTP_200_OK)


class CheckTransactionOnline(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        trans_id = request.data['transaction_id']
        transaction = PaymentTransaction.objects.filter(id=trans_id).get()
        try:
            if transaction.checkoutRequestID:
                status_response = check_payment_status(transaction.checkoutRequestID)
                return JsonResponse(
                    status_response, status=200)
            else:
                return JsonResponse({
                    "message": "Server Error. Transaction not found",
                    "status": False
                }, status=400)
        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Server Error. Transaction not found",
                "status": False
            },
                status=400)


class CheckTransaction(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        trans_id = data['transaction_id']
        try:
            transaction = PaymentTransaction.objects.filter(id=trans_id).get()
            if transaction:
                return JsonResponse({
                    "message": "ok",
                    "finished": transaction.isFinished,
                    "successful": transaction.isSuccessFull
                },
                    status=200)
            else:
                # TODO : Edit order if no transaction is found
                return JsonResponse({
                    "message": "Error. Transaction not found",
                    "status": False
                },
                    status=400)
        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Server Error. Transaction not found",
                "status": False
            },
                status=400)


class RetryTransaction(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        trans_id = request.data['transaction_id']
        try:
            transaction = PaymentTransaction.objects.filter(id=trans_id).get()
            if transaction and transaction.isSuccessFull:
                return JsonResponse({
                    "message": "ok",
                    "finished": transaction.isFinished,
                    "successful": transaction.isSuccessFull
                },
                    status=200)
            else:
                response = sendSTK(
                    phone_number=transaction.phone_number,
                    amount=transaction.amount,
                    orderId=transaction.order_id,
                    transaction_id=trans_id)
                return JsonResponse({
                    "message": "ok",
                    "transaction_id": response
                },
                    status=200)

        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                "message": "Error. Transaction not found",
                "status": False
            },
                status=400)


class ConfirmView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        # save the data
        request_data = json.dumps(request.data)
        request_data = json.loads(request_data)
        body = request_data.get('Body')
        resultcode = body.get('stkCallback').get('ResultCode')
        # Perform your processing here e.g. print it out...
        if resultcode == 0:
            print('Payment successful')
            requestId = body.get('stkCallback').get('CheckoutRequestID')
            metadata = body.get('stkCallback').get('CallbackMetadata').get('Item')
            for data in metadata:
                if data.get('Name') == "MpesaReceiptNumber":
                    receipt_number = data.get('Value')
            transaction = PaymentTransaction.objects.get(
                checkoutRequestID=requestId)
            if transaction:
                transaction.trans_id = receipt_number
                transaction.isFinished = True
                transaction.isSuccessFull = True
                transaction.save()

        else:
            print('unsuccessfull')
            requestId = body.get('stkCallback').get('CheckoutRequestID')
            transaction = PaymentTransaction.objects.get(
                checkoutRequestID=requestId)
            if transaction:
                transaction.isFinished = True
                transaction.isSuccessFull = False
                transaction.save()

        # Prepare the response, assuming no errors have occurred. Any response
        # other than a 0 (zero) for the 'ResultCode' during Validation only means
        # an error occurred and the transaction is cancelled
        message = {
            "ResultCode": 0,
            "ResultDesc": "The service was accepted successfully",
            "ThirdPartyTransID": "1237867865"
        }

        # Send the response back to the server
        return Response(message, status=HTTP_200_OK)

    def get(self, request):
        return Response("Confirm callback", status=HTTP_200_OK)


class ValidateView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        # save the data
        request_data = request.data


        # Perform your processing here e.g. print it out...
        print("validate data" + request_data)

        # Prepare the response, assuming no errors have occurred. Any response
        # other than a 0 (zero) for the 'ResultCode' during Validation only means
        # an error occurred and the transaction is cancelled
        message = {
            "ResultCode": 0,
            "ResultDesc": "The service was accepted successfully",
            "ThirdPartyTransID": "1234567890"
        }

        # Send the response back to the server
        return Response(message, status=HTTP_200_OK)


class RegisterApiView(APIView):
    permission_classes =  [AllowAny, ]

    def get(self, request, format=None):
        res = registerUrl()
        return Response(res, status=HTTP_200_OK)


class SimulateTransactionApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        response = simulateTransaction()
        return Response(response, status=HTTP_200_OK)


class C2BValidation(APIView):
    permission_classes = [AllowAny, ]
    
    def get(self, request, format=None):
        data = request.data
        return Response(data)

class C2BConfirmationApiView(CreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = PayBillPayment.objects.all()
    serializer_class = PayBillSerialzer


    def create(self, request):
        transaction_type = request.data['TransactionType']
        transaction_id = request.data['TransID']
        # trans_time = request.data['TransTime']
        trans_amount = request.data['TransAmount']
        business_short_code = request.data['BusinessShortCode']
        bill_ref_number = request.data['BillRefNumber']
        invoice_number = request.data['InvoiceNumber']
        org_account_balance = request.data['OrgAccountBalance']
        third_party_trans_id = request.data['ThirdPartyTransID']
        msisdn_number = request.data['MSISDN']
        first_name = request.data['FirstName']
        middle_name = request.data['MiddleName']
        last_name = request.data['LastName']

        paybill_model = PayBillPayment.objects.create(
            TransactionType=transaction_type,
            TransID=transaction_id,
            TransAmount=trans_amount,
            BusinessShortCode=business_short_code,
            BillRefNumber=bill_ref_number,
            InvoiceNumber=invoice_number,
            OrgAccountBalance=org_account_balance,
            ThirdPartyTransID=third_party_trans_id,
            MSISDN=msisdn_number,
            FirstName=first_name,
            MiddleName=middle_name,
            LastName=last_name
        )

        paybill_model.save()
      
        print(request.data, 'This request comes from the confirmation')
        return Response({'ResultDesc': request.data})


    # @csrf_exempt
    # def post(self, request, format=None):
    #     serializer = PayBillSerialzer(data=request.data)
    #     print(serializer)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def TestValidation(request):
    mpesa_body = request.body.decode('utf-8')
    print(mpesa_body, "This is request data in validation")
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
    # return Response({"ResultCode": 0, "ResultDesc": "Accepted"})


@csrf_exempt
def TestConfirmation(request):
    mpesa_body = request.body.decode('utf-8')
    print(mpesa_body, "This is request data in confirmation")
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted",
    }

    return JsonResponse(dict(context))
    # return Response({"ResultCode": 0,"ResultDesc": "Accepted"})