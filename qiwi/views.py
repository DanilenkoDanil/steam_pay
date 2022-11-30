from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions, views
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from .send import send_steam
from .models import Code, Setting, Payment
from .api import check_code
import requests
from django.http import JsonResponse


def get_key(key: str):
    try:
        return Code.objects.filter(code=key)[0]
    except IndexError:
        return False


def get_setting():
    return Setting.objects.filter(id=1)[0]


def get_currency():
    response = requests.get('https://free.currconv.com/api/v7/convert?q=RUB_KZT&compact=ultra&apiKey=b9e0655ea622bcfeefa5')
    return float(response.json()['RUB_KZT'])


class JustPayAPIView(generics.RetrieveAPIView):
    queryset = Code.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        setting = get_setting()
        login = request.query_params.get('login')
        amount = request.query_params.get('amount')
        payment_obj = Payment.objects.create(status=False, amount=amount, username=login, error='')
        try:
            send_steam(login, amount, setting.qiwi_code)
            print('sssend')
            payment_obj.status = True
            payment_obj.save()
            response = {
                'status': 'Success',
                'username': login,
                'amount': amount
            }
            return JsonResponse(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            payment_obj.error = str(e)
            payment_obj.save()
            response = {
                'status': 'Failure',
                'username': login,
                'amount': amount
            }
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
