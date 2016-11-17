# -*- coding: utf-8 -*-

import os
import pickle

from conversation.statement import Statement

class ReverseItem(object):
    def __init__(self, weight, text):
        self.weight = weight;
        self.statement = Statement(text);

class ReverseDict(object):
    def __init__(self):
        # Load reverse dict
        self.incr = 0;
        self.reverse = {};
        try:
            f = open("reverse.dict", 'rb');
            self.reverse = pickle.load(f);
            f.close();
        except IOError:
            print("Open reverse.dict failed!")

    def dump(self):
        try:
            f = open("reverse.dict", 'wb');
            pickle.dump(self.reverse, f);
            f.close();
        except IOError:
            print("Open reverse.dict failed!")

    def add(self, key, weight, text):
        items = self.reverse.get(key, []);

        idx = 0
        for item in items:
            if item.weight > weight:
                idx += 1
                continue
            elif item.weight < weight:
                item = ReverseItem(weight, text);
                items.insert(idx, item);
                self.incr += 1;
                self.reverse[key] = items;
                return
            elif text == item.statement.text:
                return

        item = ReverseItem(weight, text);
        items.insert(idx, item);
        self.incr += 1;
        self.reverse[key] = items;
        #print("key:%s weight:%s text:%s" % (key, weight, text))
        return

    def find(self, key):
        return self.reverse.get(key, []); # Statement[]列表

    def remove(self, key):
        del(self.reverse, key)
