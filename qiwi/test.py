# import pyqiwi
#
# wallet = pyqiwi.Wallet(token='116d52a6bdcdc33a488d82b9e736bc7c', number='79114962781')
# print(wallet.balance())
# wallet.send(pid=99, recipient='31212', amount=100, comment='danilenko231')


from SimpleQIWI import *

token = '116d52a6bdcdc33a488d82b9e736bc7c'
phone = "79118500238"

api = QApi(token=token, phone=phone)

print(api.balance)

api.pay(account="31212", amount=60)

print(api.balance)