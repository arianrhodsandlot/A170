# coding: utf-8
import json
import os
import random
import re
import socket
import time
import urllib
from imgpy import Img
from requests_html import HTMLSession
from slugify import slugify
from tempfile import gettempdir

session = HTMLSession()
if os.path.exists('tmp'):
    tempdir = 'tmp'
else:
    tempdir = gettempdir()

socket.setdefaulttimeout(3)

def get_sticker_urls_from_fabiaoqing(sticker_name, limit=10):
    if not limit:
        return []
    url = 'https://www.fabiaoqing.com/search/search/keyword/{}'.format(urllib.parse.quote(sticker_name))
    print('开始请求{}'.format(url))
    try:
        r = session.get(url, timeout=2)
    except Exception as e:
        print(e)
        return []
    sticker_els = r.html.find('.searchbqppdiv .image')[:limit]
    if not sticker_els:
        return []
    sticker_urls = [sticker_el.attrs.get('data-original') for sticker_el in sticker_els]
    for idx, sticker_url in enumerate(sticker_urls):
        if sticker_url.startswith('/'):
            sticker_urls[idx] = 'https://www.fabiaoqing.com' + sticker_url
    return sticker_urls


def get_sticker_urls_from_doutula(sticker_name, limit=10):
    if not limit:
        return []
    url = 'https://www.doutula.com/search?keyword={}'.format(urllib.parse.quote(sticker_name))
    print('开始请求{}'.format(url))
    try:
        r = session.get(url, timeout=2)
    except Exception as e:
        print(e)
        return []
    sticker_els = r.html.find('.random_picture .img-responsive')[:limit]
    if not sticker_els:
        return []
    sticker_urls = [sticker_el.attrs.get('data-original') for sticker_el in sticker_els]
    for idx, sticker_url in enumerate(sticker_urls):
        if sticker_url.startswith('/'):
            sticker_urls[idx] = 'https://www.doutula.com/' + sticker_url
    return sticker_urls


def get_sticker_urls_from_google(sticker_name, limit=10):
    if not limit:
        return []
    q = '{} 表情包'.format(urllib.parse.quote(sticker_name))
    url = 'https://www.google.com/search?tbs=itp%3Aanimated&tbm=isch&q={}'.format(q)
    print('开始请求{}'.format(url))
    try:
        r = session.get(url, timeout=2)
    except Exception as e:
        print(e)
        return []
    sticker_els = r.html.find('.rg_el .rg_meta')[:limit]
    if not sticker_els:
        return []
    sticker_urls = [json.loads(sticker_el.text).get('ou') for sticker_el in sticker_els]
    sticker_urls = [sticker_url if sticker_url.endswith('.gif') else '{}#.gif'.format(sticker_url) for sticker_url in sticker_urls]
    return sticker_urls


def get_sticker_urls_from_sogou(sticker_name, limit=10):
    if not limit:
        return []
    url = 'http://biaoqing.sogou.com/anonymous/call/tugele/getSearchForOfficial?keyword={}'.format(urllib.parse.quote(sticker_name))
    print('开始请求{}'.format(url))
    try:
        r = session.get(url, timeout=2)
    except Exception as e:
        print(e)
        return []
    sticker_els = r.json().get('data')[:20]
    if not sticker_els:
        return []
    sticker_urls = [sticker_el.get('url') for sticker_el in sticker_els]
    gif_sticker_urls = [sticker_url for sticker_url in sticker_urls if sticker_url.endswith('.gif')]
    if len(gif_sticker_urls) > limit:
        return gif_sticker_urls[:limit]
    normal_sticker_urls = [sticker_url for sticker_url in sticker_urls if not sticker_url.endswith('.gif')]
    sticker_urls = gif_sticker_urls + normal_sticker_urls
    return sticker_urls[:limit]


def get_sticker_urls(sticker_name, limit=18, shuffle=True):
    sticker_urls = []

    sticker_urls += get_sticker_urls_from_fabiaoqing(sticker_name, limit=int(limit * 2 / 3))
    if len(sticker_urls) < limit:
        sticker_urls += get_sticker_urls_from_sogou(sticker_name, limit=int(limit * 1 / 3))
    if len(sticker_urls) < limit:
        sticker_urls += get_sticker_urls_from_doutula(sticker_name, limit=0)
    if len(sticker_urls) < limit:
        sticker_urls += get_sticker_urls_from_google(sticker_name, limit=0)

    sticker_urls = sticker_urls[:limit] or []
    if shuffle:
        random.shuffle(sticker_urls)
    return sticker_urls


def send_stickers_with_keyword_to_chat(sticker_name, chat, count=3, send_fail_message=True):
    print('开始搜索：{}'.format(sticker_name))
    sticker_urls = get_sticker_urls(sticker_name)
    sent_count = 0
    for idx, sticker_url in enumerate(sticker_urls):
        if sent_count + 1 > count:
            return
        print('开始发送第{}张，原链接为 {}'.format(idx + 1, sticker_url))
        try:
            if sticker_url.endswith('.gif'):
                ext = 'gif'
            else:
                ext = os.path.splitext(urllib.parse.urlparse(sticker_url).path)[1].lstrip('.')
            base = slugify('{}-{}-{}'.format(__name__, time.time(), sticker_name))
            sticker = '{}.{}'.format(base, ext)
            sticker = os.path.join(tempdir, sticker)
            urllib.request.urlretrieve(sticker_url, sticker)
            sticker_size_in_mb = os.path.getsize(sticker) / 1024 / 1024
            if ext == 'gif' and sticker_size_in_mb < 0.1:
                print('动图文件大小{}MB太小，质量高几率较差，跳过发送'.format(round(sticker_size_in_mb, 2)))
                continue
            with Img(fp=sticker) as im:
                w, h = im.size
                if w < 180:
                    print('图片尺寸{}×{}太小，质量高几率较差，跳过发送'.format(w, h))
                    continue
                if sticker_size_in_mb > 10:
                    thumb_w = 180
                    thumb_h = int(thumb_w / w * h)
                    im.resize((thumb_w, thumb_h))
                    sticker = '{}.thumb.{}'.format(base, ext)
                    sticker = os.path.join(tempdir, sticker)
                    im.save(fp=sticker)
                sticker_size_in_mb = os.path.getsize(sticker) / 1024 / 1024
                if sticker_size_in_mb > 10:
                    print('压缩后大小为{}MB，可能超过微信限制，跳过发送'.format(round(sticker_size_in_mb, 2)))
                    continue
                print('压缩后大小减少为{}MB'.format(round(sticker_size_in_mb, 2)))
            time.sleep(0.8)
            chat.send_image(sticker)
            sent_count += 1
        except Exception as e:
            print('发送{}失败'.format(sticker), e)
            if (getattr(e, 'err_code', None) == 1205):
                print('已达到微信限制频率', e)
                if send_fail_message:
                    chat.send('我被封了，先休息会')
                return
    if sent_count == 0:
        print('未发送任何表情')
        if send_fail_message:
            chat.send('我这没有{}表情'.format(sticker_name))


def send_gif_stickers_with_keyword_to_chat(sticker_name, chat, count=3, send_fail_message=True):
    print('开始搜索：{}'.format(sticker_name))
    sticker_urls = get_sticker_urls(sticker_name, limit=240, shuffle=True)
    if sticker_name == '加油':
        sticker_urls = [
            'http://img01.sogoucdn.com/app/a/200678/62e9a448c191324efb3802da9db56e84.gif',
            'http://img01.sogoucdn.com/app/a/200678/15107319259024.gif',
            'http://img01.sogoucdn.com/app/a/200678/924818e2060226414b626e3d06425445.gif',
            'http://img01.sogoucdn.com/app/a/200678/93a591fd45aefd06e783164d2bfddf7e.gif',
            'http://img01.sogoucdn.com/app/a/200678/3b4a7c3079fc9fa5606a8e854b7fffce.gif',
        ]
    sent_count = 0
    sticker_urls = filter(lambda u:u.endswith('.gif'), sticker_urls)
    for idx, sticker_url in enumerate(sticker_urls):
        if sent_count + 1 > count and sticker_name != '加油':
            return
        try:
            if not sticker_url.endswith('.gif'):
                continue

            print('开始发送第{}张，原链接为 {}'.format(idx + 1, sticker_url))
            ext = 'gif'
            base = slugify('{}-{}-{}'.format(__name__, time.time(), sticker_name))
            sticker = '{}.{}'.format(base, ext)
            sticker = os.path.join(tempdir, sticker)
            urllib.request.urlretrieve(sticker_url, sticker)
            sticker_size_in_mb = os.path.getsize(sticker) / 1024 / 1024
            if ext == 'gif' and sticker_size_in_mb < 0.1:
                print('动图文件大小{}MB太小，质量高几率较差，跳过发送'.format(round(sticker_size_in_mb, 2)))
                continue
            chat.send_image(sticker)
            sent_count += 1
        except Exception as e:
            print('发送{}失败'.format(sticker), e)
            if (getattr(e, 'err_code', None) == 1205):
                print('已达到微信限制频率', e)
                if send_fail_message:
                    chat.send('我被封了，先休息会')
                return
    if sent_count == 0:
        print('未发送任何表情')
        if send_fail_message:
            chat.send('我这没有{}表情'.format(sticker_name))
