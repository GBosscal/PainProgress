"""
@Project: BackendForPain
@File: feedback.py
@Auth: Bosscal
@Date: 2023/9/15
@Description: 
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR, Text, or_, and_

from model.base import BaseModel
from utils.orm_mysql import create_db_session
from const import DeleteOrNot

session = create_db_session()


class Feedback(BaseModel):
    __tablename__ = "feedback"

    receiver = Column(VARCHAR(36), nullable=False)  # 收件人
    sender = Column(VARCHAR(36), nullable=False)  # 发件人
    msg = Column(Text, nullable=False)

    def __init__(self, receiver, sender, msg):
        self.receiver = receiver
        self.sender = sender
        self.msg = msg

    def to_dict(self):
        return {
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S"), "receiver": self.receiver,
            "sender": self.sender, "msg": self.msg, "created_timestamp": self.created_time.timestamp()
        }

    @classmethod
    def add_msg(cls, receiver, sender, msg):
        new_msg = cls(receiver=receiver, sender=sender, msg=msg)
        try:
            session.add(new_msg)
            session.commit()
            return True
        except Exception:
            print(traceback.format_exc())
            session.rollback()
            return False

    @classmethod
    def query_msg_by_id(cls, msg_id):
        return session.query(cls).filter_by(id=msg_id, is_deleted=DeleteOrNot.NotDeleted.value).first()

    @classmethod
    def delete_msg(cls, msg_data):
        msg_data.id_deleted = DeleteOrNot.Deleted.value
        try:
            session.merge(msg_data)
            session.commit()
            return True
        except Exception:
            print(traceback.format_exc())
            session.rollback()
            return False

    @classmethod
    def query_msg_by_receiver_and_sender(cls, receiver, sender):
        # 这里查找的时候，收件人/发件人是其中一方的时候，发件人/收件人是另一方即可
        data = session.query(cls).filter(
            or_(
                and_(cls.receiver == receiver, cls.sender == sender),
                and_(cls.sender == receiver, cls.receiver == sender)
            )
        ).order_by(cls.created_time).all()
        return data
