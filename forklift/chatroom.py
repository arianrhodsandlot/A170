# coding: utf-8
import itchat
from .config import FORKLIFT_CHATROOM_NAME
from .reporter import report_login, report_logout

itchat.auto_login(enableCmdQR=2, hotReload=True, loginCallback=report_login, exitCallback=report_logout)
chatroom = itchat.search_chatrooms(FORKLIFT_CHATROOM_NAME)[0]
