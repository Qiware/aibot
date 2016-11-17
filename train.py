# -*- coding: utf-8 -*-
import os
import jieba
import chatbot

def load_userdict():
    # 姓名列表
    jieba.load_userdict("./dict/name/amuse.txt");
    jieba.load_userdict("./dict/name/sporter.txt");
    jieba.load_userdict("./dict/name/politicians.txt");

    # 体育项目
    jieba.load_userdict("./dict/sport.txt"); # 体育项目

    # 默认词典
    jieba.load_userdict("./dict/dict.txt");

if __name__ == "__main__":
    # 加载字典
    load_userdict()

    # 新建机器人
    bot = chatbot.ChatBot("qifeng")

    # 训练机器人
    bot.train("chatterbot.corpus.chinese")

    # 打印训练结果
    #print("Print train result!")
    #bot.printx()

    # 固化训练结果
    bot.dump()
