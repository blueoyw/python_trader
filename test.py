#import modules.coinone as co
import modules.trade as tr
import modules.crawl as cr
import pandas as pd
import signal, os
import sys, traceback
from modules.Logger import *
#https://github.com/thesharp/daemonize
from daemonize import Daemonize

secs = 30
#secs = 5 #for test
currency = 'xrp'
pid = '/root/TRADER/robot.pid'
exchanger = 'coinone'
feeRate = 0.2
currencies = ["btc", "bch", "eth", "etc", "xrp", "qtum", "iota", "ltc", "btg"]

def main():
    try :
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

    args = sys.argv[1:]
    args_length = len(args)
    if args_length > 0 and args[0] == '-d':
    daemon = Daemonize( app='robot', pid=pid, action=main, keep_fds=keep_fds, logger=LOG )
    daemon.start()
    else:
main()
