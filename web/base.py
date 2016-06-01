#!/bin/env python3
#coding:utf-8
#公用的模块
import base64
import smtplib
import xlwt
from email.mime.text import MIMEText
def encode(str):
    encodestr=base64.b64encode(str.encode())
    return encodestr.decode()
def decode(str):
    decodestr=base64.b64decode(str)
    return decodestr.decode()

def send_mail(to_list,sub,content):
    mail_host="smtp.51credit.com"
    mail_user='alert2@51credit.com'
    mail_pass='alert'
    mail_postfix='pop.51credit.com'
    me= mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg=MIMEText(content,_charset="utf-8")
    msg["Subject"] =sub
    msg["From"] =me
    msg["To"]=";".join(to_list)
    s=smtplib.SMTP()
    s.connect(mail_host)
    s.login(mail_user,mail_pass)
    s.sendmail(me,to_list,msg.as_string())
    s.close()
def excel():
    import xlrd
    data=xlrd.open_workbook("test.xls")
    table=data.sheets()[0]
    nrows=table.nrows
    ncols=table.ncols
    for r in range(nrows):
        for c in range(ncols):
            print("{0}行{1}列的数据为{2}".format(r+1,c+1,table.cell(r,c).value))