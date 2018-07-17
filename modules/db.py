#https://www.tutorialspoint.com/python3/python_database_access.htm

from modules.Logger import *
import pandas as pd
from sqlalchemy import create_engine
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb

user = 'ywoh'
pw = 'open'
db = 'stock'                   

def connect() :
	engine = create_engine("mysql+mysqldb://"+user+":"+pw+"@localhost:3306/"+db)
	conn = engine.connect()
	conn.close()

def insert( df, table ) :
	LOG.info("start insert!")
	LOG.debug( df.to_string() )
	try : 
		engine = create_engine("mysql+mysqldb://"+user+":"+pw+"@localhost:3306/"+db)
		conn = engine.connect()    
		df.to_sql( name=table, con=engine, if_exists='append', index=False)
		LOG.info("end insert!")
	except Exception as e:
		LOG.error("db insert fail" + str(e) )
		LOG.error( str(e) )
		raise e
	finally:
		conn.close()

def select( query, index=None ):
	LOG.info("start select!")
	try : 
		engine = create_engine("mysql+mysqldb://"+user+":"+pw+"@localhost:3306/"+db)
		conn = engine.connect()    

		if index is None:
			df = pd.read_sql( query, conn )
		else :
			df = pd.read_sql( query, conn,index_col=index )
		LOG.info("end Select")
		LOG.debug(query)
	except Exception as e:
		LOG.error("db select fail" + str(e) )
		raise e
	finally :
		conn.close()
	LOG.debug( df.to_string() )
	return df



