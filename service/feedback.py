"""
@Project: BackendForPain
@File: feedback.py
@Auth: Bosscal
@Date: 2023/9/15
@Description: 
"""
from model.feedback import Feedback
from model.user import User
from const import ErrorCode


class FeedbackService:

    @classmethod
    def add_msg(cls, receiver, sender, msg):
        """
        增加一条消息
        :param receiver: 收件人
        :param sender: 发件人
        :param msg: 信息
        :return:
        """
        # 查询发件人，收件人是否存在
        if User.query_user_by_id(receiver) is None or User.query_user_by_id(sender) is None:
            return ErrorCode.UserNotExists
        # 新建一条消息
        if not Feedback.add_msg(receiver, sender, msg):
            return ErrorCode.AddMsgError
        return ErrorCode.Success

    @classmethod
    def delete_msg(cls, msg_id):
        """
        删除一条信息
        :param msg_id: 信息的ID
        :return:
        """
        # 查询消息是否存在
        msg_data = Feedback.query_msg_by_id(msg_id)
        if not msg_data:
            return ErrorCode.MsgNotExists
        # 删除一条消息
        if not Feedback.delete_msg(msg_data):
            return ErrorCode.DeleteMsgError
        return ErrorCode.Success

    @classmethod
    def get_msg_by_user_id(cls, receiver, sender):
        """
        根据收件人ID和发件人ID查找具体的消息
        :param receiver: 收件人
        :param sender: 发件人
        :return:
        """
        # 查询发件人，收件人是否存在
        if User.query_user_by_id(receiver) is None or User.query_user_by_id(sender) is None:
            return ErrorCode.UserNotExists
        # 查询信息
        return Feedback.query_msg_by_receiver_and_sender(receiver, sender)
