# Payment Integration

Mpesa Payment Integration App API focussing on STK Push(Lipa na Mpesa Online) and C2B (Customer to Paybill).
Built using Django and Django Rest Framework on the backend.

# Testing the Application STK Push (Lipa na Mpesa Online)

1. Make sure you have Postman installed.
2. Make a post request on the endpoint: {your_app_url}/api/submit/.
3. The Body parameter should have phone_number and amount.
4. Click on send button and you are done.


# Testing the Application C2B(Customer to Paybill)

1. Make sure you have Postman installed.
2. Make a GET request on the endpoint to register the urls: {your_app_url}/api/register-urls
3. Make a POST request on the endpoint to Simulate transactions: {your_app_url}/api/simulate-transactions/.

# Confirmation and Validation Endpoints:
1.  Confirmation Endpoint:  POST Request: {your_app_url}/api/c2b-confirmation/
        => With the following as parameters: \
        "TransactionType": "Pay Bill",
        "TransID": "PIR31HK5JV",
        "TransAmount": "10",
        "BusinessShortCode": "600978",
        "BillRefNumber": "myaccnumber",
        "InvoiceNumber": "",
        "OrgAccountBalance": "664841.00",
        "ThirdPartyTransID": "",
        "MSISDN": "254708374149",
        "FirstName": "John",
        "MiddleName": "J.",
        "LastName": "Doe"

2.  Validation Endpoint :   GET Request: {your_app_url}/api/c2b-validation/


Finally you can view the transactions through your heroku apps logs, 
you can create django super admin to view the saved transactions.


@Happy Coding everyone!! cheers.