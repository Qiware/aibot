# -*- coding: utf-8 -*-

import re
import jieba
import random
import jieba.posseg
import jieba.analyse
from fuzzywuzzy import fuzz

from .simhashdict import SimHashDict
from .reversedict import ReverseDict
from .conversationdict import ConversationDict

class Storage(object):
    def __init__(self):
        self.rate = 0.5
        self.word_max_len = 2
        self.simhash_dict = SimHashDict()
        self.reverse_dict = ReverseDict()
        self.conversation_dict = ConversationDict()

    def dump(self):
        self.simhash_dict.dump()
        self.reverse_dict.dump()
        self.conversation_dict.dump()

    def printx(self):
        self.conversation_dict.printx()

    def gen_key_list(self, word_list, weight_list, num, key_max_len):
        """
        功能描述: 生成关键字列表.
        注意事项: 列表中关键字越来越短, 因此越靠前匹配出来的结果可靠性越高.
        """
        #key_dict = {}
        key_list = []
        for i in xrange(key_max_len):
            kl = key_max_len - i
            for idx in xrange(num-kl+1):
                #print("kl:%d idx:%d" % (kl, idx))
                key = ""
                weight = 0;
                x = 0
                for n in xrange(kl):
                    if 0 == x:
                        key += word_list[idx+n]
                        x = 1
                    else:
                        key += "-" + word_list[idx+n]
                    weight += weight_list[idx+n]
                #key_dict.setdefault(key, weight)
                #print("key:%s" % key)
                key_list.append(key)
        #return key_dict
        return key_list

    def insert_into_conversation_dict(self, hash_val, text, resp):
        """
        功能描述: 插入对话词典
        参数列表:
            @hash: 文本text的哈希值
            @text: 文本text
            @resp: 文本text对应的应答
        注意事项: 对话词典以文本text的哈希值为主键.
        """
        if resp:
            self.conversation_dict.add(hash_val, text, resp);

    def insert_into_reverse_dict(self, hash_val, text):
        """
        功能描述: 插入倒排词典
        参数列表:
            @hash: 文本text的哈希值
            @text: 文本text
        注意事项: 当词的所占权重低于平均权重的20%时, 不对其构建索引, 也不对其进行搜索.
        """
        word_num = 0;
        weight_avg = 0;
        weight_total = 0;

        word_list = []
        weight_list = []

        # 切词处理
        word_with_weight = jieba.analyse.extract_tags(text, withWeight=True)
        for word, weight in word_with_weight:
            word_num += 1;
            weight_total += float(weight);
        if word_num > 0:
            weight_avg = weight_total / word_num;
        for word, weight in word_with_weight:
            if weight < (self.rate * weight_avg):
                break
            word_list.append(word);
            weight_list.append(weight);

        # 生成关键字列表
        list_len = len(word_list)
        key_list = self.gen_key_list(word_list, weight_list, list_len, self.word_max_len)
        for key in key_list:
            self.reverse_dict.add(key, 100, hash_val); # 生成倒排(key -> hash)

    def add(self, text, resp):
        hash_val = hash(text);

        print("hash:%s" % hash_val);

        # 加入会话字典
        self.insert_into_conversation_dict(hash_val, text, resp);

        # 加入SIMHASH字典
        #self.simhash_dict.add(text);

        # 加入倒排字典
        self.insert_into_reverse_dict(hash_val, text)

    # 从对话词典中匹配
    def find_from_conversation_dict(self, hash_val):
        statement = self.conversation_dict.find(hash_val)
        if statement:
            num = len(statement.in_response_to);
            if num > 0:
                print("num:%s hash:%s" % (num, hash_val))
                return statement.in_response_to[random.randint(0, num-1)].text
        print("Not found from conversation dictionary! hash:%s" % (hash_val))
        return None

    # 从倒排词典中匹配
    def find_from_reverse_dict(self, hash_val, text):
        """
        功能描述: 当词的所占权重低于平均权重的20%时, 不对其构建索引, 也不对其进行搜索.
        参数列表:
            @hash_val: 文本text的SIM哈希值
            @text: 聊天文本
        """
        word_num = 0;
        weight_avg = 0;
        weight_total = 0;

        # 查找所有关联语句
        word_list = []
        weight_list = []

        # 切词处理
        word_with_weight = jieba.analyse.extract_tags(text, withWeight=True)
        for word, weight in word_with_weight:
            word_num += 1;
            weight_total += float(weight);
        if word_num > 0:
            weight_avg = weight_total / word_num;
        for word, weight in word_with_weight:
            if weight < (self.rate * weight_avg):
                break
            word_list.append(word);
            weight_list.append(weight);

        # 生成关键字列表
        list_len = len(word_list)
        key_list = self.gen_key_list(word_list, weight_list, list_len, self.word_max_len)
        if 0 == len(key_list):
            return None

        # 查找匹配交集
        idx = 0
        intersection = {} #哈系值集合
        for key in key_list:
            temp_dict = {} # key对应的句子哈希值集合
            print("key:%s" % key)
            statements = self.reverse_dict.find(key)
            if 0 == len(statements):
                continue
            for item in statements:
                # 注意:此时的item.statement.text对应的哈希值
                temp_dict.setdefault(item.statement.text, 1)

            idx += 1

            # 获取关联语句交集
            if 0 == len(intersection):
                intersection = temp_dict;
            else:
                keys = list(set(intersection.keys()) & set(temp_dict.keys()))
                if 0 == len(keys):
                    continue
                intersection = {}
                for key in keys:
                    intersection.setdefault(key, None)
            if idx >= word_num:
                break # 匹配超过word_num次则退出后续比较(TODO: 待验证合理性)

        # 筛选匹配度最高的语句
        ratio = 0
        confidence = -1
        closest_text = None
        for hash_item in intersection:
            print("hash:%s" % (hash_item))
            statement = self.conversation_dict.find(hash_item);
            if statement:
                ratio = fuzz.ratio(text, statement.text)
                print("ratio:%s item:%s hash:%s" % (ratio, statement.text, hash_item))
                if ratio > confidence and ratio >= 60:
                    confidence = ratio
                    closest_text = hash_item

        #print("confidence:%s match:%s" % (confidence, closest_text))
        # 获取匹配度最高的应答
        if closest_text:
            return self.find_from_conversation_dict(closest_text);

        return None 

    def find(self, text):
        hash_val = hash(text);

        # 从会话字典匹配
        resp_text = self.find_from_conversation_dict(hash_val);
        if resp_text:
            return resp_text

        # 从倒排字典匹配
        resp_text = self.find_from_reverse_dict(hash_val, text)
        if resp_text:
            return resp_text

        return "~你让我~无言以对~~"
