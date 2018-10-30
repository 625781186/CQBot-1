#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月22日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: botserver
@description:
"""
import json
import logging
import sqlite3
from time import time

from skylark import Database
from tornado.gen import coroutine
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler

import BotConfig
import BotHandler


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class BotApiSocketHandler(WebSocketHandler):
    """api接口,主要用于发送消息"""

    WS = None

    def open(self, *args, **kwargs):
        if not BotApiSocketHandler.WS and self.request.headers.get('X-Self-Id', None):
            BotApiSocketHandler.WS = self
        logging.info(str(self.request.headers))

    def on_close(self):
        BotApiSocketHandler.WS = None
        logging.info('api ws 断开连接')

    def on_message(self, message):
        logging.info('发送结果: ' + str(message))

    @classmethod
    def send_msg(cls, message):
        if BotApiSocketHandler.WS:
            BotApiSocketHandler.WS.write_message({
                "action": "send_group_msg",
                "params": message,
                "echo": time()
            })
        else:
            logging.info('api ws 未连接')


class BotEventSocketHandler(WebSocketHandler):
    """消息事件,主要用于接收消息和分发消息到前端"""

    MESSAGEID = 0

    @coroutine
    def on_message(self, message):
        logging.info(str(message))
        try:
            # str -> json
            message = json.loads(message)
        except:
            return
        if not isinstance(message, dict):
            return
        # 获取群号
        group_id = str(message.get('group_id', ''))
        # 消息id（自增）
        BotEventSocketHandler.MESSAGEID = message.get('message_id', 0)
        # 不是群消息或者不是目标群
        if not group_id or group_id not in BotConfig.GROUPIDS:
            return
        # 先添加到web接口的那个群记录中
        if group_id in BotConfig.WEBGROUP:
            IndexHandler.append(message.copy())
        # 再回复目标群
        try:
            message = yield BotHandler.replyMessage(group_id, message.copy())
            if not message:
                return
#             message['message_id'] = BotEventSocketHandler.MESSAGEID + 1
            BotApiSocketHandler.send_msg(message)
        except Exception as e:
            logging.warn(str(e))


class ShareHandler(RequestHandler):

    def post(self, *args, **kwargs):
        try:
            body = json.loads(self.request.body.decode())
            title = body.get('title', '')
            url = body.get('url', '')
            if not url:
                self.finish({'error': 1, 'msg': '链接为空'})
                return
            # 发送给机器人
            for group_id in BotConfig.SHAREGROUP:
                try:
                    BotApiSocketHandler.send_msg({
                        'group_id': int(group_id),
                        'message': '[新文章] {}\n{}'.format(title, url),
                        'auto_escape': False
                    })
                except Exception as e:
                    logging.warn(str(e))
            self.finish({'msg': '分享成功'})
        except Exception as e:
            self.finish({'error': 1, 'msg': str(e)})


class IndexHandler(RequestHandler):

    MSGS = []  # 缓存单个消息
    MSGSLEN = 30  # 最多30条

    def get(self, *args, **kwargs):
        self.finish({'msgs': IndexHandler.MSGS})

    @classmethod
    def append(cls, message):
        if len(cls.MSGS) > cls.MSGSLEN:  # 超过30个
            cls.MSGS.pop(0)  # 删除第一个
        message = BotHandler.msgFilter(message)
        if not message:
            return
        cls.MSGS.append(message)


class CQBotApplication(Application):

    def __init__(self, *args, **kwargs):
        handlers = [
            (r'/ws/api/', BotApiSocketHandler),
            (r'/ws/event/', BotEventSocketHandler),
            (r'/share/', ShareHandler),
            (r'/.*', IndexHandler),
        ]
        super(CQBotApplication, self).__init__(handlers)


def initDb(db=None):
    """初始化数据库连接"""
    logging.debug('use db {}'.format(db))
    Database.set_dbapi(sqlite3)
    Database.set_autocommit(True)
    if db:
        Database.config(db=db, check_same_thread=False)


def initLog():
    logging.basicConfig(
        level=logging.WARNING,
        format="[%(asctime)s %(name)s %(module)s:%(funcName)s:%(lineno)s] %(levelname)-8s %(message)s")


def main(port=9898):
    initLog()
    initDb('data.db')
    server = HTTPServer(CQBotApplication())
    server.listen(port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
