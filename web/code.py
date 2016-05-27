#!/bin/env python3
#coding:utf-8
#代码操作
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User
from .models import Team,Host,Status
from .base import encode,decode
import paramiko,re
import time
import os
from multiprocessing import Pool

#上传文件
def update(hostip,port,username,password,updatefile,filename,teamnameid):
    t=paramiko.Transport(hostip,port)
    t.connect(username=username,password=password)
    sftp=paramiko.SFTPClient.from_transport(t)
    try:
        sftp.mkdir('/update',mode=0o755)
    except:
        pass
    sftp.put(updatefile,'{0}/{1}'.format('/update',filename),)
    t.close()
    team=Team.objects.get(id=teamnameid)
    status=Status.objects.get(status='等待更新')
    team.status.add(status)
#重启nginx,默认nginx使用www用户启动
def nginx(hostip,port,username,password):
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip,port,username,password)

    comm="sed -i 's/\(server {0} .*;\)/'"
    stdin,stdout,stderr=ssh.exec_command('ls')

#重启tomcat，默认tomcat使用app用户启动
def nginx(hostip,port,username,password):
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip,port,username,password)
    comm="sed -i 's/\(server {0} .*;\)/'"
    stdin,stdout,stderr=ssh.exec_command('ls')

#备份
def backup():
    pass

#回滚
def back():
    pass

#多进程

@login_required(login_url=reverse_lazy('login'))
def code(request):
    teamall=Team.objects.all()
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
            #cp文件，重启服务，返回结果
            #这里应该用多进程写
            p=Pool(5)
            for host in teamhost.host.all():
                p.apply_async(update,args=(host.hostip,host.port,host.user,decode(host.hostpwd),pathname,file.name,teamname))
            p.close()
            p.join()
            return render(request,'upload.html',{"msg":"已经成功上传,正在发布，请关注邮箱，在发布完成，系统会发送邮件给你"})
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