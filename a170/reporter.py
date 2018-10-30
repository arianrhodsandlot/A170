# coding: utf-8
import yagmail
from .config import (LOG_TEMPLATE_LOGIN, LOG_TEMPLATE_LOGOUT, REPORT_GMAIL, REPORT_GMAIL_PASSWORD,
                     REPORT_MAIL_SUBJECT, REPORT_MAIL_BODY)
from .logger import logger


def report_login():
    logger.success(LOG_TEMPLATE_LOGIN)


yag = None
if REPORT_GMAIL and REPORT_GMAIL_PASSWORD:
    yag = yagmail.SMTP(REPORT_GMAIL, REPORT_GMAIL_PASSWORD)


def report_logout():
    logger.critical(LOG_TEMPLATE_LOGOUT)
    if yag:
        yag.send(REPORT_GMAIL, REPORT_MAIL_SUBJECT, REPORT_MAIL_BODY)
