from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions, views
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from .send import send_steam
from .models import Code
import requests


def get_key(key: str):
    try:
        return Code.objects.filter(code=key)[0]
    except IndexError:
        return False


# Create your views here.
class GetCodeAPIView(generics.RetrieveAPIView):
    queryset = Code.objects.all()

    def retrieve(self, request, *args, **kwargs):
        code = request.query_params.get('code')
        code_obj = Code.objects.filter(code=int(code))
        if len(code_obj) != 0:
            return Response(f"Ваш код уже обработан", status=status.HTTP_201_CREATED)
        if code == '13123123':
            send_steam('sh33shka', 500)
            Code.objects.create(code=code, status=True, amount=500, username='danilenko231')
            return Response(f"Ваш код принят", status=status.HTTP_201_CREATED)
        return Response(f"Ваш код не подходит", status=status.HTTP_201_CREATED)


class GetCodeAPIView(generics.RetrieveAPIView):
    queryset = Code.objects.all()

    def retrieve(self, request, *args, **kwargs):
        code = request.query_params.get('uniquecode')
        key = get_key(code)
        if key is False:
            info = api.check_code(code)
            if info['retval'] == 0:
                send_steam('sh33shka', 500)
                Code.objects.create(code=code, status=True, amount=500, username='danilenko231')
                return Response(f"Ваш код принят", status=status.HTTP_201_CREATED)
        else:
            return Response(f"Ваш код уже обработан", status=status.HTTP_201_CREATED)


def index(request):
    code = request.GET.get('uniquecode')
    key = get_key(code)
    if key is False:
        info = api.check_code(code)
        if info['retval'] == 0:

            game = get_game(info['id_goods'])
            game_code = game.app_code

            image_link = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_code}/header.jpg"
            game_link = f'https://store.steampowered.com/app/{game_code}'

            return render(request, 'main/account.html',
                          {'game_name': game.name,
                           'game_link': game_link,
                           'image_link': image_link,
                           'code': code
                           })
        else:
            html = f"Код {code} не действителен!"
            return HttpResponse(html)
    else:

        return render(request, 'main/account.html',
                      {'game_name': key.game.name,
                       'game_link': game_link,
                       'image_link': image_link,
                       'code': code,
                        })