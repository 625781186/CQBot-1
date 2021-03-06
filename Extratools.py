#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年2月15日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Extratools
@description: 额外工具类,色情图片鉴别,斗图
"""
import base64
import hashlib
import io
import json
import os
from random import choice
from time import time
from urllib.parse import quote, urlencode

from PIL import Image
from tornado.gen import coroutine, Task
from tornado.httpclient import AsyncHTTPClient


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

url_vision_porn = 'https://api.ai.qq.com/fcgi-bin/vision/vision_porn'

url_doutu = 'http://tugele.mse.sogou.com/query?flag_time={flag_time}&h=ffffffff-d25b-cfdd-ffff-ffff990f5542&v=android8.28.1&ip=&pv=android5.1.1&aid=00f1f3b60d691050&dpi=240&key={key}&sdk=1.10&imei=863254010002417&imsi=460070024124318&page={page}&brand=MI+6+'


@coroutine
def getDouTu(key):
    """斗图
    :param key:
    """
    client = AsyncHTTPClient()
    resp = yield Task(
        client.fetch,
        url_doutu.format(flag_time=time(), key=key, page=1),
        method='GET',
    )
    if not resp.body:
        print('no body')
        return ''
    try:
        infos = json.loads(resp.body.decode())
    except Exception as e:
        print(e)
        return ''

#     print(infos)

    datas = infos.get('data', [])
    if len(datas) == 0:
        return ''
    # 随机一个
    item = choice(datas)
#     print(item.get('yuntuUrl', ''))
    return item.get('yuntuUrl', '')


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
#         print('check url: ', path)

        # 先下载图片
        client = AsyncHTTPClient()
        resp = yield Task(
            client.fetch,
            path,
            method='GET'
        )
        if not resp.body:
            print('check image, can not download image')
            return 0
        body = io.BytesIO(resp.body)
        with Image.open(body) as img:
            if len(resp.body) > 1000000:
                # 先保存
                name = 'images/' + hashlib.md5(os.urandom(6)).hexdigest() + \
                    '.' + img.format.lower()
                img.save(name, img.format, quality=10)
                image = base64.b64encode(open(name, 'rb').read()).decode()
                try:
                    os.unlink(name)
                except:
                    pass
            else:
                # 小图片直接base64编码
                image = base64.b64encode(resp.body).decode()

        params = {
            'app_id': SexImageCheck.APPID,
            # 原始图片的base64编码数据（原图大小上限1MB，支持JPG、PNG、BMP格式），image和image_url必须至少提供一个
            'image': image,
            #             'image_url': path,  # 如果image和image_url都提供，仅支持image_url，image和image_url必须至少提供一个
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
#             print(infos)
            if infos.get('ret', -1) == 0:
                normal = 0
                hot = 0
                tag_list = infos.get('data', {}).get('tag_list', [])
                for item in tag_list:
                    #                     if item.get('tag_name', '') not in ('normal', 'hot', 'tag_confidence'):
                    #                         if item.get('tag_confidence', 0) > 80:
                    #                             print('sex image: ', path)
                    #                             return 1
                    if item.get('tag_name', '') == 'normal':
                        normal = item.get('tag_confidence', 0)
                    elif item.get('tag_name', '') == 'hot':
                        hot = item.get('tag_confidence', 0)
                if hot > normal and hot > 80:  # 增加一个阈值
                    print('sex image: ', path)
                    return 1
                else:
                    return 0
        except Exception as e:
            print('check image return error:', e)
            return 0
        return 0


if __name__ == '__main__':
    SexImageCheck.init()
