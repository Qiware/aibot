# -*- coding: utf-8 -*-
import os
import jieba
import chatbot

if __name__ == "__main__":
    jieba.load_userdict("./dict/dict.txt.big");
    # 新建机器人
    bot = chatbot.ChatBot("qifeng")

    idx = 0
    while (True):
        idx += 1
        text = "你好"
        print("idx:%d Q:%s" % (idx, text));
        print("idx:%d A:%s" % (idx, bot.get_response(text)))

        text = "~国安是冠军~"
        print("idx:%d Q:%s" % (idx, text));
        print("idx:%d A:%s" % (idx, bot.get_response(text)))

        idx += 1

    #bot.printx()
