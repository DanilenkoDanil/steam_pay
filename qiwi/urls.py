from .views import GetCodeAPIView, JustPayAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('pay/', GetCodeAPIView.as_view(), name='pay'),
    path('just-pay/', JustPayAPIView.as_view(), name='just-pay'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
