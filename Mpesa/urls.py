from django.urls import path
from . import views
urlpatterns = [
    path('', views.lipaNaMpesaOnline, name='Lipa Na Mpesa Online')
]