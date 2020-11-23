import datetime
import re
import uuid
import pandas as pd
import chardet
from flask import Blueprint, request

from utils import Utils

from Constants import ERRCODE
from dbconnect import engine
from Msgs import ASocMessage
from sqlalchemy.orm import sessionmaker

from question.questions import create_mc_questions, create_sq_questions, create_pf_questions

up_api = Blueprint('upload', __name__)

#上传问题 旧的写法  采用分割符逗号获取数值
# @up_api.route('/', methods=["POST"])
# # @Utils.is_adminuser_header
# def company_child():
#     file = request.files['file']
#     action = request.form.get("action")
#     topic = request.form.get("topic")
#     topic_name = request.form.get("topic_name")
#     subject = request.form.get("subject")
#     subject_name = request.form.get("subject_name")
#     subtopic = request.form.get("subtopic")
#     subtopic_name = request.form.get("subtopic_name")
#     language = request.form.get("language")
#
#     if not file:
#         return "No file"
#     file_contents = file.stream.read()
#     msg = chardet.detect(file_contents)['encoding']
#     if msg == 'GBK':
#         file_contents = file_contents.decode("GBK")
#     elif msg == 'UTF-8':
#         file_contents = file_contents.decode("UTF-8")
#     elif msg == 'GB2312':
#         file_contents = file_contents.decode("GBK")
#     elif msg == 'UTF-8-SIG':
#         file_contents = file_contents.decode("UTF-8-SIG")
#     elif msg == 'ascii':
#         file_contents = file_contents.decode("ascii")
#     elif msg == 'ISO-8859-1':
#         file_contents = file_contents.decode("ISO-8859-1")
#
#     result = Utils.transform(file_contents)
#     #print(result)
#    # print(type(result))
#     rows = result.split("\r\n")
#    # print(rows)
#    # print(len(rows))
#     i = 0
#     error_list = []
#     haved_list = []
#     while i < len(rows):
#         if i == 0:
#             i += 1
#             continue
#         #print("一行数据=======================")
#         #print(rows[i])
#
#         #过滤第一行的标题
#         if rows[i] == '':
#             i += 1
#             continue
#
#         #过滤情况为每行出现,,,,, 的情况
#         row_match = re.match(r'^,*', rows[i]).group()
#         if row_match:
#             i += 1
#             continue
#
#         rows_list = rows[i].split(",")
#
#         #print(rows_list[1])
#         #选择对应的批量导入数据
#
#         if action == "MC":
#             select_answer = {
#                 "A":rows_list[3],
#                 "B":rows_list[4],
#                 "C":rows_list[5],
#                 "D":rows_list[6]
#             }
#             data = {
#                 "topic":topic,"topic_name":topic_name,"subject":subject,
#                 "subject_name":subject_name,"subtopic":subtopic,
#                 "subtopic_name":subtopic_name,"language":language,
#                 "difficulty":rows_list[0],"instruction":rows_list[1],
#                 "text": rows_list[2], "items": select_answer,
#                 "model_answer":rows_list[7],"explanation":rows_list[8]
#             }
#             res = create_mc_questions(data)
#         elif action == "SQ":
#             data = {
#                 "topic": topic, "topic_name": topic_name, "subject": subject,
#                 "subject_name": subject_name, "subtopic": subtopic,
#                 "subtopic_name": subtopic_name, "language": language,
#                 "difficulty": rows_list[0], "instruction": rows_list[1],
#                 "text": rows_list[2], "model_answer": rows_list[3],
#                 "keyword_count":rows_list[4],"explanation": rows_list[5]
#             }
#             res = create_sq_questions(data)
#         elif action == "PF":
#             data = {
#                 "topic": topic, "topic_name": topic_name, "subject": subject,
#                 "subject_name": subject_name, "subtopic": subtopic,
#                 "subtopic_name": subtopic_name, "language": language,
#                 "difficulty": rows_list[0], "instruction": rows_list[1],
#                 "text": rows_list[2], "model_answer1": rows_list[3],
#                 "keyword_count1": rows_list[4], "model_answer1_title":rows_list[5],
#                 "model_answer2": rows_list[6],
#                 "keyword_count2": rows_list[7], "model_answer2_title": rows_list[8],
#                 "explanation": rows_list[9]
#             }
#             res = create_pf_questions(data)
#
#         else:
#             return {"code":400,"message":"action参数不存在"}
#
#
#         if res["code"] == 500:
#             error_list.append(rows[i][0:])
#         # if code == 2:
#         #     haved_list.append(rows[i][0:])
#         #     print("数据重复")
#         i += 1
#     if len(error_list) == 0:
#         data = {"code":200,"msg": "导入成功","重复列表": haved_list}
#         return ASocMessage.truemsg(data)
#     if len(error_list) != 0:
#         data = {"code": ERRCODE,"msg":"导入失败","data":error_list,"重复列表不存在": haved_list}
#         return ASocMessage.truemsg(data)



#新上传方式， pandas采用了read_csv，如果后续觉得 这种上传方式比较好，建议可以替代以前写的旧的api接口
@up_api.route('/', methods=['post'], strict_slashes=False)
def synchronize():
    file = request.files['file']
    action = request.form.get("action")
    topic = request.form.get("topic")
    topic_name = request.form.get("topic_name")
    subject = request.form.get("subject")
    subject_name = request.form.get("subject_name")
    subtopic = request.form.get("subtopic")
    subtopic_name = request.form.get("subtopic_name")
    language = request.form.get("language")

    if not file:
        return "No file"
    file_contents = pd.read_csv(file,encoding='gbk')
    rows = file_contents.values
    # file_contents = file.stream.read()
    # msg = chardet.detect(file_contents)['encoding']
    # if msg == 'GBK':
    #     file_contents = file_contents.decode("GBK")
    # elif msg == 'UTF-8':
    #     file_contents = file_contents.decode("UTF-8")
    # elif msg == 'GB2312':
    #     file_contents = file_contents.decode("GBK")
    # elif msg == 'UTF-8-SIG':
    #     file_contents = file_contents.decode("UTF-8-SIG")
    # elif msg == 'ascii':
    #     file_contents = file_contents.decode("ascii")
    # elif msg == 'ISO-8859-1':
    #     file_contents = file_contents.decode("ISO-8859-1")

    i = 0
    error_list = []
    haved_list = []
    while i < len(rows):

        if action == "MC":
            select_answer = {
                "A": rows[i][3],
                "B": rows[i][4],
                "C": rows[i][5],
                "D": rows[i][6]
            }
            data = {
                "topic": topic, "topic_name": topic_name, "subject": subject,
                "subject_name": subject_name, "subtopic": subtopic,
                "subtopic_name": subtopic_name, "language": language,
                "difficulty": rows[i][0], "instruction": rows[i][1],
                "text": rows[i][2], "items": select_answer,
                "model_answer": rows[i][7], "explanation": rows[i][8]
            }
            text = rows[i][2]
            res = create_mc_questions(data)
        elif action == "SQ":
            data = {
                "topic": topic, "topic_name": topic_name, "subject": subject,
                "subject_name": subject_name, "subtopic": subtopic,
                "subtopic_name": subtopic_name, "language": language,
                "difficulty": rows[i][0], "instruction": rows[i][1],
                "text": rows[i][2], "model_answer": rows[i][3],
                "keyword_count": rows[i][4], "explanation": rows[i][5]
            }
            text = rows[i][2]
            res = create_sq_questions(data)
        elif action == "PF":
            data = {
                "topic": topic, "topic_name": topic_name, "subject": subject,
                "subject_name": subject_name, "subtopic": subtopic,
                "subtopic_name": subtopic_name, "language": language,
                "difficulty": rows[i][0], "instruction": rows[i][1],
                "text": rows[i][2], "model_answer1": rows[i][3],
                "keyword_count1": rows[i][4], "model_answer1_title": rows[i][5],
                "model_answer2": rows[i][6],
                "keyword_count2": rows[i][7], "model_answer2_title": rows[i][8],
                "explanation": rows[i][9]
            }
            text = rows[i][2]
            res = create_pf_questions(data)

        else:
            return {"code": 400, "message": "action参数不存在"}

        if res["code"] == 500:
            error_list.append(rows[i][0:])

        #重复数据
        # if res["code"] == 305:
        #     haved_list.append(text)
        #     print("数据重复")
        i += 1
    if len(error_list) == 0:
        data = {"code": 200, "msg": "导入成功", "重复question列表": haved_list}
        return ASocMessage.truemsg(data)
    if len(error_list) != 0:
        data = {"code": ERRCODE, "msg": "导入失败", "data": error_list, "重复列表不存在": haved_list}
        return ASocMessage.truemsg(data)




