from requests.auth import HTTPBasicAuth
from credentials import keys
import requests
from datetime import datetime
import json
from decimal import Decimal

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


def registerUrl():
    access_token = getToken()
    if access_token is False:
        raise Exception('Invalid access Token')
    
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"

    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }

    request = {
        "ShortCode": keys.shortcode,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://mwando.herokuapp.com/api/c2b-confirmation/",
        "ValidationURL":   "https://mwando.herokuapp.com/api/c2b-validation/",

        # "ConfirmationURL": "localhost:8000/api/c2b-confirmation/",
        # "ValidationURL":   "localhost:8000/api/c2b-validation/",
    }

    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    return json_response


# amount, mssidn, short_code=None
def simulateTransaction():
    code = keys.shortcode
    access_token = getToken()

    if access_token is False:
        raise Exception('Invalid access token')

    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }

    request = {
        "ShortCode": keys.shortcode,
        "CommandID": "CustomerPayBillOnline",
        "Amount": "10",
        "Msisdn": keys.test_msisdn,
        "BillRefNumber": "myaccnumber",
    }

    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    return json_response
   