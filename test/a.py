'''
import  os
def createdict(path):
    list=[]
    for p,item in enumerate(os.listdir(path)):
        children={}
        children["text"]=item
        if os.path.join(path,item):
            if len(os.listdir(os.path.join(path,item))) !=0:
                children["children"]=createdict(path)
            list.append(children)
        else:
            list.append(children)
    return list


c=createdict("/root")
print(c)
'''
'''
import  os,json,sys
def tree(path):
    list=[]
    for item in os.listdir(path):
        temp=os.path.join(path,item)
        if not os.path.isdir(temp):
            list.append({"text":item})
        else:
            list.append({"text":item,"children":tree(temp)})
    return list
print(json.dumps(tree(sys.argv[1]),ensure_ascii=False))
print()
'''
import smtplib
from email.mime.text import MIMEText
def send_mail(to_list,sub,content):
    mail_host="smtp.51credit.com"
    mail_user='alert2@51credit.com'
    mail_pass='alert2'
    mail_postfix='pop.51credit.com'
    me= mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg=MIMEText(content,_charset="utf-8")
    msg["Subject"] =sub
    msg["From"] =me
    msg["To"]=to_list
    s=smtplib.SMTP()
    s.connect(mail_host)
    s.login(mail_user,mail_pass)
    s.sendmail(me,to_list,msg.as_string())
    s.close()


send_mail('wangshenghui@51credit.com','test','test')