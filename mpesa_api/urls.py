from django.urls import path
from . import views

urlpatterns = [
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    
    # register, confirmation, validation and callback urls
    path('cb2/register', views.register_urls, name="register_mpesa_validation"),
    path('cb2/confirmation', views.confirmation, name="confirmation"),
    path('cb2/validation', views.validation, name="validation"),
    path('cb2/callback', views.call_back, name="call_back")
    
]