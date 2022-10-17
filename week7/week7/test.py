from account import *

account=Account('zjc',100)
try:
	#account.deposit(-100)
	account.withdraw(10000)
except AccountNegativeDepositError as ande:
	print(ande.message)
except AccountBalanceNotEnoughError as abnee:
	print(abnee.message)
except AccoutError:
	print('noname exception')
else:
	print('no except...')
	print(account.get_balance())