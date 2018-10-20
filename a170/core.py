# coding: utf-8
import os
import re
import itchat
from a170.helpers import send_stickers_with_keyword_to_chat, send_gif_stickers_with_keyword_to_chat


chatroom_name = os.environ.get('A170_CHATROOM_NAME', 'a170')

itchat.auto_login(enableCmdQR=2, hotReload=True)

chatroom = itchat.search_chatrooms(chatroom_name)[0]
chatroom_owner = chatroom.memberList[0]

current_reply_msg = None


def reply_sharing():
    print('{}说：{} {}'.format(msg.actualNickName, msg.text, msg.url))
    chatroom.send('@{} 逮住个发广告的！'.format(chatroom_owner.nickName))
    send_stickers_with_keyword_to_chat(sticker_name='发广告的', chat=chatroom, send_fail_message=True)


def reply_note():
    send_stickers_with_keyword_to_chat(sticker_name='谢谢老板', chat=chatroom, send_fail_message=True)


def reply_text():
    print('{}说：{}'.format(msg.actualNickName, msg.text))
    global current_reply_msg
    sticker_name = re.search('求(.*)表情', msg.text)
    gif_sticker_name = re.search('求(.*)动图', msg.text)
    if sticker_name:
        sticker_name = sticker_name.group(1).strip()
    if gif_sticker_name:
        gif_sticker_name = gif_sticker_name.group(1).strip()
    if not sticker_name and not gif_sticker_name:
        return
    if current_reply_msg:
        print('由于正在回复上一条{}，跳过回复此消息'.format(current_reply_msg.sender))
        return
    current_reply_msg = msg
    if sticker_name:
        send_stickers_with_keyword_to_chat(sticker_name, chat=chatroom)
    elif gif_sticker_name:
        send_gif_stickers_with_keyword_to_chat(gif_sticker_name, chat=chatroom)
    current_reply_msg = None


supported_msg_types = [itchat.content.TEXT, itchat.content.SHARING, itchat.content.NOTE]
@itchat.msg_register(supported_msg_types, isGroupChat=True)
def _(msg):
    if msg.toUserName != chatroom.userName:
        return
    if msg.type == itchat.content.SHARING:
        reply_sharing()
    elif msg.type == itchat.content.NOTE:
        reply_note()
    elif msg.type == itchat.content.TEXT:
        reply_text()

itchat.run(blockThread=False)
