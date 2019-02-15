#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月22日
@author: Irony
@site: https://pyqt5.com, https://github.com/892768447
@email: 892768447@qq.com
@file: BotHandler
@description: 处理消息
"""
import json
import logging
import re
import time
from urllib.parse import quote, urlencode

from tornado.gen import coroutine, Task
from tornado.httpclient import AsyncHTTPClient

from BotConfig import NoticeGroup, IgnoreGroup, BaiduMatch, GoogleMatch,\
    RunMatch, QTDocMatch, GitHubMatch, StackMatch, FindMatch, ADMIN, AddQWMatch,\
    ImageSearch
from BotModel import Questions
from HelpMenu import WelcomeMsg, HelpMenu
from SexImageCheck import SexImageCheck


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


def msgFilter(message):
    # 对消息进行过滤
    msg = message.get('message', '')
    # 替换图片链接
#     msg = re.sub('\[CQ:.*?,url=(.*?)\]',
#                  lambda m: '<a target="_blank" href="' +
#                  m.group(1) + '">', msg)
    msg = re.sub('\[CQ:.*?,url=(.*?)\]',
                 lambda m: '[图片消息]', msg)
    # 替换酷Q码为空
    msg = re.sub('\[CQ:.*\]', '', msg, flags=re.S | re.M)
    if not msg:
        return
    message['message'] = msg
    message['time'] = time.strftime('%m-%d %H:%M', time.localtime(
        message.get('time', int(time.time()))))
    message['rint'] = str(time.time()).replace('.', '')[:13]
    return message


@coroutine
def do_run_code(user_id, message, code):
    """执行代码
    :param user_id:        用户QQ
    :param message:        消息json结构体
    :param code:           代码
    """
    code = code.strip()
    if not code:
        return
    body = urlencode(
        {'language': 15, 'fileext': 'py3', 'code': code, 'stdin': ''}, safe='()')
    client = AsyncHTTPClient()
    resp = yield Task(
        client.fetch,
        #             'http://www.runoob.com/api/compile.php',
        'https://m.runoob.com/api/compile.php',
        method='POST',
        body=body,
        headers={
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            #                 'Host': 'www.runoob.com',
            #                 'Origin': 'http://www.runoob.com',
            'Host': 'm.runoob.com',
            'Origin': 'https://c.runoob.com',
            'Referer': 'https://c.runoob.com/compile/9',
            'Referer': 'http://www.runoob.com/try/runcode.php?filename=basic_data_type1&type=python3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6756.400 QQBrowser/10.3.2473.400',
            #                 'X-Requested-With': 'XMLHttpRequest'
        }
    )
    if not resp.body:
        result = '没有结果'
    else:
        try:
            result = json.loads(resp.body.decode())
            result = result.get('output', '') + result.get('errors', '')
        except Exception as e:
            result = '运行错误: ' + str(e)
    message['message'] = '[CQ:at,qq={}]\n{}'.format(user_id, result)
    return message


@coroutine
def replyMessage(group_id, message):
    """对消息进行处理和回复,如果不回复内容则返回None
    :param group_id:            # 群号
    :param message:             # 原始消息json
    :return: message
    """
    user_id = message.get('user_id', None)  # 发送人QQ
    message_type = message.get('message_type', None)  # 消息类型
    msg = message.get('message', '')  # 消息内容
    logging.debug('处理消息: {}'.format(msg))

    # 进群消息
    if message.get('notice_type', '') == 'group_increase' and group_id in NoticeGroup:
        logging.debug('{}加入群{}'.format(user_id, group_id))
        message['message'] = WelcomeMsg.format(user_id) + HelpMenu['菜单']
        return message
    # 群聊消息
    elif message_type == 'group':
        comMsg = HelpMenu.get(msg, '')
        # 匹配到菜单,忽略忽视群
        if comMsg and group_id not in IgnoreGroup:
            message['message'] = comMsg.format(user_id)
            return message
        # 匹配到百度搜索
        elif BaiduMatch.search(msg):
            wd = msg[3:]
            logging.debug('百度搜索: {}'.format(wd))
            message['message'] = '[CQ:at,qq={}]\nhttps://pyqt5.com/search.php?m=baidu&w={}' \
                .format(user_id, quote(wd))
            return message
        # 匹配到谷歌搜索
        elif GoogleMatch.search(msg):
            wd = msg[3:]
            logging.debug('谷歌搜索: {}'.format(wd))
            if str(group_id) == '592588163':
                message['message'] = '[CQ:at,qq={}]\nhttps://pyqt5.com/search.php?m=google&w={}' \
                    .format(user_id, quote(wd))
            else:
                message['message'] = '[CQ:at,qq={}]\nhttps://pyqt5.com/search.php?m=google&w={}' \
                    .format(user_id, quote(wd))
            return message
#         # 匹配到翻译
#         elif TransMatch.search(msg):
#             text = msg[3:]
#             yield Translate.getSeed()
#             result = yield Translate.translate(text)
#             message['message'] = '[CQ:at,qq={}]\n{}'.format(
#                 user_id, result)
#             return message
        # 执行代码
        elif RunMatch.search(msg):
            code = msg[3:]
            logging.debug('执行代码: {}'.format(code))
            return do_run_code(user_id, message, code)
        # 匹配QT官方文档
        elif QTDocMatch.search(msg):
            wd = msg[3:].lower()  # 后面有关键词
            logging.debug('QT官方文档: {}'.format(wd))
            message['message'] = '[CQ:at,qq={}]\n1.QT版本: http://doc.qt.io/qt-5/{}.html;\n2.pyside2版本: https://doc-snapshots.qt.io/qtforpython/search.html?q={}' \
                .format(user_id, wd, wd)
            return message
        # 匹配 GitHub
        elif GitHubMatch.search(msg):
            wd = msg[3:]  # 后面有关键词
            message['message'] = '[CQ:at,qq={}]\nhttps://github.com/search?o=desc&q={}&s=stars&type=Repositories' \
                .format(user_id, '+'.join(wd.split(' ')))
            return message
        # 匹配StackOverflow
        elif StackMatch.search(msg):
            wd = msg[3:].lower()  # 后面有关键词
            logging.debug('StackOverflow: {}'.format(wd))
            message['message'] = '[CQ:at,qq={}]\nhttps://stackoverflow.com/search?q={}' \
                .format(user_id, '+'.join(wd.split(' ')))
            return message
        # 检索问题(查找数据库)
        elif FindMatch.search(msg):
            question = msg[3:]  # 后面有关键词
            logging.debug('检索问题: {}'.format(question))
            rets = Questions.query(question)
            if not rets:
                return
            message['message'] = '[CQ:at,qq={}]\n{}' \
                .format(user_id, '\n'.join(['{}. {}'.format(
                    i + 1, ret.answer) for i, ret in enumerate(rets)]))
            return message
        # 添加问题
        elif AddQWMatch.search(msg) and str(user_id) in ADMIN:
            logging.debug('添加问题: {}'.format(msg))
            try:
                question, answer = AddQWMatch.findall(msg)[0]
                message['message'] = Questions.add(question, answer)
                return message
            except Exception as e:
                logging.warn(str(e))
        # 图片
        elif ImageSearch.search(msg):
            urls = ImageSearch.findall(msg)
            print('find urls: ', urls)
#             for url in urls:
#                 url = url.replace('&amp;', '&')
#                 ret = yield SexImageCheck.check(url)
            if urls:
                url = urls[0].replace('&amp;', '&')
                ret = yield SexImageCheck.check(url)
                if ret == 1:
                    message['message'] = ' ⃢ܫ⃢ : 发现一张色情图!!!'
                    return message
