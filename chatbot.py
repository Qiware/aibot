# -*- coding: utf-8 -*-

from corpus import Corpus
from storage import Storage
from conversation import Response
from conversation import Statement

class ChatBot(object):

    def __init__(self, name):
        self.name = name
        self.storage = Storage()

    def get_response(self, text):
        return self.storage.find(text)

    def train(self, dot_path):
        print("Begin train...")
        corpus = Corpus()
        corpus_data = corpus.load_corpus(dot_path)
        for data in corpus_data:
            for conversation in data: # conversation表示一个会话
                statement_history = []
                for text in conversation: # 依次从训练对话中取句子
                    if statement_history:
                        self.storage.add(statement_history[-1], text.encode('utf-8'));
                    statement_history.append(text.encode('utf-8')) # 当前语句加入历史列表
        print("End of train!")

    def dump(self):
        print("Begin dump...")
        self.storage.dump()
        print("End of dump!")

    def printx(self):
        self.storage.printx()
