#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年2月15日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: SexImageCheck
@description: 色情图片鉴别
"""
import hashlib
import json
import os
from time import time
from urllib.parse import quote, urlencode

from tornado.gen import coroutine, Task
from tornado.httpclient import AsyncHTTPClient


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

url_vision_porn = 'https://api.ai.qq.com/fcgi-bin/vision/vision_porn'


class SexImageCheck:

    APPID = ''
    APPKEY = ''

    @classmethod
    def init(cls):
        try:
            conf = json.loads(open('ai.json', 'rb').read().decode())
            SexImageCheck.APPID = conf.get('APPID', '')
            SexImageCheck.APPKEY = conf.get('APPKEY', '')
            print(
                'APPID: ', SexImageCheck.APPID[:3] + '*****' + SexImageCheck.APPID[-3:])
            print(
                'APPKEY: ', SexImageCheck.APPKEY[:3] + '*****' + SexImageCheck.APPKEY[-3:])
        except Exception as e:
            print(e)

    @classmethod
    def getReqSign(cls, params, appkey):
        """计算签名
        :param cls:
        :param params:
        :param appkey:
        """
        keys = list(params.keys())
        keys.sort()
        data = ''
        for key in keys:
            value = params[key]
            if value:
                data += key + '=' + quote(value, safe='') + '&'
        data += 'app_key=' + appkey
        return hashlib.md5(data.encode()).hexdigest().upper()

    @classmethod
    @coroutine
    def check(cls, path):
        """对图片进行检查
        :param cls:
        :param path:
        """
        if not SexImageCheck.APPID or not SexImageCheck.APPKEY:
            print('appid or appkey is null')
            return 0
        print('check url: ', path)
        params = {
            'app_id': SexImageCheck.APPID,
            # 原始图片的base64编码数据（原图大小上限1MB，支持JPG、PNG、BMP格式），image和image_url必须至少提供一个
            #     'image': base64.b64encode(open('324118.jpg', 'rb').read()).decode(),
            'image_url': path,  # 如果image和image_url都提供，仅支持image_url，image和image_url必须至少提供一个
            'nonce_str': hashlib.md5(os.urandom(32)).hexdigest(),  # 32长度随机字符串
            'sign': '',  # 32长度签名信息
            'time_stamp': str(time()).replace('.', '')[:10],  # 请求时间戳（秒级）
        }
        params['sign'] = cls.getReqSign(params, SexImageCheck.APPKEY)

        client = AsyncHTTPClient()
        resp = yield Task(
            client.fetch,
            url_vision_porn,
            method='POST',
            body=urlencode(params),
        )
        if not resp.body:
            print('check image return no body')
            return 0
        try:
            infos = json.loads(resp.body.decode())
        except Exception as e:
            print('check image return error:', e)
            return 0
#         print(infos)
        if infos.get('ret', -1) == 0:
            normal = 0
            hot = 0
            tag_list = infos.get('data', {}).get('tag_list', [])
            for item in tag_list:
                if item.get('tag_name', '') == 'normal':
                    normal = item.get('tag_confidence', 0)
                elif item.get('tag_name', '') == 'hot':
                    hot = item.get('tag_confidence', 0)
            if hot > normal:
                print('sex image: ', path)
                return 1
        return 0


if __name__ == '__main__':
    SexImageCheck.init()
