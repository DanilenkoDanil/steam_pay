from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions, views
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from .send import send_steam
from .models import Code, Setting
from .api import check_code
import requests


def get_key(key: str):
    try:
        return Code.objects.filter(code=key)[0]
    except IndexError:
        return False


def get_setting():
    return Setting.objects.filter(id=1)[0]


class GetCodeAPIView(generics.RetrieveAPIView):
    queryset = Code.objects.all()

    def retrieve(self, request, *args, **kwargs):
        setting = get_setting()
        code = request.query_params.get('uniquecode')
        key = get_key(code)
        if key is False:
            try:
                print(code)
                print(setting.digi_code)
                print(setting.seller_id)
                info = check_code(code=code, guid=setting.digi_code, seller_id=setting.seller_id)
                print(info)
            except Exception as e:
                print(e)
                print('no info')
                return Response(f"Ваш код не действителен", status=status.HTTP_201_CREATED)
            if info['retval'] == 0:
                value = float(setting.course) * float(info['value'])
                try:
                    print(info['username'], value, setting.qiwi_code)
                    send_steam(info['username'], value, setting.qiwi_code)
                    Code.objects.create(code=code, status=True, amount=value, username=info['username'], error='')
                    return Response(f"Ваш код принят", status=status.HTTP_201_CREATED)
                except Exception as e:
                    Code.objects.create(code=code, status=False, amount=value, username=info['username'], error=str(e))
                    return Response(f"Произошла ошибка - обратитесь к продавцу", status=status.HTTP_201_CREATED)
            else:
                return Response(f"Ваш код не действителен", status=status.HTTP_201_CREATED)

        else:
            return Response(f"Ваш код уже обработан", status=status.HTTP_201_CREATED)
