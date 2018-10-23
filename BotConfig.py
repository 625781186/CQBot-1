#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月22日
@author: Irony
@site: https://pyqt5.com, https://github.com/892768447
@email: 892768447@qq.com
@file: BotConfig
@description: 
"""
import re


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0

# 管理员QQ
ADMIN = {
    '892768447': '群主',
    '625781186': '人间白头'
}

# 提供一个api获取该群的30条最新消息
WEBGROUP = {
    '246269919': 'PyQt 学习',
    #     '277624735': '我的测试群',
}

# 自动分享博客链接到群
SHAREGROUP = {
#     '277624735': '我的测试群',
    '246269919': 'PyQt 学习',
    '432987409': 'PyQt5小组',
    '592588163': 'PyQt5 开发高级群',
    #     '432993537': 'pyqt_qml',
    '435685112': 'Python学习交流分享'
}

# 需要监听的群号
GROUPIDS = {
    '277624735': '我的测试群',
    '246269919': 'PyQt 学习',
    '432987409': 'PyQt5小组',
    '592588163': 'PyQt5 开发高级群',
    '432993537': 'pyqt_qml',
    '435685112': 'Python学习交流分享',
    '134840268': '开发交流'
}

# 进群提示公告消息
NoticeGroup = {
    '246269919': 'PyQt 学习',
    '432987409': 'PyQt5小组',
    '432993537': 'pyqt_qml',
    '134840268': '开发交流'
}

# 忽略群
IgnoreGroup = {
    # '435685112': 'Python学习交流分享'
}


BaiduMatch = re.compile('^百度 (.*)', re.M | re.S)
GoogleMatch = re.compile('^谷歌 (.*)', re.M | re.S)
RunMatch = re.compile('^运行 (.*)', re.M | re.S)
FindMatch = re.compile('^检索 (.*)', re.M | re.S)
AddQWMatch = re.compile('^问题:(.*?)答案:(.*)', re.M | re.S)
BaiduResult = re.compile(
    'data-tools=\'{"title":"(.*?)","url":"(.*?)"}\'><a class="c-tip-icon">')

QTDocMatch = re.compile('^-f (.*)', re.M | re.S)
GitHubMatch = re.compile('^-g (.*)', re.M | re.S)
StackMatch = re.compile('^-s (.*)', re.M | re.S)
