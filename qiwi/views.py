from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .send import send_steam, send_steam_ozon, get_balance
from .models import Code, Setting, Payment, Qiwi, Interhub
from .api import check_code
import requests
from django.http import JsonResponse
from datetime import date, timedelta


def get_key(key: str):
    try:
        return Code.objects.filter(code=key)[0]
    except IndexError:
        return False


def get_setting():
    return Setting.objects.filter(id=1)[0]


def get_qiwi(value: float):
    setting = get_setting()
    delta_time = date.today() - timedelta(days=1)
    for qiwi in Qiwi.objects.all():
        if qiwi.current_counter + value < setting.qiwi_limit:
            return qiwi, qiwi.qiwi_code
        elif date(delta_time.year, delta_time.month, delta_time.day) > date(qiwi.timer.year,
                                                                            qiwi.timer.month,
                                                                            qiwi.timer.day):
            qiwi.current_counter = 0
            qiwi.timer = date.today()
            qiwi.save()
            return qiwi, qiwi.qiwi_code
    return False


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
                    qiwi, key = get_qiwi(value)
                    send_steam(info['username'], value, key)
                    qiwi.current_counter += value
                    qiwi.save()
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
        login = request.query_params.get('login')
        amount = float(request.query_params.get('amount'))
        payment_obj = Payment.objects.create(status=False, amount=amount, username=login, error='')
        interhub = Interhub.objects.get(id=1)
        try:
            send_steam_ozon(login, amount, interhub.token)
            interhub.balance = get_balance(interhub.token)
            interhub.save()
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
