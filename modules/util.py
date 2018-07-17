import datetime, time
from modules.Logger import *

class TestError(Exception):
    pass

#should follow date format '%Y-%m-%d %H:%M:%S' to insert datatime to DB
def get_time():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    LOG.debug( now )
    return now


