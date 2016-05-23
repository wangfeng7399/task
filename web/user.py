#!/bin/env python3
#coding:utf-8
#用户管理操作
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User
from .models import Team,Host,Language
from .base import encode,decode
@login_required(login_url=reverse_lazy('login'))
def createuser(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        username=request.POST.get('loginname')
        superuser=request.POST.get('superuser')
        password="1"
        print(type(superuser),superuser)
        if superuser=="0":
            user=User.objects.create_user(username=username,password=password)
        else:
            user=User.objects.create_superuser(username=username,email="",password=password)
        user.first_name=name
        user.save()
    else:
        return render(request, 'user.html')

@login_required(login_url=reverse_lazy('login'))
def agentpasswd(request):
    if request.method == 'POST':
        passwd=request.POST.get('pwd')
        user=User.objects.get(username=request.user)
        user.set_password(passwd)
        user.save()
        return render(request,'agentpasswd.html',{"msg":"修改成功"})
    else:
        return render(request,'agentpasswd.html')

@login_required(login_url=reverse_lazy('login'))
def creategroup(request):
    if request.method=='POST':
        groupname=request.POST.get("groupname")
        Team.objects.get_or_create(groupname=groupname)
        return render(request,'creategroup.html',{"msg":"添加成功"})
    else:
        return render(request,'creategroup.html')

@login_required(login_url=reverse_lazy('login'))
def teamall(request):
    group=Team.objects.all()
    return render(request, 'hostall.html', {"group":group})

@login_required(login_url=reverse_lazy('login'))
def hostall(request):
    group=Team.objects.all()
    return render(request, 'hostall.html', {"group":group})

@login_required(login_url=reverse_lazy('login'))
def createhost(request):
    if request.method=='POST':
        hostip=request.POST.get('hostip')
        hostpwd=request.POST.get('hostpwd')
        teamname=request.POST.get('teamname')
        teampath=request.POST.get('teampath')
        svnpath=request.POST.get('svnpath')
        svnpwd=request.POST.get('svnpwd')
        nginxpath=request.POST.get('nginxpath')
        nginxupstream=request.POST.get('nginxupstream')
        nginxsbin=request.POST.get('nginxsbin')
        ps=request.POST.get('ps')
        encodepwd=encode(hostpwd)

        Host.objects.create(hostip=hostip,hostpwd=encodepwd,path=teampath,svnpath=svnpath,svnpwd=svnpwd,nginxpath=nginxpath,nginxsbin=nginxsbin,nginxupstream=nginxupstream,ps=ps)
        return render(request,'createhost.html')
    else:
        return render(request,'createhost.html')

def test(request):
    if request.method == 'POST':
        data=request.POST.get('data')
        print(data)
        return HttpResponse('ok!')

@login_required(login_url=reverse_lazy('login'))
def agentteam(request):
    if request.method=="POST":
        teamname=request.POST.get('team')
        team=Team.objects.filter(groupname=teamname).count()
        if team !=0:
            return HttpResponse('项目已经存在')
        else:
            return HttpResponse('项目可以添加')

@login_required(login_url=reverse_lazy('login'))
def createlanguage(request):
    if request.method=='POST':
        language=request.POST.get("language")
        Language.objects.get_or_create(language=language)
        return render(request,'createlanguage.html',{"msg":"添加成功"})
    else:
        return render(request,'createlanguage.html')


@login_required(login_url=reverse_lazy('login'))
def agentteam(request):
    if request.method=="POST":
        teamname=request.POST.get('team')
        team=Team.objects.filter(groupname=teamname).count()
        if team !=0:
            return HttpResponse('项目已经存在')
        else:
            return HttpResponse('项目可以添加')

@login_required(login_url=reverse_lazy('login'))
def agentlanguage(request):
    if request.method=="POST":
        teamname=request.POST.get('team')
        team=Team.objects.filter(groupname=teamname).count()
        if team !=0:
            return HttpResponse('项目已经存在')
        else:
            return HttpResponse('项目可以添加')