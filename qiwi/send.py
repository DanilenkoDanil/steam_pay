import requests
import time


def send_steam(login: str, amount: float, authorization: str) -> dict:
    s = requests.Session()
    s.headers['Accept'] = 'application/json'
    s.headers['Content-Type'] = 'application/json'
    s.headers['authorization'] = 'Bearer ' + authorization
    postjson = {
        'id': "",
        "sum": {
            "amount": "",
            "currency": "398"
        },
        "paymentMethod": {
            "type": "Account",
            "accountId": "398"
        },
        "fields": {
            "account": ""
        }
    }
    postjson['id'] = str(int(time.time() * 1000))
    postjson['sum']['amount'] = str(amount)
    postjson['fields']['account'] = login
    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/31212/payments', json=postjson)
    print(res.json())
    return res.json()
