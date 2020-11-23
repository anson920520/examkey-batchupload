# models.py中
import base64

from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Date, DateTime, Enum, Float, JSON, String, ForeignKey, DECIMAL, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT, VARCHAR, DOUBLE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


from Constants import JWT_KEYS, ENCRY_UTIL, S_JMQ
from dbconnect import engine

Base = declarative_base()
metadata = Base.metadata

#new models for this application
#---------------------------管理員與客戶帳戶處理--------------------------------#
class admin_user(Base):
    __tablename__ = "admin_user"

    id = Column(INTEGER(11),primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    createAt = Column(String(255))
    updateAt = Column(String(255))
    deleteAt = Column(String(255))

    def to_dict(self):
        column_name_list = [
            value[0] for value in self._sa_instance_state.attrs.items()
        ]
        return dict(
            (column_name, getattr(self, column_name, None)) \
            for column_name in column_name_list
        )

    @staticmethod
    def generate_auth_token(key_data, expiration=36000):
        key_data = base64.encodebytes(key_data)
        key_data = str(key_data, encoding="utf-8")

        return S_JMQ.dumps(key_data)

    @staticmethod
    def verify_auth_token(token):
        session = sessionmaker(engine)
        mysql_connection = session()

        try:
            data = S_JMQ.loads(token)
            print("data====")
            print(data)
            key_data = bytes(data, encoding="utf-8")
            key_data = base64.decodebytes(key_data)
            user_info_bytes = ENCRY_UTIL.decrypt(key_data)
            user_info = user_info_bytes.decode('utf-8')
            print("user_info========")
            print(user_info)
        except SignatureExpired:
            mysql_connection.close()
            return 1  # valid token, but expired
        except BadSignature:
            mysql_connection.close()
            return None  # invalid token
        user = mysql_connection.query(admin_user).filter_by(username=user_info
                                                            .split("&")[0]).first()
        print("admin_user===")
        mysql_connection.close()
        print(user)
        return user



class McQuestion(Base):
    __tablename__ = "mc_question"

    id = Column(INTEGER(11),primary_key=True)
    topic = Column(INTEGER(10))
    topic_name = Column(String(255))
    subject = Column(INTEGER(10))
    subject_name = Column(String(255))
    subtopic = Column(INTEGER(11))
    subtopic_name = Column(String(255))
    language = Column(String(255))
    difficulty = Column(INTEGER(10))
    instruction = Column(Text)
    text = Column(Text)
    model_answer = Column(Text)
    explanation = Column(Text)
    items = Column(JSON)
    created_at = Column(String(255))
    edited_at = Column(String(255))
    deleted_at = Column(String(255))
    
    def to_dict(self):
        column_name_list = [
            value[0] for value in self._sa_instance_state.attrs.items()
        ]
        return dict(
            (column_name, getattr(self, column_name, None)) \
            for column_name in column_name_list
        )


class proofreading(Base):
    __tablename__ = "proofreading_question"

    id = Column(INTEGER(11), primary_key=True)
    topic = Column(INTEGER(10))
    topic_name = Column(String(255))
    subject = Column(INTEGER(10))
    subject_name = Column(String(255))
    subtopic = Column(INTEGER(11))
    subtopic_name = Column(String(255))
    language = Column(String(255))
    difficulty = Column(INTEGER(10))
    instruction = Column(Text)
    text = Column(Text)
    model_answer1 = Column(Text)
    model_answer1_title = Column(Text)
    keyword_count1 = Column(INTEGER(11))
    model_answer2 = Column(Text)
    model_answer2_title = Column(Text)
    keyword_count2 = Column(INTEGER(11))
    explanation = Column(Text)
    created_at = Column(String(255))
    edited_at = Column(String(255))
    deleted_at = Column(String(255))

    def to_dict(self):
        column_name_list = [
            value[0] for value in self._sa_instance_state.attrs.items()
        ]
        return dict(
            (column_name, getattr(self, column_name, None)) \
            for column_name in column_name_list
        )


class shortquestion(Base):
    __tablename__ = "short_question"

    id = Column(INTEGER(11), primary_key=True)
    topic = Column(INTEGER(10))
    topic_name = Column(String(255))
    subject = Column(INTEGER(10))
    subject_name = Column(String(255))
    subtopic = Column(INTEGER(11))
    subtopic_name = Column(String(255))
    language = Column(String(255))
    difficulty = Column(INTEGER(10))
    instruction = Column(Text)
    text = Column(Text)
    model_answer = Column(Text)
    keyword_count = Column(INTEGER(11))
    explanation = Column(Text)
    created_at = Column(String(255))
    edited_at = Column(String(255))
    deleted_at = Column(String(255))

    def to_dict(self):
        column_name_list = [
            value[0] for value in self._sa_instance_state.attrs.items()
        ]
        return dict(
            (column_name, getattr(self, column_name, None)) \
            for column_name in column_name_list
        )