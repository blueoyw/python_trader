#import modules.coinone as co
import modules.trade as tr
import modules.crawl as cr
import pandas as pd
import signal, os
import sys
from modules.Logger import *

currency = 'all'
threads = []
secs = 30
#secs = 5 #for test

class Stop(Exception):
    #to do
    LOG.critical('Stop exception' )
    pass

def handler(signum, frame):
    LOG.critical('Signal handler called with signal=>'+ str(signum) )
    raise Stop

def main():    
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    level = "debug"
    path = "/root/TRADER"
    init_logger( path, level, "robot" )
    printLargeTitle("Start robot coinone!! currency="+currency)    
    try :
        threads.append( cr.Crawl( secs ) ) # per 6 secs
        #threads.append( tr.Trade( 'btc', 5 ) )

        for t in threads:
            t.start()
    except Exception as e:
        LOG.critical( "Exceptions=>"+str(e) )
        for t in threads:
            t.shutdown_flag.set()

    for t in threads:
        t.join()
    LOG.critical( "robot end")

if __name__ == '__main__':
    main()
    
