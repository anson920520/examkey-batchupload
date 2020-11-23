import datetime
import decimal
import hashlib
import io
import json
import os
import time
import urllib

import pymysql
import requests
import sqlalchemy
import xlsxwriter as xlsxwriter


from functools import wraps

from http.client import HTTPConnection
from urllib.parse import urlencode

from flask import session, request, g
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker

#from Constants import SMS_HOST, SMS_SEND_URI, SMS_PASSWORD, SMS_ACOUNT, SALT_ONE, SALT_TWO, ENCRY_UTIL, APPID, SECRET, \
    #WX_ACCESS_TOKEN, ORDER_CANCEL, XCX_APPID
from Msgs import Message
from dbconnect import  redis_connection, engine
from models import *
from flask.json import JSONEncoder
from datetime import date

class Utils:

    def timeS(self,data):
        timeArray = time.strptime(data, "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def timeD(self,data):
        dateArray = datetime.datetime.fromtimestamp(data)
        otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        return otherStyleTime

    # 本月第一天到最后一天时间搓
    def timeMonth(self):
        now = datetime.datetime.now()
        # 每月新增会员
        this_month_start = datetime.datetime(now.year, now.month, 1)
        this_month_start = this_month_start.strftime('%Y-%m-%d')
        time_start = self.timeS(this_month_start)
        this_month_end = datetime.datetime(now.year, now.month + 1, 1) - datetime.timedelta(
            days=1) + datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        this_month_end = this_month_end.strftime('%Y-%m-%d')
        time_end = self.timeS(this_month_end)
        return time_start, time_end

    # 上个月的第一天---最后一天时间搓
    def lastMonth(self):
        now = datetime.datetime.now()
        this_month_start = datetime.datetime(now.year, now.month, 1)
        last_month_end = this_month_start - datetime.timedelta(days=1) + datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
        last_month_end = last_month_end.strftime('%Y-%m-%d')
        last_month_start = last_month_start.strftime('%Y-%m-%d')
        time_end = self.timeS(last_month_end)
        time_start = self.timeS(last_month_start)
        return time_start, time_end



    #管理员用户验证token
    def is_adminuser_header(func):
        @wraps(func)
        def haveuser(*args, **kwargs):
            try:
                token = request.headers["Authorization"]
            except Exception as e:
                return Message.errormsg("本功能需要管理端權限！", 420)
            #print("装饰器token=======")
            #print(token)
            #print(type(token))
            admin = admin_user.verify_auth_token(token)
            #print("admini_user=======")
            #print(admin)
            if admin:
                if admin == 1:

                    return Message.errormsg("token已过期，请重新登陆获取",60000)
                else:
                    return func(*args, **kwargs)
            else:
                return Message.errormsg("本功能需要管理端權限！", 420)
        return haveuser


    #子公司用户验证token
    def is_companystaffuser_header(func):
        @wraps(func)
        def haveuser(*args, **kwargs):
            try:
                token = request.headers["Authorization"]
            except Exception as e:
                return Message.errormsg("本功能需要公司用戶權限！", 420)
            #print("装饰器token=======")
            #print(token)
           # print(type(token))
            company_user = company_staff_user.verify_auth_token(token)
            #print("admini_user=======")
            #print(company_user)
            if company_user:
                if company_user == 1:

                    return Message.errormsg("token已过期，请重新登陆获取",60000)
                else:
                    return func(*args, **kwargs)
            else:
                return Message.errormsg("本功能需要公司用戶權限！", 420)
        return haveuser

    #删除服务器中的文件数据
    def deletefile(file_path):
        if (os.path.exists(file_path)):
            try:
                os.remove(file_path)
            except Exception as e:
                #print(e)
                return 0
            return 1
        else:
            return 0

    # 移等换逗大法
    def transform(text_file_contents):
        result = text_file_contents.replace("=", ",")
        return result
    # 批量导入corporateInfo
    @staticmethod
    def store_mysql_by_session_info(data, cls,ty):
        session = sessionmaker(engine)
        mysql_connection = session()
        try:
            # if ty == "policy":
            #     new_model = cls(company_profile_id=data[0],policy=data[1],
            #                     implementation_example=data[2],createAt=data[3],uuid=data[4])
            #
            # elif ty == "evaluation":
            #     new_model = cls(company_profile_id=data[0],Internal_evaluation=data[1],
            #                     external_evaluation=data[2],createAt=data[3],uuid=data[4])
            # elif ty == "stakeholder":
            #     communication_channel = [
            #         {
            #             "man":data[0],
            #             "communication_channel":data[1],
            #             "expectations_demands":data[2],
            #             "response":data[3],
            #             "val":data[4]
            #         }
            #     ]
            #     new_model = cls(company_profile_id=data[0],communication_channel=communication_channel,
            #                     expectations_demands=data[2],response=data[3],createAt=data[5],uuid=data[6])

            if ty == "corporateInfo":
                new_model = mysql_connection.query(cls).filter_by(company_profile_id=data[0]).first()
                if new_model:
                    new_model.cigs_id = data[1]
                    new_model.business_coverage = data[2]
                    new_model.major_business = data[3]
                    new_model.trend = data[4]
                    new_model.total_employee = data[5]
                    new_model.sales_description = data[6]
                    new_model.chairman_word = data[7]
                    new_model.board_of_director = data[8]
                    new_model.esg_structure_info = data[9]
                    new_model.esg_management_policy = data[10]
                    new_model.updateAt = datetime.datetime.now()
                else:
                    new_model = cls(company_profile_id=data[0],cigs_id=data[1],
                                    business_coverage=data[2],major_business=data[3],trend=data[4],total_employee=data[5],
                                    sales_description=data[6],chairman_word=data[7],board_of_director=data[8],
                                    esg_structure_info=data[9],esg_management_policy=data[10],
                                    createAt=data[11],uuid=data[12])

            mysql_connection.add(new_model)
            mysql_connection.commit()
           # print("_____________________________")
            code = 1
        except Exception as e:
           # print(e)
            code = 0
            return code

        mysql_connection.close()
        return code

# 通用存表大法3
    @staticmethod
    def store_mysql_by_session_str(data, cls):
        #print("data====")
        #print(data)
        #print(type(data))
        new_model = cls(data)
        code = store_exe(new_model)
        return code

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()

            if isinstance(obj, datetime.datetime):
                print("捕捉到了datetime异常")
                return obj.strftime("%Y-%m-%d %H:%M:%S")

            if isinstance(obj, decimal.Decimal):
                return float(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
      # def default(self, o):
      #       if is instance(o, date):
      #           return o.isoformat()
      #
      #       return super().default(o)

def store_exe(model):
    session = sessionmaker(engine)
    mysql_connection = session()
    try:
        mysql_connection.add(model)
        mysql_connection.commit()
        return 1
    except sqlalchemy.exc.IntegrityError as e:
        #print(e)
        mysql_connection.rollback()
        return 2
    except Exception as e:
        #print(e)
        mysql_connection.rollback()
        return 0
    finally:
        mysql_connection.close()

