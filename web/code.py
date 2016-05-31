#!/bin/env python3
#coding:utf-8
#代码操作
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User
from .models import Team,Host,Status,Code,NginxHost
from .base import encode,decode
import paramiko,re
import time
import os
from multiprocessing import Pool

class update:
    def __init__(self,hostip,port,username,password,updatefile,filename,teamnameid,teamhost):
        self.updatefile=updatefile
        self.filename=filename
        self.teamnameid=teamnameid
        self.teamhost=teamhost
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
        self.ssh.exec_command('mv -rf {0} {1}/{2}'.format(self.teamhost.host,'/backup',self.teamhost.path+time.strftime("%Y-%m-%d",time.localtime())))
    #替换文件
    #回滚
    def goback(self):
        pass

class nginx:
    def __init__(self,host,teamnameid,nginxconf):
        self.teamnameid=teamnameid
        self.nginxconf=nginxconf
        self.ssh=paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host.hostip,host.port,host.username,host.hostpwd)
    def downteam(self):
        pass
        #下线一台机器，写数据库
        #重启
    def upteam(self):
        pass
        #上线机器，写数据库
def curl(url):
    import urllib.request
    try:
        urllib.request.urlopen(url)
        return True
    except:
        return False
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
                u=update(host.hostip,host.port,host.user,decode(host.hostpwd),pathname,file.name,teamname,teamhost)
                p.apply_async(u.update())
            p.close()
            p.join()
        status=Status.objects.get(status='等待更新')
        Code.objects.create(team=teamhost,path=pathname,status=status,user=userid)
        return render(request,'upload.html',{"msg":"已经上传成功，请前往发布列表页进行发布","teamall":teamall})
    return render(request,'upload.html',{"teamall":teamall})

@login_required(login_url=reverse_lazy('login'))
def status(request):

    return render(request, 'status.html')

@login_required(login_url=reverse_lazy('login'))
def updateall(request):
    user=User.objects.get(username=request.user)
    if user.is_superuser:
        updateall=Code.objects.all()
        return render(request,'updateall.html',{'updateall':updateall})
    else:
        updateall=Code.objects.filter(user=user)
        return render(request,'updateall.html',{'updateall':updateall})


@login_required(login_url=reverse_lazy('login'))
def backall(request):
    status=Status.objects.get(status="回退")
    backall=Code.objects.filter(status=status)
    return render(request,'backall.html',{"backall":backall})

@login_required(login_url=reverse_lazy('login'))
def tree(request):
    return render(request,'phptree.html')

@login_required(login_url=reverse_lazy('login'))
def release(request):
    if request.method=="POST":
        id=request.POST.get("id")
        code=Code.objects.get(id=id)
        status=Status.objects.get(status="正在发布")
        code.status=status
        code.save()
        #涉及灰度发布
        #摘nginx
        nginxhosts=code.team.nginxhost.all()#所有nginx
        nginxconf=code.team.nginxconf #nginx的配置文件
        nginxupstream=code.team.nginxupstream #nginx的upstream
        teamhosts=code.team.host.all() #项目的所有主机
        p=Pool(5)
        for nginxhost in nginxhosts:
            nginx=nginx(nginxhost,id,nginxconf)
            p.apply_async(nginx.downteam())
        p.close()
        p.join()
        #重启
        #备份
        #测试
        #回退
        #重启
        return HttpResponse('OK')