#import modules.coinone as co
import modules.trade as tr
import modules.crawl as cr
import pandas as pd
import signal, os
import sys, traceback
from modules.Logger import *
import argparse
#https://github.com/thesharp/daemonize
from daemonize import Daemonize

currency = 'xrp'
pid = '/root/TRADER/robot.pid'
exchanger = 'coinone'
feeRate = 0.002
min_order = 1 #minimum order quentity
currencies = ["btc", "bch", "eth", "etc", "xrp", "qtum", "iota", "ltc", "btg"]

parser = argparse.ArgumentParser( )
parser.add_argument('-d', help='daemon', action="store_true"  )
parser.add_argument('-t', help='test trade', action="store_true"  )
parser.add_argument('-k', help='test init krw asset', type=int )
parser.add_argument('-s', help='seconds', type=int )
args = parser.parse_args()

def main():
	try :
		krw = 0
		if args.k:
			krw = args.k

		secs = 0
		if args.k:
			secs = args.s
			LOG.info("seconds="+str(secs) )

		if args.t:
			LOG.info("Start Test init krw asset="+str(krw) )
			crawl = cr.Crawl( secs, currency, currencies, exchanger, feeRate, min_order, isTest=True, krw=krw )
			crawl.run()
		else:
			crawl = cr.Crawl( secs, currency, currencies, exchanger, feeRate )
			crawl.run()

	except Exception as e:
		LOG.critical( "Exceptions=>"+str(e) )
		LOG.exception( str(e) )

	LOG.critical( "robot end")

if __name__ == "__main__":
	level = "debug"
	path = "/root/TRADER"
	fh = init_logger( path, level, "robot" )
	keep_fds = [fh.stream.fileno()]
	printLargeTitle("Start robot coinone!! currency="+currency)

	if args.d:
		print("Start Deamon")
		LOG.info("Start Daemon")
		daemon = Daemonize( app='robot', pid=pid, action=main, keep_fds=keep_fds, logger=LOG )
		daemon.start()
	else:
		main()
