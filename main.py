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
current_reply_msg = None

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
    print('搜到{}张表情包，{}动图，{}不动图'.format(len(final_stiker_urls), len(animate_sticker_urls), len(static_sticker_urls)))
    random.shuffle(final_stiker_urls)
    return final_stiker_urls

def respond_stickers_with_keyword(sticker_name, silent=False):
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
            sticker_size_in_mb = os.path.getsize(sticker) / 1024 / 1024
            if sticker_size_in_mb > 1:
                print('第' + str(idx + 1) + '张因大小可能超过微信限制跳过发送，原链接为 ' + sticker_url)
                continue
            print('开始发送第' + str(idx + 1) + '张，原链接为 ' + sticker_url)
            group.send_image(sticker)
            sent_count += 1
        except Exception as e:
            print('发送失败', e)
            if (e.err_code == 1205):
                print('已达到微信限制频率', e)
                if not silent:
                    group.send('我暂时被微信封了，其它群友有的帮忙发下')
                return
        time.sleep(0.8)
    if not sent_count and not silent:
        group.send('我这没有{}表情, 其它群友有的帮忙发下'.format(sticker_name))

@bot.register(group, SHARING, False)
def reply_spam(msg):
    print('{}说：{}'.format(msg.sender.name, msg.text))
    group.send('@辛仝 逮住一个广告的')
    respond_stickers_with_keyword('发广告的')


@bot.register(group, TEXT, False)
def reply_message(msg):
    global current_reply_msg
    print('{}说：{}'.format(msg.sender.name, msg.text))
    if current_reply_msg:
        print('由于正在回复上一条，跳过回复此消息')
        if msg.sender.name == current_reply_msg.sender.name:
            group.send('@{} ，我正在给你找{}的图，你等我发完再重新问'.format(msg.sender.name, get_sticker_name(current_reply_msg.text)))
        else:
            group.send('@{} ，我正在给 @{} 找图，你等我发完再重新问'.format(msg.sender.name, current_reply_msg.sender.name))
        return
    current_reply_msg = msg
    sticker_name = get_sticker_name(msg.text)
    if not sticker_name:
        return
    respond_stickers_with_keyword(sticker_name)
    current_reply_msg = None

embed(shell='i')
