# -*- coding: utf-8 -*-
import os
import cgi
import sys
import json
import jieba
import chatbot
import logging
import SocketServer
import SimpleHTTPServer

# 新建机器人
idx = 0
bot = chatbot.ChatBot("qifeng")

def load_userdict():
    """
    Load user dictionary
    """
    # 姓名列表
    jieba.load_userdict("./dict/name/amuse.txt");
    jieba.load_userdict("./dict/name/sporter.txt");
    jieba.load_userdict("./dict/name/politicians.txt");

    # 体育项目
    jieba.load_userdict("./dict/sport.txt"); # 体育项目

    # 默认词典
    jieba.load_userdict("./dict/dict.txt");

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def chat_handler(self, post_dict):
        """
        请求报体: {"uid":123456, roomid=1000000015, "gid":5, "text":"你好"}
        应答报体: {"uid":123456, roomid=1000000015, "gid":5, "text":"你好, 有事吗?"}
        """
        global bot, idx;

        # 判断报体合法性
        if not post_dict.has_key("uid"):
            logging.warning("Miss param 'uid' in request body!")
            self.send_error(415, "Miss param 'uid' in request body!")
            return
        elif not post_dict.has_key("roomid"):
            logging.warning("Miss param 'roomid' in request body!")
            self.send_error(415, "Miss param 'roomid' in request body!")
            return
        elif not post_dict.has_key("gid"):
            logging.warning("Miss param 'gid' in request body!")
            self.send_error(415, "Miss param 'gid' in request body!")
            return
        elif not post_dict.has_key("text"):
            logging.warning("Miss param 'text' in request body!")
            self.send_error(415, "Miss param 'text' in request body!")
            return

        # 获取应答结果
        resp_text = bot.get_response(post_dict.get("text").encode('utf-8'));

        idx += 1;
        print("idx:%d Q:%s" % (idx, post_dict.get("text")));
        print("idx:%d A:%s" % (idx, resp_text));

        # 发送应答结果
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        resp_dict = {}
        resp_dict.setdefault("idx", idx)
        resp_dict.setdefault("uid", post_dict.get("uid"))
        resp_dict.setdefault("roomid", post_dict.get("roomid"))
        resp_dict.setdefault("gid", post_dict.get("gid"))
        resp_dict.setdefault("text", resp_text.decode('utf-8'))

        self.wfile.write(json.dumps(resp_dict))
        return

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)

        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)

        # 获取参数
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'application/json':
            length = int(self.headers['content-length'])
            post_dict = json.loads(self.rfile.read(length))
            self.TODOS.append(post_dict)
        else:
            #self.send_error(415, "Only json data is supported.")
            #return
            length = int(self.headers['content-length'])
            post_dict = json.loads(self.rfile.read(length))

        self.chat_handler(post_dict)

if __name__ == "__main__":
    # 解析命令行
    PORT = 80
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])

    # 加载自定义字典
    load_userdict();

    # 启动HTTP服务
    httpd = SocketServer.TCPServer(("", PORT), ServerHandler)

    print("Started httpserver on port:%s" % PORT);

    httpd.serve_forever()
