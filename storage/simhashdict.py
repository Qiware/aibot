# -*- coding: utf-8 -*-

import os
import pickle
from conversation.statement import Statement

#SimHash只是句子的索引, 并不存储句子对应的应答.
#通过SimHash锁定句子后, 再到ConversionDict中获取应答语句.
class SimHashDict(object):
    def __init__(self):
        # Load simhash dict
        self.incr = 0;
        self.simhash = {};
        try:
            f = open("simhash.dict", 'rb');
            self.simhash = pickle.load(f);
            f.close();
        except IOError:
            print("Open simhash.dict failed")

    def dump(self):
        try:
            f = open("simhash.dict", 'wb');
            pickle.dump(self.simhash, f);
            f.close();
        except IOError:
            print("Open simhash.dict failed")

    def add(self, text):
        key = simhash(text)
        statement_list = self.simhash.get(key, []);

        is_find = False
        for statement in statement_list:
            if text == statement.text:
                is_find = True;
                break;

        if False == is_find:
            statement = Statement(text);
            statement_list.append(statement);

        self.incr += 1;
        self.simhash[key] = statement_list;
        #print("hash:%s" % key)

    def find(self, text):
        key = simhash(text)
        return self.simhash.get(key); # Statement[]列表

    def remove(self, text):
        key = simhash(text)
        del(self.simhash, key)
