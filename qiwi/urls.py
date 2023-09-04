from .views import GetCodeAPIView, JustPayAPIView, UserLimitationView, UserPaymentsView, CheckPaymentView
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.shortcuts import render


urlpatterns = [
    path('pay/', GetCodeAPIView.as_view(), name='pay'),
    path('just-pay/', JustPayAPIView.as_view(), name='just-pay'),
    path('get-balance/', UserLimitationView.as_view(), name='get-balance'),
    path('get-payments/', UserPaymentsView.as_view(), name='get-payments'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('check/', CheckPaymentView.as_view(), name='check'),
    path('docs/', lambda request: render(request, 'main/docs.html'), name='docs')
]
