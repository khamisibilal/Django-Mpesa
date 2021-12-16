from Src.mpesa_api.mpesa_credentials import LipanaMpesaPassword, MpesaAccessToken
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
import requests
from requests import api
from requests.auth import HTTPBasicAuth
import json
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPassword
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment

# Create your views here.
def getAccessToken(request):
    consumer_key = 'wZeqHoIeNex11DYqCnGu3J4r0wXbiMzM'
    consumer_secret = 'y1TCX15H0czkaNAn'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    
    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortcode": LipanaMpesaPassword.Business_short_code,
        "Password": LipanaMpesaPassword.decode_password,
        "Timestamp": LipanaMpesaPassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254710962243, # your phone number
        
        "PartyB": LipanaMpesaPassword.Business_short_code,
        "PhoneNumber": 254710962243, # your phone number
        
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Bimal",
        "TransactionDesc": "Testing stk push"
        
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('Success')


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://b1ad-102-219-248-12.ngrok.io//api/v1/c2b/confirmation",
               "ValidationURL": "https://b1ad-102-219-248-12.ngrok.io//api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    
    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass

@csrf_exempt
def validation(request):
    
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return requests.get(context)
#JsonResponse(dict(context))

