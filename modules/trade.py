import pandas as pd
import time
import datetime as dt
from modules.util import *
from modules.Logger import *
from stockstats import *
import modules.db as db
import modules.coinone as co
from collections import defaultdict

class TestTrade( ):
	def __init__( self, krw, currency, exchanger, feeRate, min_order ):
		self.currency = currency
		self.feeRate = feeRate
		self.exchanger = exchanger
		self.min_order = min_order

		self.krw_balance = krw
		self.crypto_balance = 0.0

	def buy( self, dict_order, price ):
		holding = False
		if len(dict_order) > 0 :
			tmpType = str(dict_order['type'])
			if tmpType == 'bid':
				LOG.warn("already buy. type="+ tmpType )
				holding = True
				return

		fee = round( price*self.feeRate )
		min_pay = round( self.min_order * (price + fee) )
		if self.krw_balance < min_pay :
			LOG.error("not enough money. krw=>"+ str(self.krw_balance) + " "+self.currency+"=>"+ str(min_pay ) )
			return

		qty = int( self.krw_balance / min_pay )
		self.crypto_balance = qty
		LOG.debug("krw="+ str(self.krw_balance) + " "+self.currency+"="+ str(price ) )
		LOG.debug("qty="+ str(qty) + " fee="+ str(fee ) + " min_pay="+str(min_pay) )

		self.krw_balance = self.krw_balance - (qty*min_pay)
		LOG.debug("will be krw_balance="+ str(self.krw_balance ) )

		now = get_time()
		dict = defaultdict(object)
		dict['exchanger'] = self.exchanger
		dict['date'] = now
		dict['currency'] = self.currency
		dict['type'] = 'bid'
		dict['price'] = price
		dict['qty'] = qty
		dict['feeRate'] = self.feeRate
		dict['fee'] = fee
		dict['order_id'] = 'TEST_'+ now
		dict['profit'] = 0
		dict['balance'] = self.krw_balance
		dict['crypto_balance'] = self.crypto_balance

		df = pd.DataFrame( dict, index=[0] )
		db.insert( df, 'TEST')
		LOG.info("end buy")


	def sell( self, dict_order, price ):
		if len(dict_order) < 1 :
			LOG.warn("order is empty")
			return
		tmpType = str(dict_order['type'])
		if tmpType != 'bid':
			LOG.warn("last order is "+ tmpType )
			return

		decision = price - (dict_order['price'] + dict_order['fee'] )
		if decision >= 0 :
			LOG.info("not sell!! price="+ str(price) + " decision="+str(decision))
			return

		LOG.info("qty=>"+ str(dict_order['qty']) + " "+self.currency+"=>"+ str(price ) )
		qty = dict_order['qty']
		fee = round(qty*price*self.feeRate)
		get = qty*price - fee

		profit = (price - dict_order['price']) / dict_order['price'] * 100

		self.krw_balance = self.krw_balance + get
		self.crypto_balance = self.crypto_balance - qty

		now = get_time()
		dict = defaultdict(object)
		dict['exchanger'] = self.exchanger
		dict['date'] = now
		dict['currency'] = self.currency
		dict['type'] = 'ask'
		dict['price'] = price
		dict['qty'] = dict_order['qty']
		dict['feeRate'] = self.feeRate
		dict['fee'] = fee
		dict['order_id'] = 'TEST_'+ now
		dict['profit'] = profit
		dict['balance'] = self.krw_balance
		dict['crypto_balance'] = self.crypto_balance

		df = pd.DataFrame( dict, index=[0] )
		db.insert( df, 'TEST')
		LOG.info("end")

	def trading( self, signal, price ):
		if signal['currency'] != self.currency :
			return
		LOG.info("start "+self.currency)

		#get recent order and balance
		sql = "select * from TEST where exchanger='"+self.exchanger+"' and currency='"+self.currency+"' order by test_serial desc limit 1"
		df_order = db.select(sql )
		if df_order.empty == False :
			df_order = df_order.iloc[0]
		LOG.debug("currency balance=>"+str(self.crypto_balance)+ " krw=>"+str(self.krw_balance))

		if signal['up_50_cross'] == '1':
			self.buy( df_order, price )
		elif signal['down_50_cross'] == '1':
			self.sell( df_order, price )

class Trade( ):
	def __init__( self, currency, exchanger, feeRate, min_order ):
		self.currency = currency
		self.feeRate = feeRate
		self.exchanger = exchanger
		self.min_order = min_order

	def buy( self, dict_order, price, krw_balance ):
		holding = False
		if len(dict_order) > 0 and dict_order['type'] != 'bid':
			LOG.warn("already sell. type="+ dict_order['type'] )
			return
		if len(dict_order) > 0 and dict_order['type'] == 'bid':
			holding = True

		fee = price*self.feeRate
		min_pay = self.min_order * (price + fee)

		if self.krw_balance < min_pay :
			LOG.error("not enough money. krw=>"+ str(self.krw_balance) + " "+self.currency+"=>"+ str(min_pay ) )
			return
		if self.krw_balance < min_pay :
			LOG.error("not enough money. krw=>"+ str(krw_balance) + " "+self.currency+"=>"+ str(min_pay ) )
			return

		fee = price*self.feeRate
		qty = self.krw_balance / (price + fee )

		url = 'https://api.coinone.co.kr/v2/order/limit_buy/'
		payload = {
				"access_token": co.ACCESS_TOKEN,
				'currency': self.currency
				}
		payload['qty'] = qty
		payload['price'] = price

		LOG.info("krw=>"+ str(krw_balance) + " "+self.currency+"=>"+ str(price ) )
		LOG.info("qty=>"+ str(qty) )

		result = co.post(url, payload)
		if result is None:
			return

		if result['result'] == 'success':
			df = pd.DataFrame()
			df['exchanger'] = self.exchanger
			df['date'] = get_time()
			df['currency'] = self.currency
			df['type'] = 'bid'
			df['price'] = price
			df['qty'] = qty
			df['feeRate'] = self.feeRate
			df['fee'] = fee
			df['order_id'] = result['orderId']
			db.insert( df, 'ORDERS')

		LOG.info("end buy")


	def sell( self, dict_order, price, balance ):
		if len(dict_order) < 1 :
			LOG.warn("order is empty")
			return
		if dict_order['type'] != 'bid':
			LOG.warn("last order is "+ dict_order['type'] )
			return

		decision = price - (dict_order['price'] + dict_order['fee'] )
		if decision >= 0 :
			LOG.info("sell wait!! price="+ str(price) + " decision="+str(decision))
			return
		url = 'https://api.coinone.co.kr/v2/order/limit_sell/'
		payload = {
				"access_token": co.ACCESS_TOKEN,
				'currency': self.currency
				}
		payload['qty'] = dict_order['qty']
		payload['price'] = price

		LOG.info("qty=>"+ str(qty) + " "+self.currency+"=>"+ str(price ) )

		result = co.post(url, payload)
		if result is None:
			return

		if result['result'] == 'success':
			df = pd.DataFrame()
			df['exchanger'] = self.exchanger
			df['date'] = get_time()
			df['currency'] = self.currency
			df['type'] = 'ask'
			df['price'] = price
			df['qty'] = dict_order['qty']
			df['feeRate'] = self.feeRate
			fee = price * self.feeRate
			df['fee'] = fee
			df['order_id'] = result['orderId']
			db.insert( df, 'ORDERS')
		LOG.info("end")

	def trading( self, signal, price ):
		if signal['currency'] != self.currency :
			return
		LOG.info("start "+self.currency)

		#get recent order
		url = 'https://api.coinone.co.kr/v2/order/complete_orders/'
		payload = {
				"access_token": co.ACCESS_TOKEN,
				"currency": self.currency
				}

		df_order = co.post(url, payload)
		if df_order is None:
			return

		if df_order['result'] != 'success':
			LOG.error( url + " Fail code=>"+result['errorCode'])
			return
		order = []
		if len(df_order['completeOrders']) > 0 :
			order = df_order[0] # recent order

		#get balance
		balance = 0.0
		krw_balance = 0

		url = 'https://api.coinone.co.kr/v2/account/balance/'
		payload = {
				"access_token": co.ACCESS_TOKEN,
				'currency': self.currency
				}
		content = co.post( url, payload )
		if content is None:
			return

		if content['result'] == 'success':
			if content[ self.currency ] :
				balance = float(content[self.currency]['avail'])
				krw_balance = int(content['krw']['avail'])
		LOG.debug("balance=>"+str(balance)+ " krw=>"+str(krw_balance))

		if signal['up_50_cross'] == '1':
			self.buy( order, price, krw_balance )
		elif signal['down_50_cross'] == '1':
			self.sell( order, price, balance )





