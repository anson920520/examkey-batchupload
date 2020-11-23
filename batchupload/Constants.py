# SMS
import os

from pyDes import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# MYSQL_URL = "mysql+pymysql://root:134679852@127.0.0.1/hkappraisal_ESG?charset=utf8mb4"
MYSQL_URL = "mysql+pymysql://admin:dCF6bgKsgCQ6UCKJD267uwd9wsVAv7s9eD42@mysql-dev.cmxlm4alocmn.ap-southeast-1.rds.amazonaws.com/exam"
REDIS_URL = "redis://:@localhost:6379/7" #部署後重新開啟

JWT_KEYS = "CHINIJIADAMILE"


host = "mysql-dev.cmxlm4alocmn.ap-southeast-1.rds.amazonaws.com"
port = 3306
user = "admin"
password = "dCF6bgKsgCQ6UCKJD267uwd9wsVAv7s9eD42"
dbname = "exam"

ENCRY_UTIL = des(b"DESCRYPT", CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)

ERRCODE = 99999
#过期时长1小时
S_JMQ = Serializer(JWT_KEYS,expires_in=3600)

#用户状态码
UNFREEZE = 1
FREEZE = 0
