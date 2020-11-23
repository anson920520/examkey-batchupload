import datetime

from sqlalchemy.orm import sessionmaker

from batchupload.dbconnect import engine
from models import McQuestion,shortquestion,proofreading


def create_mc_questions(data):
    session = sessionmaker(engine)
    mysql_connection = session()

    # topic = Column(INTEGER(10))
    # topic_name = Column(String(255))
    # subject = Column(INTEGER(10))
    # subject_name = Column(String(255))
    # subtopic = Column(INTEGER(11))
    # subtopic_name = Column(String(255))
    # language = Column(String(255))
    # difficulty = Column(INTEGER(10))
    # instruction = Column(Text)
    # text = Column(Text)
    # model_answer = Column(Text)
    # explanation = Column(Text)
    # items = Column(JSON)
    # create_at = Column(String(255))
    # edited_at = Column(String(255))
    # delete_at = Column(String(255))

    # 检查重复text
    # row = mysql_connection.query(McQuestion).filter_by(text=data['text']).first()
    # if row:
    #     return {"code":305,"data": {"msg": "question重复"}}

    try:
        created_at = datetime.datetime.now()
        dates = McQuestion(
            topic=data['topic'],
            topic_name=data['topic_name'],
            subject=data['subject'],
            subject_name=data['subject_name'],
            subtopic=data['subtopic'],
            subtopic_name=data['subtopic_name'],
            language=data['language'],
            difficulty=data['difficulty'],
            instruction=data['instruction'],
            text=data['text'],
            model_answer=data['model_answer'],
            explanation=data['explanation'],
            items=data['items'],
            created_at=created_at,
        )

        mysql_connection.add(dates)
        mysql_connection.flush()
        # 返回主鍵PK
        # userId = dates.id
        # print(userId)
        mysql_connection.commit()
    except Exception as e:
        print(e)
        return {"code": 500, "data": {"msg": "question創建失败"}}


    finally:
        mysql_connection.close()

    return {"code": 200, "data": {"msg": "分類創建成功"}}





def create_sq_questions(data):
    session = sessionmaker(engine)
    mysql_connection = session()
    # 检查重复text
    # row = mysql_connection.query(shortquestion).filter_by(text=data['text']).first()
    # if row:
    #     return {"code": 305, "data": {"msg": "question重复"}}


    try:
        created_at = datetime.datetime.now()
        dates = shortquestion(
            topic=data['topic'],
            topic_name=data['topic_name'],
            subject=data['subject'],
            subject_name=data['subject_name'],
            subtopic=data['subtopic'],
            subtopic_name=data['subtopic_name'],
            language=data['language'],
            difficulty=data['difficulty'],
            instruction=data['instruction'],
            text=data['text'],
            model_answer=data['model_answer'],
            explanation=data['explanation'],
            keyword_count=data['keyword_count'],
            created_at=created_at,
        )

        mysql_connection.add(dates)
        mysql_connection.flush()
        # 返回主鍵PK
        # userId = dates.id
        # print(userId)
        mysql_connection.commit()
    except Exception as e:
        print(e)
        return {"code": 500, "data": {"msg": "question創建失败"}}


    finally:
        mysql_connection.close()

    return {"code": 200, "data": {"msg": "分類創建成功"}}


def create_pf_questions(data):
    session = sessionmaker(engine)
    mysql_connection = session()

    #检查重复text
    # row = mysql_connection.query(proofreading).filter_by(text=data['text']).first()
    # if row:
    #     return {"code": 305, "data": {"msg": "question重复"}}


    try:
        created_at = datetime.datetime.now()
        dates = proofreading(
            topic=data['topic'],
            topic_name=data['topic_name'],
            subject=data['subject'],
            subject_name=data['subject_name'],
            subtopic=data['subtopic'],
            subtopic_name=data['subtopic_name'],
            language=data['language'],
            difficulty=data['difficulty'],
            instruction=data['instruction'],
            text=data['text'],
            model_answer1=data['model_answer1'],
            model_answer1_title=data['model_answer1_title'],
            keyword_count1=data['keyword_count1'],
            model_answer2=data['model_answer2'],
            model_answer2_title=data['model_answer2_title'],
            keyword_count2=data['keyword_count2'],
            explanation = data['explanation'],
            created_at=created_at,
        )

        mysql_connection.add(dates)
        mysql_connection.flush()
        # 返回主鍵PK
        # userId = dates.id
        # print(userId)
        mysql_connection.commit()
    except Exception as e:
        print(e)
        return {"code": 500, "data": {"msg": "question創建失败"}}


    finally:
        mysql_connection.close()

    return {"code": 200, "data": {"msg": "分類創建成功"}}