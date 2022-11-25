from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions, views
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from .send import send_steam
from .models import Code, Setting, Payment
from .api import check_code
import requests


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


class GetCodeAPIView(generics.RetrieveAPIView):
    queryset = Code.objects.all()

    def retrieve(self, request, *args, **kwargs):
        setting = get_setting()
        code = request.query_params.get('uniquecode')
        key = get_key(code)
        if key is False:
            try:
                info = check_code(code=code, guid=setting.digi_code, seller_id=setting.seller_id)
            except Exception as e:
                print(e)
                print('no info')
                return Response(f"Ваш код не действителен", status=status.HTTP_201_CREATED)
            if info['retval'] == 0:
                if setting.auto_course:
                    currency = get_currency()
                else:
                    currency = float(setting.course)
                value = currency * float(info['value'])
                code_obj = Code.objects.create(code=code, status=False, amount=value, username=info['username'],
                                               error='')
                try:
                    send_steam(info['username'], value, setting.qiwi_code)
                    print('sssend')
                    code_obj.status = True
                    code_obj.save()
                    return Response(f"Ваш код принят", status=status.HTTP_201_CREATED)
                except Exception as e:
                    code_obj.error = str(e)
                    code_obj.save()
                    return Response(f"Произошла ошибка - обратитесь к продавцу", status=status.HTTP_201_CREATED)
            else:
                return Response(f"Ваш код не действителен", status=status.HTTP_201_CREATED)

        else:
            return Response(f"Ваш код уже обработан", status=status.HTTP_201_CREATED)


class JustPayAPIView(generics.RetrieveAPIView):
    queryset = Code.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        setting = get_setting()
        login = request.query_params.get('login')
        amount = request.query_params.get('amount')
        payment_obj = Payment.objects.create(status=False, amount=amount, username=login, error='')
        try:
            # send_steam(login, amount, setting.qiwi_code)
            print('sssend')
            payment_obj.status = True
            payment_obj.save()
            return Response(f"Запрос принят", status=status.HTTP_201_CREATED)
        except Exception as e:
            payment_obj.error = str(e)
            payment_obj.save()
            return Response(f"Произошла ошибка - обратитесь к продавцу", status=status.HTTP_201_CREATED)
