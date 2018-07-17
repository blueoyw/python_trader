import pandas as pd
import time
import datetime as dt
from modules.util import *
from modules.Logger import *
from stockstats import *
import modules.db as db
import modules.coinone as co

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
		if len(dict_order) > 0 and dict_order['type'] != 'bid':
			LOG.warn("already sell. type="+ dict_order['type'] )
			return
		if len(dict_order) > 0 and dict_order['type'] == 'bid':
			holding = True

		min_pay = self.min_order * ( 1+ self.feeRate)
		if self.krw_balance < min_pay :
			LOG.error("not enough money. krw=>"+ str(self.krw_balance) + " "+self.currency+"=>"+ str(min_pay ) )
			return

		fee = price*self.feeRate
		qty = self.krw_balance / (price + fee )
		self.crypto_balance = qty
		self.krw_balance = self.krw_balance - qty*self.price

		now = get_time()
		df = pd.DataFrame()
		df['exchanger'] = self.exchanger
		df['date'] = now
		df['currency'] = self.currency
		df['type'] = 'bid'
		df['price'] = price
		df['qty'] = qty
		df['feeRate'] = self.feeRate
		df['fee'] = fee
		df['order_id'] = 'TEST_'+ now
		df['profit'] = 0
		df['balance'] = self.krw_balance
		df['crypto_balance'] = self.crypto_balance
		db.insert( df, 'TEST')

		LOG.info("end buy")


	def sell( self, dict_order, price ):
		if len(dict_order) < 1 :
			LOG.warn("order is empty")
			return
		if dict_order['type'] != 'bid':
			LOG.warn("last order is "+ dict_order['type'] )
			return

		decision = price - (dict_order['price'] + dict_order['fee'] )
		if decision >= 0 :
			LOG.info("not sell!! price="+ str(price) + " decision="+str(decision))
			return

		LOG.info("qty=>"+ str(dict_order['qty']) + " "+self.currency+"=>"+ str(price ) )
		qty = dict_order['qty']
		fee = qty*price*feeRate
		get = qty*price - fee

		profit = (price - dict_order['price']) / dict_order['price'] * 100

		self.krw_balance = self.krw_balance + get
		self.crypto_balance = self.crypto_balance - qty

		df = pd.DataFrame()
		now = get_time()
		df['exchanger'] = self.exchanger
		df['date'] = now
		df['currency'] = self.currency
		df['type'] = 'ask'
		df['price'] = price
		df['qty'] = dict_order['qty']
		df['feeRate'] = self.feeRate
		df['fee'] = fee
		df['order_id'] = 'TEST_'+ now
		df['profit'] = profit
		df['balance'] = self.krw_balance
		df['crypto_balance'] = self.crypto_balance
		db.insert( df, 'TEST')
		LOG.info("end")

	def trading( self, signal, price ):
		if signal['currency'] != self.currency :
			return
		LOG.info("start "+self.currency)

		#get recent order and balance
		sql = "select * from TEST where exchanger='"+self.exchanger+"' and currency='"+self.currency+"' order by test_serial desc limit 1"
		df_order = db.select(sql )

		LOG.debug("currency balance=>"+str(self.crypto_balance)+ " krw=>"+str(self.krw_balance))

		if signal['up_50_cross'] == '1':
			self.buy( order, price )
		elif signal['down_50_cross'] == '1':
			self.sell( order, price )





