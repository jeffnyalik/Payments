import requests
from requests.auth import HTTPBasicAuth

from Mpesa.accessToken import generateAccessToken
from Mpesa.encode import generatePassword
from Mpesa.utils import getTimeStamp
from credentials import keys


def lipaNaMpesa():
    formatted_time = getTimeStamp()
    decoded_password = generatePassword(formatted_time)
    access_token = generateAccessToken()

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {"Authorization": "Bearer %s" % access_token}

    request = {
        "BusinessShortCode": keys.business_shortCode,
        "Password": decoded_password,
        "Timestamp": formatted_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": keys.phone_number,
        "PartyB": keys.business_shortCode,
        "PhoneNumber": keys.phone_number,
        "CallBackURL": "https://africawatalii.com/api/payments/lnm/",
        "AccountReference": "test aware",
        "TransactionDesc": "Pay School Fees",
    }

    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)


lipaNaMpesa()