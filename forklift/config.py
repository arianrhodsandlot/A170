# coding: utf-8
import os
from dotenv import load_dotenv

load_dotenv()

FORKLIFT_CHATROOM_NAME = os.getenv('FORKLIFT_CHATROOM_NAME', 'forklift')

EVERY_REPLY_SEND_COUNT = 3

STICKERS_FOR_SPAM = [
    'http://ww4.sinaimg.cn/bmiddle/6af89bc8gw1f8qr12jbhmg208c05ktrd.gif',
    'http://ww3.sinaimg.cn/bmiddle/6af89bc8gw1f8qkn6x1oog20b40b4474.gif',
    'http://ww4.sinaimg.cn/bmiddle/6af89bc8gw1f8r6bfidweg205m05owwm.gif',
    'http://ww4.sinaimg.cn/bmiddle/6af89bc8gw1f8r1cnnansj20ix0jt0t6.jpg',
    'http://ww2.sinaimg.cn/bmiddle/6af89bc8gw1f8rgjyw2nkj205i05ijr7.jpg',
    'http://ws2.sinaimg.cn/bmiddle/9150e4e5ly1ffua6th8zdj205i05i749.jpg',
    'http://wx3.sinaimg.cn/bmiddle/006APoFYly1fobpj18rnsj30dc0dcaaj.jpg',
    'http://ws1.sinaimg.cn/bmiddle/9150e4e5ly1fnrsxrym57j207806ddfy.jpg',
    'http://ww1.sinaimg.cn/bmiddle/6af89bc8gw1f8nur6xnswj209c06hdg4.jpg',
    'http://ws3.sinaimg.cn/large/9150e4e5ly1frx7a15j3hj205i05imxi.jpg',
    'http://ww3.sinaimg.cn/bmiddle/6af89bc8gw1f8spfp38vcg206y056tlk.gif',
    'http://image.bee-ji.com/59490',
    'http://image.bee-ji.com/25019',
    'http://image.bee-ji.com/59485',
]

LOG_DIRNAME = 'log'
LOG_FILENAME = 'forklift-log.log'

LOG_TEMPLATE_START_SEND = os.getenv('LOG_TEMPLATE_SEND_DOWNLOAD', '开始发送 {}')
LOG_TEMPLATE_DOWNLOAD_FAILED = os.getenv('LOG_TEMPLATE_DOWNLOAD_FAILED', '下载 {} 失败')
LOG_TEMPLATE_UPLOAD_FAILED = os.getenv('LOG_TEMPLATE_UPLOAD_FAILED', '上传 {} 失败')
LOG_TEMPLATE_SEND_FAILED = os.getenv('LOG_TEMPLATE_SEND_FAILED', '发送 {} 失败')
LOG_TEMPLATE_SEARCH_COUNT = os.getenv('LOG_TEMPLATE_SEARCH_COUNT', '从 {} 搜索到{}个图片')
LOG_TEMPLATE_TOO_FEW_SKIP = os.getenv('LOG_TEMPLATE_TOO_FEW_SKIP', '数量太少跳过')
LOG_TEMPLATE_LOGIN = os.getenv('LOG_TEMPLATE_LOGIN', 'Log in')
LOG_TEMPLATE_LOGOUT = os.getenv('LOG_TEMPLATE_LOGOUT', 'Log out')

REPLY_TEMPLATE_SPAM = os.getenv('REPLY_TEMPLATE_SPAM', '@{} 逮住个发广告的！')

QUERY_AND_QUERY_TYPE_REG = r'(求|有没有|谁有)\s*(?P<query>.+)\s*(?P<query_type>表情|动图)'
ANIMATED_QUERY_TYPE = '动图'

GIFT_MONEY_KEYWORD = os.getenv('GIFT_MONEY_KEYWORD', '红包')
GIFT_MONEY_STICKER_QUERY = os.getenv('GIFT_MONEY_STICKER_QUERY', '谢谢老板')

REPORT_GMAIL = os.getenv('REPORT_GMAIL')
REPORT_GMAIL_PASSWORD = os.getenv('REPORT_GMAIL_PASSWORD')
REPORT_MAIL_SUBJECT = os.getenv('REPORT_MAIL_SUBJECT', 'Forklift log out!')
REPORT_MAIL_BODY = os.getenv('REPORT_MAIL_BODY', REPORT_MAIL_SUBJECT)
