import modules.db as db
import pandas as pd
from modules.Logger import *

#db.connect()
level = "debug"
path = "/root/TRADER"
init_logger( path, level, "db_test")
df = db.select("select * from INFO")
print( df )