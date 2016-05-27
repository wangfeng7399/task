#!/bin/env python3
#coding:utf-8
#代码操作
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User
from .models import Team,Host,Status,Code
from .base import encode,decode
import paramiko,re
import time
import os
from multiprocessing import Pool
class nginx:
    def __init__(self,hostip,port,username,password,teamnameid,nginxconf):
        self.ssh=paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostip,port,username,password)
        #随机取一台机器
    def downteam(self):
        pass
        #下线一台机器，写数据库
    def upteam(self):
        pass
        #上线机器，写数据库
    def curl(self):
        pass
        #判断状态
class update:
    def __init__(self,hostip,port,username,password,updatefile,filename,teamnameid):
        self.updatefile=updatefile
        self.filename=filename
        self.teamnameid=teamnameid
        self.t=paramiko.Transport(hostip,port)
        self.t.connect(username=username,password=password)
        self.sftp=paramiko.SFTPClient.from_transport(self.t)
        self.team=Team.objects.get(id=teamnameid)
        self.ssh=paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostip,port,username,password)
    #上传文件
    def update(self):
        try:
            self.sftp.mkdir('/update',mode=0o755)
        except:
            pass
        self.sftp.put(self.updatefile,'{0}/{1}'.format('/update',self.filename),)
        self.t.close()
    #备份
    def backup(self):
        time.sleep(100)

    #回滚
    def goback(self):
        pass
    #多进程

@login_required(login_url=reverse_lazy('login'))
def code(request):
    userid=User.objects.get(username=request.user)
    teamall=Team.objects.filter(userid=userid).all()
    if request.method =="POST":
        filename=request.FILES.getlist('files[]')
        teamname=request.POST.get('teamname')
        teamhost=Team.objects.get(id=teamname)
        path='{0}/{1}/{2}'.format('/opt',request.user,time.strftime("%Y-%m-%d",time.localtime()),)
        if not os.path.exists(path):
            os.makedirs(path)
        for file in filename:
            pathname='{0}/{1}'.format(path,file.name)
            with open(pathname,'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            p=Pool(5)
            for host in teamhost.host.all():
                u=update(host.hostip,host.port,host.user,decode(host.hostpwd),pathname,file.name,teamname)
                p.apply_async(u.update())
            p.close()
            p.join()
        status=Status.objects.get(status='等待更新')
        Code.objects.create(team=teamhost,path=pathname,status=status,user=userid)
        p=Pool(5)
        for host in teamhost.host.all():
            u=update(host.hostip,host.port,host.user,decode(host.hostpwd),pathname,file.name,teamname)
            p.apply_async(u.backup())
        return render(request,'upload.html',{"msg":"已经成功上传,正在发布，请关注邮箱，在发布完成，系统会发送邮件给你","teamall":teamall})
    return render(request,'upload.html',{"teamall":teamall})

@login_required(login_url=reverse_lazy('login'))
def status(request):
    return render(request, 'status.html')


def updateall(request):
    return render(request,'updateall.html')

def backall(request):
    return render(request,'backall.html')


def tree(request):
    return render(request,'phptree.html')