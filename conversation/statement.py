# -*- coding: utf-8 -*-
from .response import Response

class Statement(object):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.
    """

    # 初始化流程
    def __init__(self, text, **kwargs):
        self.text = text # 语句
        self.in_response_to = kwargs.get("in_response_to", []) # 应答列表 注:当in_response_to不存在时, 返回空列表[].

        self.extra_data = {}

        if "in_response_to" in kwargs:
            del(kwargs["in_response_to"])

        self.extra_data.update(kwargs)

    def __str__(self):
        return self.text

    def __repr__(self):
        return "<Statement text:%s>" % (self.text)

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, Statement): # 判断类型是否一致
            return self.text == other.text

        return self.text == other

    # 添加扩展数据
    def add_extra_data(self, key, value):
        """
        This method allows additional data to be stored on the
        statement object.
        """
        self.extra_data[key] = value

    # 增加应答
    def add_response(self, response):
        """
        Add the response to the list if it does not already exist.
        """
        if not isinstance(response, Response):
            raise Statement.InvalidTypeException(
                'A {} was recieved when a {} instance was expected'.format(
                    type(response),
                    type(Response(''))
                )
            )

        updated = False
        for index in range(0, len(self.in_response_to)):
            if response.text == self.in_response_to[index].text: # 判断应答列表中是否已经存在
                self.in_response_to[index].occurrence += 1 # 统计发生次数
                updated = True

        if not updated:
            self.in_response_to.append(response) # 更新应答列表

    # 从应答链表中删除某应答
    def remove_response(self, response_text):
        """
        Removes a response from the statement's response list based
        on the value of the response text.
        """
        for response in self.in_response_to:
            if response_text == response.text:
                self.in_response_to.remove(response)
                return True
        return False

    # 获取某应答的出现次数
    def get_response_count(self, statement):
        """
        Return the number of times the statement occurs in the database.
        """
        for response in self.in_response_to:
            if statement.text == response.text:
                return response.occurrence

        return 0

    # 序列化 返回值:map类型
    def serialize(self):
        """
        Returns a dictionary representation of the current object.
        """
        data = {}

        data["text"] = self.text
        data["in_response_to"] = []
        data.update(self.extra_data)

        for response in self.in_response_to:
            data["in_response_to"].append(response.serialize())

        return data

    class InvalidTypeException(Exception):

        def __init__(self, value='Recieved an unexpected value type.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
