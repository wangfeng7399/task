#!/usr/bin/env python3
#coding:utf-8
#公用的模块
import base64
import smtplib
import logging
import logging.handlers
from email.mime.text import MIMEText


def ec(str):
    encodestr=base64.b64encode(str.encode())
    return encodestr.decode()
def dc(str):
    decodestr=base64.b64decode(str)
    return decodestr.decode()

def send_mail(to_list,sub,content):
    mail_host="smtp.51credit.com"
    mail_user='alert2@51credit.com'
    mail_pass='alert2'
    mail_postfix='pop.51credit.com'
    me= mail_user+"<"+mail_user+"@"+mail_postfix+">"
    #msg=MIMEText(content,_charset="utf-8")
    msg=MIMEText(str(content),_charset="utf-8")
    msg["Subject"] =sub
    msg["From"] =me
    msg["To"]=to_list
    s=smtplib.SMTP()
    s.connect(mail_host)
    s.login(mail_user,mail_pass)
    s.sendmail(me,to_list,msg.as_string())
    s.close()


def logfunc():
    logname="python.log"
    log=logging.getLogger()
    sh=logging.handlers.TimedRotatingFileHandler(logname,when="D",interval=1)
    sh.setLevel(logging.DEBUG)
    fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)
    sh.setFormatter(formatter)
    log.addHandler(sh)
    return log