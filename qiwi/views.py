from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .send import send_steam, send_steam_ozon, get_balance, check_full
from .models import Code, Setting, Payment, Qiwi, Interhub, UserLimitation
from .api import check_code
import requests
from django.http import JsonResponse
from datetime import date, timedelta
from qiwi.serializers import PaymentSerializer


def get_key(key: str):
    try:
        return Code.objects.filter(code=key)[0]
    except IndexError:
        return False


def get_user_limit(user):
    try:
        return UserLimitation.objects.filter(user=user)[0]
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
                currency = float(setting.course)
                value = float(info['value']) / currency
                code_obj = Code.objects.create(code=code, status=False, amount=value, username=info['username'],
                                               error='')
                try:
                    interhub = Interhub.objects.all().last()
                    send_steam_ozon(info['username'], value, interhub.token)
                    interhub.balance = get_balance(interhub.token)
                    interhub.save()
                    print('sssend')
                    code_obj.status = True
                    code_obj.save()
                    return Response(f"Ваш аккаунт пополнен", status=status.HTTP_201_CREATED)
                except Exception as e:
                    code_obj.error = str(e)
                    code_obj.save()
                    return Response(f"Произошла ошибка - обратитесь к продавцу", status=status.HTTP_201_CREATED)
            else:
                return Response(f"Ваш код не действителен", status=status.HTTP_201_CREATED)

        else:
            return Response(f"Ваш код уже обработан", status=status.HTTP_201_CREATED)


class JustPayAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        login = request.query_params.get('login')
        amount = float(request.query_params.get('amount'))

        user_limit = get_user_limit(request.user)
        if user_limit is not False:
            if user_limit.now_balance < amount:
                return JsonResponse('Insufficient balance', status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse('Limit not set', status=status.HTTP_400_BAD_REQUEST)

        payment_obj = Payment.objects.create(status=False, amount=amount, username=login, error='', user=request.user)
        interhub = Interhub.objects.all().last()
        try:
            send_steam_ozon(login, amount, interhub.token)
            interhub.balance = get_balance(interhub.token)
            interhub.save()
            payment_obj.status = True
            payment_obj.save()
            user_limit.now_balance -= amount
            user_limit.save()
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


class UserLimitationView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserLimitation.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        try:
            user_limitation = UserLimitation.objects.get(user=user)
            response_data = {
                'user': user.username,
                'now_balance': user_limitation.now_balance
            }
            return Response(response_data, status=200)
        except UserLimitation.DoesNotExist:
            response_data = {
                'user': user.username,
                'message': 'User limitation data not found'
            }
            return Response(response_data, status=404)


class UserPaymentsView(generics.ListAPIView):
    queryset = Payment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(user=user)


class CheckPaymentView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserLimitation.objects.all()

    def retrieve(self, request, *args, **kwargs):
        login = request.query_params.get('login')
        amount = float(request.query_params.get('amount'))
        interhub = Interhub.objects.all().last()
        response_data = check_full(login, amount, interhub.token)
        return Response(response_data, status=200)
