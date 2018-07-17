import simplejson as json
import time
import datetime
import modules.coinone as co
import modules.db as db
import modules.trade as tr
import pandas as pd
import tzlocal 
from modules.Logger import *
from stockstats import *
from collections import defaultdict

class Crawl( ):
	def __init__(self, secs,currency, currencies, exchanger, feeRate, min_order=0, isTest=False, krw=0 ):
		self.secs = secs
		#self.currencies = ["btc", "bch", "eth", "etc", "xrp", "qtum", "iota", "ltc", "btg"]
		self.exchanger = exchanger
		self.currencies = currencies
		self.MAX_VOLUME_RATE = 0.1
		self.MAX_PRICE_RATE = 0.005
		self.MIN_VOLUME = 6 * secs #per seconds * one tick

		self.dictPrice = defaultdict(list)
		self.dictVolume = defaultdict(list)
		self.signal_short = defaultdict(str) #short 15 key - currency, value=position( none, under, over )
		self.signal_long = defaultdict(str) #short 50 key - currency, value=position( none, under, over )

		self.status = 'None' #status, None, monitoring_buy, buy, monitoring_sell, sell
		self.status_tick = 2 # monitoring count ticker
		self.isTest = isTest
		if isTest == True:
			self.trade = tr.TestTrade( krw, currency, exchanger, feeRate, min_order )
		else:
			self.trade = tr.Trade( currency, exchanger, feeRate, min_order)


	def getRecentOrder(self, currency, period):
		url = "https://api.coinone.co.kr/trades/?currency="+currency+"&period="+period
		result = co.get(url);
		df = pd.DataFrame( result['completeOrders'] )    # completeOrder is list
		#df.info()

		local_timezone = tzlocal.get_localzone()  # local time이 설정되어 있는 지 확인.
		df = df.tail(1)
		test = lambda x: datetime.datetime.fromtimestamp( int( x ), local_timezone  ).strftime('%Y-%m-%d %H:%M:%S')

		df['timestamp'] = df['timestamp'].apply( test )         
		df = df.set_index( 'timestamp' ) # index 변경
		LOG.debug( df.to_string() )                

	def sma(self, tmpList, duration):
		if duration > 50 :
			del tmpList[0:len(tmpList)-duration]

		if len(tmpList) >= duration :
			tmp = tmpList[-duration:]
			LOG.debug( "sum=>"+str(sum(tmp))+" duration=>"+str(duration)  )
			return int( sum(tmp) /duration ) 
		else :
			return 0

	def rate(self, tmpList):
		if len(tmpList) > 2 :
			del tmpList[0:len(tmpList)-2]
			#LOG.debug( "rate=>" + ''.join(tmpList ) )
			diff = tmpList[1] - tmpList[0] 
			if diff > self.MIN_VOLUME :
				return diff/tmpList[0] * 100
		return 0

	def stockIndex(self, result):
		LOG.info("start stockIndex")
		LOG.info( self.dictPrice.keys() )

		for i in self.currencies:
			tmpList = self.dictPrice[i].append( int(result[i]['last']) )
			result[i]['sma_50'] = self.sma( self.dictPrice[i], 50)
			result[i]['sma_15'] = self.sma( self.dictPrice[i], 15)
			result[i]['sma_5'] = self.sma( self.dictPrice[i], 5)
			self.dictVolume[i].append( float(result[i]['volume']) )
			result[i]['volume_rate'] = self.rate( self.dictVolume[i] )

		LOG.info("end stockIndex")

	#to do choose cryptocurrency
	def getSignal( self, date, result ):
		LOG.info("start getSignal")

		tmpList = []
		signal = False
		action = '' # buy, sell

		for i in self.currencies:
			signal = False
			action = '' # buy, sell
			tmpDict = {'':''}
			tmpDict['exchanger'] = self.exchanger
			tmpDict['date'] = date
			tmpDict['currency'] = i
			LOG.debug( "sma_5=>"+ str(result[i]['sma_5']) )
			LOG.info(" sma_15=>"+ str(result[i]['sma_15']) +" sma_50=>"+ str(result[i]['sma_50']) )
			LOG.info(" volume_rate=>"+str(result[i]['volume_rate']) )
			LOG.debug("signal currency=>"+ i + " 10_position=>"+ self.signal_short[i] + " 15_position=>"+ self.signal_long[i] )

			if result[i]['volume_rate'] is not None:
				if result[i]['volume_rate'] > self.MAX_VOLUME_RATE:
					tmpDict['volume_signal'] = '1'
					signal = True
				else:
					tmpDict['volume_signal'] = '0'

			if result[i]['sma_15'] > 0 and result[i]['sma_5'] > 0 :
				if self.signal_short[i] == '' :
					if result[i]['sma_5'] < result[i]['sma_15'] :
						self.signal_short[i] = 'under';
					elif result[i]['sma_5'] > result[i]['sma_15'] :
						self.signal_short[i] = 'over';
				else:
					if self.signal_short[i] == 'under':
						if result[i]['sma_5'] > result[i]['sma_15'] :
							self.signal_short[i] = 'over'
							tmpDict['up_cross'] = '1'
							tmpDict['down_cross'] = '0'
							signal = True
					elif self.signal_short[i] == 'over':
						if result[i]['sma_5'] < result[i]['sma_15'] :
							self.signal_short[i] = 'under'
							tmpDict['down_cross'] = '1'
							tmpDict['up_cross'] = '0'
							signal = True

			if result[i]['sma_50'] > 0 and result[i]['sma_15'] > 0 :
				if self.signal_long[i] == '' :
					if result[i]['sma_15'] < result[i]['sma_50'] :
						self.signal_long[i] = 'under';
					elif result[i]['sma_15'] > result[i]['sma_50'] :
						self.signal_long[i] = 'over';
				else:
					if self.signal_long[i] == 'under':
						if result[i]['sma_15'] > result[i]['sma_50'] and \
								result[i]['sma_5'] > result[i]['sma_15'] and \
								int(result[i]['last']) > result[i]['sma_5']    :
							self.signal_long[i] = 'over'
							tmpDict['up_50_cross'] = '1'
							tmpDict['down_50_cross'] = '0'
							signal = True

							if tmpDict['currency'] == 'xrp': #to do
								self.trade.trading( tmpDict, int(result[i]['last'] ) )
					elif self.signal_long[i] == 'over':
						if result[i]['sma_15'] < result[i]['sma_50'] and \
								int(result[i]['last']) < result[i]['sma_15'] :
							self.signal_long[i] = 'under'
							tmpDict['up_50_cross'] = '0'
							tmpDict['down_50_cross'] = '1'
							signal = True

							if tmpDict['currency'] == 'xrp': #to do
								self.trade.trading( tmpDict, int(result[i]['last'] ) )
			if signal == True :
				del tmpDict['']
				tmpList.append(tmpDict)



		if len(tmpList) > 0 :
			df = pd.DataFrame( tmpList )
			LOG.debug( "df=>"+ df.to_string() )
			db.insert( df, "STOCK_SIGNAL" )

		LOG.info("end")


	def getPrice(self, currency ):
		LOG.info("start getprice")
		url = "https://api.coinone.co.kr/ticker/?currency="+currency
		result = co.get(url);

		if result is None :
			LOG.error( url+" api server fail" )
			return None                  

		if result['result'] != 'success':
			LOG.error( url+" Fail code=>"+result['errorCode'] )
			return None                  

		LOG.debug( "Response=>"+ str(json.dumps(result, sort_keys=True, indent=4) ) )        

		local_timezone = tzlocal.get_localzone()  # local time이 설정되어 있는 지 확인.        
		date = datetime.datetime.fromtimestamp( int( result['timestamp'] ), local_timezone  ).strftime('%Y-%m-%d %H:%M:%S')       
		if currency == 'all':

			# calculate sma and volume rate
			self.stockIndex( result )

			self.getSignal( date, result )

			#make df for db insert
			tmpList = []
			for i in self.currencies:
				tmpList.append( result[i] )

			df = pd.DataFrame( tmpList )    # list to dataframe            

			df['timestamp'] = result['timestamp']
			df['errorCode'] = result['errorCode']
			df['result'] = result['result']    
			LOG.debug( df.to_string() )    
		else :
			df = pd.DataFrame( result, index=[0] )    # dict to dataframe                        

		df['exchanger'] = self.exchanger
		df['date'] = date 

		LOG.debug( df.to_string() )        
		LOG.info( "end getprice" )        
		return df                

	def crawl(self ):
		LOG.info("Start crawling")
		df = self.getPrice( 'all' )

		if df is not None :
			#write db
			db.insert( df, 'INFO')
		LOG.info("End crawling")

	def run( self ):                
		LOG.critical("Start")
		while True:
			self.crawl( )
			time.sleep( self.secs )
		LOG.critical("End")

