#Logger.py 

import os
import logging
import logging.handlers

LOG = logging.getLogger("process");

def init_logger(path,level,logname,logtype = "all"):
		
    global LOG

# set formatter
    formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s (%(filename)-12s, [%(funcName)s]-%(lineno)2s) : %(message)s ')
    #formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s (%(filename)-15s, [%(funcName)s] %(lineno)2s) : %(message)s ')
    path = os.path.join(path,"log")
# log dir check
    if not os.path.isdir(path):
        os.makedirs(path)

    # set log file
    file = path + "/" + logname + ".log"

    fileMaxIndex = 10
    fileMaxByte  = 1024 * 1024 * 50 #50MB

    # set handler
    rotateHandler = logging.handlers.RotatingFileHandler(file, maxBytes=fileMaxByte, backupCount=fileMaxIndex)
    # set formatter
    rotateHandler.setFormatter(formatter)
    # add handler
    LOG.addHandler(rotateHandler)

    # set logger level
    if level == 'debug':
        LOG.setLevel(logging.DEBUG)
    elif level == 'info':
        LOG.setLevel(logging.INFO)
    elif level == 'warning':
        LOG.setLevel(logging.WARNING)
    elif level == 'error':
        LOG.setLevel(logging.ERROR)
    elif level == 'critical':
        LOG.setLevel(logging.CRITICAL)
    else :# default warning
        LOG.setLevel(logging.WARNING)
    return rotateHandler
	
#	LOG.debug("debug")
#	LOG.info("info")
#	LOG.warning("warning")
#	LOG.error("error")
#	LOG.critical("critical")

LINE = "-"*80
LINE2 = "="*80
def printTitle(title):
	LOG.info(" ")
	LOG.info(LINE)
	LOG.info("<" + title + ">")
	LOG.info(LINE)

def printTerminateMsg(msg, bReturn=True):
	LOG.info(" ")
	LOG.info("  !! " + msg + " !!")
	if bReturn:
		printTitle("Abnormal TERMINATION")

def printLargeTitle(title):
	LOG.info(" ")
	LOG.info(LINE2)
	LOG.info("\t### " + title + " ###")
	LOG.info(LINE)
