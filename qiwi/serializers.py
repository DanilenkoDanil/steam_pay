from rest_framework import serializers
from .models import Code, Payment
import requests
from requests.auth import HTTPBasicAuth


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Code
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"



