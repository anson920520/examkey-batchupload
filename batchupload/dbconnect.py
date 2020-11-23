import pymysql
import redis
import sqlalchemy

from sqlalchemy.orm import sessionmaker

from Constants import MYSQL_URL

engine = sqlalchemy.create_engine(MYSQL_URL, isolation_level="AUTOCOMMIT")
session = sessionmaker(engine)
mysql_connection_for_db = session()

redis_connection = redis.Redis(host="119.3.150.173",port=6379,password="acarepro20!9",decode_responses=True)
redis_connection_for_user = redis.Redis(host="119.3.150.173",port=6379,password="acarepro20!9",db=7, decode_responses=True)

host = "119.3.150.173"
port = 3306
user = "root"
password = "acarepro2019"
dbname = "hkappraisal_ESG"

# host = "127.0.0.1"
# port = 3306
# user = "root"
# password = "134679852"
# dbname = "hkappraisal_ESG"


ceshi_mysql_connection = pymysql.connect(host=host,port=port,user=user,password=password,db=dbname)
print(ceshi_mysql_connection)
ceshi_mysql_connection_cur = ceshi_mysql_connection.cursor()

