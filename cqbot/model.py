#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月22日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: cqbot.model
@description: 
"""
from cqbot.skylark import Model, PrimaryKey, Field


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class Commands(Model):
    cid = PrimaryKey()
    name = Field()              # 命令关键词
    value = Field()             # 回复内容

    @classmethod
    def add(cls, name, value):
        """添加或更新命令
        :param cls:
        :param name:           # 命令关键词
        :param value:          # 回复内容
        """
        try:
            entity = cls.findone(cls.name == name)
            if entity:
                # 已存在则更新
                entity.value = value
                return '' if entity.save() else '更新命令失败'
            return '' if cls.create(name=name, value=value) else '添加命令失败'
        except Exception as e:
            return '添加命令失败: {}'.format(e)


class Notices(Model):
    nid = PrimaryKey()
    gid = Field()               # 群号-int
    txt = Field()               # 进群提示消息


class Questions(Model):
    qid = PrimaryKey()
    question = Field()          # 问题关键词, like模糊匹配
    answer = Field()            # 答案
