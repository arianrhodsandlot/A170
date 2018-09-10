#!/usr/bin/env python
# coding: utf-8
from wxpy import *
from requests_html import HTMLSession
import urllib.request
import urllib.parse
import uuid
import time
import os
import random
import re

group_name = 'a170'

session = HTMLSession()
bot = Bot()
group = ensure_one(bot.groups().search(group_name))

def get_sticker_name(msg):
    sticker_name = re.search('求(.*)表情', msg)
    if sticker_name:
        sticker_name = sticker_name.group(1)
        return sticker_name.strip()
    return ''

def get_sticker_urls(sticker_name):
    r = session.get('https://www.fabiaoqing.com/search/search/keyword/' + sticker_name)
    sticker_els = r.html.find('.searchbqppdiv .image')
    sticker_urls = [sticker_el.attrs.get('data-original') for sticker_el in sticker_els]
    animate_sticker_urls = []
    static_sticker_urls = []
    for sticker_url in sticker_urls:
        ext = os.path.splitext(urllib.parse.urlparse(sticker_url).path)[1]
        if ext == '.gif':
            animate_sticker_urls.append(sticker_url)
        else:
            static_sticker_urls.append(sticker_url)
    final_stiker_urls = animate_sticker_urls + static_sticker_urls
    print('搜到' + str(len(final_stiker_urls)) + '张表情包')
    print(str(len(animate_sticker_urls)) + '动图')
    print(str(len(static_sticker_urls)) + '不动图')
    return final_stiker_urls

def get_stickers(sticker_name):
    sticker_urls = get_sticker_urls(sticker_name)
    stickers = []
    for sticker_url in sticker_urls:
        ext = os.path.splitext(urllib.parse.urlparse(sticker_url).path)[1]
        sticker = 'tmp/' + str(uuid.uuid1()) + ext
        urllib.request.urlretrieve(sticker_url, sticker)
        stickers.append(sticker)
    return stickers, sticker_urls

@bot.register()
def print_messages(msg):
    print(msg)

@bot.register()
def reply_message(msg):
    print('收到信息：' + msg)
    sticker_name = get_sticker_name(msg)
    if not sticker_name:
        print('不需进行自动回复')
        return
    print('开始搜索：' + sticker_name)
    stickers, sticker_urls = get_stickers(sticker_name)
    if not stickers:
        return
    sent_count = 0
    for idx, sticker in enumerate(stickers):
        if sent_count > 5:
            return
        try:
            print('开始发送第' + str(idx) + '张，原链接为 ' + sticker_urls[idx])
            group.send_image(sticker)
            sent_count += 1
            time.sleep(0.6)
        except Exception as e:
            print('发送失败', e)

embed(shell='i')
