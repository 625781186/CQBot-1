#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月22日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: cqbot
@description: 
"""
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class BotApiSocketHandler(WebSocketHandler):
    pass


class BotEventSocketHandler(WebSocketHandler):
    pass


class IndexHandler(RequestHandler):
    pass


class CQBotApplication(Application):

    # 缓存单个消息,最多30条
    MSGS = []

    def __init__(self, *args, **kwargs):
        handlers = [
            (r'/ws/api/', BotApiSocketHandler),
            (r'/ws/event/', BotEventSocketHandler),
            (r'/.*', IndexHandler),
        ]
        super(CQBotApplication, self).__init__(handlers)


def run(port=9898):
    server = HTTPServer(CQBotApplication())
    server.listen(port)
    IOLoop.current().start()
