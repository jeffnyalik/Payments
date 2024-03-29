from django.urls import path
from .views import (
SubmitView, 
CheckTransaction,
ConfirmView,
CheckTransactionOnline,
RegisterApiView,
SimulateTransactionApiView, 
# C2BConfirmation,
C2BValidation,
)

from .import views


urlpatterns = [
    path('submit/', SubmitView.as_view(), name='submit'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
    path('check-online/', CheckTransactionOnline.as_view(), name='confirm-online'),
    path('check-transaction/', CheckTransaction.as_view(), name='check_transaction'),

    # C2b transaction urls
    path('register-urls/', RegisterApiView.as_view(), name='register-urls'),
    path('simulate-transactions/', SimulateTransactionApiView.as_view(), name='simulate-transactions'),

    #C2b validation and confirmation urls
    # path('c2b-confirmation/', views.TestConfirmation, name='c2b-confirmation'),
    path('c2b-validation/', views.TestValidation, name='c2b-validation'),

    # testpath
    path('c2b-confirmation/', views.C2BConfirmationApiView.as_view(), name='c2b-confirmation'),
]