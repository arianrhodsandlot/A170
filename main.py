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

group_name = os.environ.get('A170_GROUP_NAME', 'a170')
tmp_directory = 'tmp'

session = HTMLSession()
bot = Bot(console_qr=True)
group = ensure_one(bot.groups().search(group_name))
if not os.path.exists(tmp_directory):
    os.makedirs(tmp_directory)

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
        if sticker_url.startswith('/'):
            sticker_url = 'https://www.fabiaoqing.com' + sticker_url
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

def respond_with_keyword(sticker_name):
    print('开始搜索：' + sticker_name)
    sticker_urls = get_sticker_urls(sticker_name)
    if not sticker_urls:
        return
    sent_count = 0
    stickers = []
    for idx, sticker_url in enumerate(sticker_urls):
        if sent_count > 4:
            return
        try:
            ext = os.path.splitext(urllib.parse.urlparse(sticker_url).path)[1]
            sticker = tmp_directory + '/' + str(uuid.uuid1()) + ext
            urllib.request.urlretrieve(sticker_url, sticker)
            print('开始发送第' + str(idx + 1) + '张，原链接为 ' + sticker_url)
            group.send_image(sticker)
            sent_count += 1
        except Exception as e:
            if (e.err_code == 1205):
                print('已达到微信限制频率', e)
                return
            print('发送失败', e)
        time.sleep(0.6)

@bot.register(group, SHARING, False)
def reply_spam(msg):
    group.send('@辛仝 发广告的来了')
    respond_with_keyword('发广告的')


@bot.register(group, TEXT, False)
def reply_message(msg):
    print('收到信息：' + msg.text)
    sticker_name = get_sticker_name(msg.text)
    if not sticker_name:
        print('不需进行自动回复')
        return
    respond_with_keyword(sticker_name)

embed(shell='i')
