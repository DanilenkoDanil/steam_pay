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
    return res.json()


def check(account: str, amount: float, authorization: str):
    url = "https://api.interhub.uz/api/payment/check"
    timer = time.time()
    payload = {
        "amount": amount,
        "service_id": 92,
        "agent_transaction_id": str(timer + 68846442),
        "account": account,
        "params": {}
    }
    headers = {
        'token': 'okhwhalpvuf10Y8EEMA-JhBPn1?ckHvZX9vatbpUrGlrB1'
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return response.json()['transaction_id']


def pay(transaction: str, authorization: str):
    url = "https://api.interhub.uz/api/payment/pay"

    payload = {
        "transaction_id": transaction,
        "currencyId": 0,
        "checkTransactionId": transaction
    }
    headers = {
        'token': 'okhwhalpvuf10Y8EEMA-JhBPn1?ckHvZX9vatbpUrGlrB1'
    }

    response = requests.request("POST", url, headers=headers, json=payload)
    return response.json()


def send_steam_ozon(login: str, amount: float, authorization: str) -> bool:
    transaction_id = check(login, amount, authorization)
    pay(transaction_id, authorization)
    return True


# send_steam('sh33shka', 560, '5a6d1dac7d9455bed78462ab4858c8c1')
# send_steam_ozon('sh33shka', 560, '5a6d1dac7d9455bed78462ab4858c8c1')