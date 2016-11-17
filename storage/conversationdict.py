# -*- coding: utf-8 -*-

import os
import pickle
from conversation.response import Response
from conversation.statement import Statement

class ConversationDict(object):
    def __init__(self):
        # Load conversation dict
        self.incr = 0;
        self.conversation = {};
        try:
            f = open("conversation.dict", 'rb');
            self.conversation = pickle.load(f);
            f.close();
        except IOError:
            print("Open conversation.dict failed")

    def dump(self):
        try:
            f = open("conversation.dict", 'wb');
            pickle.dump(self.conversation, f);
            f.close();
        except IOError:
            print("Open conversation.dict failed")

    def add(self, hash_val, req_text, rsp_text):
        statement = self.conversation.get(hash_val);
        if statement is None:
            self.incr += 1
            statement = Statement(req_text)

        response = Response(rsp_text)
        statement.add_response(response);
        self.conversation[hash_val] = statement

    def find(self, hash_val):
        return self.conversation.get(hash_val);

    def printx(self):
        idx = 0;
        for k, v in self.conversation.items():
            idx += 1
            print("idx:%d k:%s v:%s" % (idx, k, v))

    def remove(self, hash_val):
        del(self.conversation, hash_val)
