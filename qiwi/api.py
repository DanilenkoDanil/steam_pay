import requests
import time
from hashlib import sha256
import json


def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def check_code(code: str, guid: str = '22882862E75441D5B0DC400A77F4972D', seller_id: int = 224269):
    timestamp = str(int(time.time()))

    api_guid = guid + timestamp

    sign = sha256(api_guid.encode('utf-8')).hexdigest()

    data = {
        'seller_id': seller_id,
        'timestamp': timestamp,
        'sign': sign

    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post('https://api.digiseller.ru/api/apilogin', json=data, headers=headers)
    token_json = json.loads(response.content.decode('utf8'))
    try:
        token = token_json['token']
    except KeyError:
        time.sleep(10)
        response = requests.post('https://api.digiseller.ru/api/apilogin', json=data, headers=headers)
        token_json = json.loads(response.content.decode('utf8'))
        token = token_json['token']

    response = requests.get(f'https://oplata.info/api/purchases/unique-code/{code}?token={token}')
    result_json = json.loads(response.content.decode('utf8'))
    try:
        value = result_json['options'][1]['value'].split(' ')[0]
        if is_digit(value) is not False:
            if float(value) < 5:
                value = result_json['cnt_goods']
        else:
            value = result_json['cnt_goods']
    except IndexError:
        value = result_json['cnt_goods']
    return {
        'retval': result_json['retval'],
        'username': result_json['options'][0]['value'],
        "value": value}


# print(check_code('A1686F6ADEBB4ADC'))
