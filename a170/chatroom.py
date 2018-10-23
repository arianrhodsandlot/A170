# coding: utf-8
import os
import itchat

chatroom_name = os.getenv('A170_CHATROOM_NAME', 'a170')

itchat.auto_login(enableCmdQR=2, hotReload=True)
chatroom = itchat.search_chatrooms(chatroom_name)[0]
