from requests.auth import HTTPBasicAuth
from credentials import keys
import requests
from datetime import datetime
from base64 import b64encode
import json
from .models import PaymentTransaction

# Applies for LipaNaMpesaOnline Payment method
def generate_pass_key():
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")
    s = keys.business_shortCode + keys.lipa_na_mpesa_passkey + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

def getToken():
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    print(api_url)

    r = requests.get(api_url, auth=HTTPBasicAuth(keys.consumer_key, keys.consumer_secret))
    if r.status_code == 200:
        jonresponse = json.loads(r.content)
        access_token = jonresponse['access_token']
        return access_token
    elif r.status_code == 400:
        print('Invalid credentials.')
        return False

def stkPush(phone_number, amount, orderId=0, transaction_id=None, short_code=None):
    code = keys.business_shortCode
    access_token = getToken()
    if access_token is False:
        raise Exception('Invalid Consumer or Secret key')
        
    time_now = datetime.now().strftime("%Y%m%d%H%I%S")

    s = code + keys.lipa_na_mpesa_passkey + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }
    request = {
        "BusinessShortCode": code,
        "Password": encoded,
        "Timestamp": time_now,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(int(amount)),
        "PartyA": phone_number,
        "PartyB": code,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://africawatalii.com/api/payments/lnm/",
        "AccountReference": code,
        "TransactionDesc": "Payment for {}".format(phone_number)
    }

    print(request)
    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    if json_response.get('ResponseCode'):
        if json_response["ResponseCode"] == "0":
            checkout_id = json_response["CheckoutRequestID"]
            if transaction_id:
                transaction = PaymentTransaction.objects.filter(id=transaction_id)
                transaction.checkoutRequestID = checkout_id
                transaction.save()
                return transaction.id
            else:
                transaction = PaymentTransaction.objects.create(phone_number=phone_number,
                                                                checkoutRequestID=checkout_id,
                                                                amount=amount, order_id=orderId)
                transaction.save()
                return transaction.id
    else:
        raise Exception("Error sending MPesa stk push", json_response)

def check_payment_status(checkout_request_id, shortcode=None):
    code = keys.business_shortCode
    access_token = getToken()
    time_now = datetime.now().strftime("%Y%m%d%H%I%S")

    s = code + keys.lipa_na_mpesa_passkey + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "{}/mpesa/stkpushquery/v1/query".format('https://sandbox.safaricom.co.ke')
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }
    request = {
        "BusinessShortCode": code,
        "Password": encoded,
        "Timestamp": time_now,
        "CheckoutRequestID": checkout_request_id
    }
    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    if 'ResponseCode' in json_response and json_response["ResponseCode"] == "0":
        requestId = json_response.get('CheckoutRequestID')
        transaction = PaymentTransaction.objects.get(
            checkoutRequestID=requestId)
        if transaction:
            transaction.isFinished = True
            transaction.isSuccessFull = True
            transaction.save()

        result_code = json_response['ResultCode']
        response_message = json_response['ResultDesc']
        return {
            "result_code": result_code,
            "status": result_code == "0",
            "message": response_message
        }
    else:
        raise Exception("Error sending MPesa stk push", json_response)