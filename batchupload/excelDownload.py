import datetime
import re
import uuid
from urllib.parse import quote

import chardet
from flask import Blueprint, request, make_response

from utils import Utils

from Constants import ERRCODE
from dbconnect import engine
from Msgs import ASocMessage
from sqlalchemy.orm import sessionmaker
from user.childCompany.child import *
from user.operationPoint.point import *

from models import company_child_company, company_operating_point, company_profile, \
    company_policy, company_evaluation, company_stakeholder, company_corporate_information,category

from admin.companyProfile.profile import getCompanyProfileDetail, getOperationPointDetail

down_api = Blueprint('download', __name__)


@down_api.route("/xls", methods=["POST","GET"])
# @Utils.isloginingby_get
def downloadxls():
    session = sessionmaker(engine)
    mysql_connection = session()
    json_data = request.args
    uuid = json_data.get("uuid")

    result = getCompanyProfileDetail(uuid)

    #生成表
    returnxls,filename = Utils.create_excel("母公司", result)
    filename=quote(filename)
    a = returnxls.getvalue()
    resp = make_response(a)
    returnxls.close()
    resp.headers["Content-Disposition"] = "attachment; filename*=utf-8''{}.xlsx".format(filename)
    resp.headers['Content-Type'] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    resp.headers["Cache-Control"] = "no-cache"
    mysql_connection.close()
    return resp


@down_api.route("/point_xls", methods=["POST","GET"])
# @Utils.isloginingby_get
def downloadxls2():
    session = sessionmaker(engine)
    mysql_connection = session()
    json_data = request.args
    uuid = json_data.get("uuid")

    result = getOperationPointDetail(uuid)

    #生成表
    returnxls,filename = Utils.create_point_excel("营运点资料", result)
    filename=quote(filename)
    a = returnxls.getvalue()
    resp = make_response(a)
    returnxls.close()
    resp.headers["Content-Disposition"] = "attachment; filename*=utf-8''{}.xlsx".format(filename)
    resp.headers['Content-Type'] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    resp.headers["Cache-Control"] = "no-cache"
    mysql_connection.close()
    return resp