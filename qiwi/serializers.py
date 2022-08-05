from rest_framework import serializers
from .models import Code
import requests
from requests.auth import HTTPBasicAuth


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Code
        fields = "__all__"


