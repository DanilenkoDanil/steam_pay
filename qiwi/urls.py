from .views import GetCodeAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('pay/', GetCodeAPIView.as_view(), name='pay'),
]