#!/bin/env python3
#coding:utf-8
#用户管理以及项目操作
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User
from .models import TeamGroup,Host,Language,Status,Team
from .base import encode,decode
@login_required(login_url=reverse_lazy('login'))
def createuser(request):
    if request.method == 'POST':
        name=request.POST.get('name',None)
        username=request.POST.get('loginname',None)
        email=request.POST.get('email',None)
        superuser=request.POST.get('superuser',None)
        password="1"
        if superuser=="0":
            user=User.objects.create_user(username=username,email=email,password=password)
        else:
            user=User.objects.create_superuser(username=username,email=email,password=password)
        user.first_name=name
        user.save()
        return render(request, 'user.html',{"msg":"添加成功"})
    else:
        return render(request, 'user.html')

@login_required(login_url=reverse_lazy('login'))
def agentpasswd(request):
    if request.method == 'POST':
        passwd=request.POST.get('pwd',None)
        user=User.objects.get(username=request.user)
        user.set_password(passwd)
        user.save()
        return render(request,'agentpasswd.html',{"msg":"修改成功"})
    else:
        return render(request,'agentpasswd.html')

@login_required(login_url=reverse_lazy('login'))
def creategroup(request):
    if request.method=='POST':
        groupname=request.POST.get("groupname",None)
        TeamGroup.objects.get_or_create(groupname=groupname)
        return render(request,'creategroup.html',{"msg":"添加成功"})
    else:
        return render(request,'creategroup.html')

@login_required(login_url=reverse_lazy('login'))
def teamall(request):
    teamall=TeamGroup.objects.all()
    for team in teamall:
        print(team.team_set)
    return render(request, 'teamall.html', {"teamall":teamall})

@login_required(login_url=reverse_lazy('login'))
def userall(request):
    user=User.objects.all()
    return render(request, 'userall.html',{"userall":user})

@login_required(login_url=reverse_lazy('login'))
def createhost(request):
    if request.method=='POST':
        hostip=request.POST.get('hostip')
        hostpwd=request.POST.get('hostpwd')
        hostuser=request.POST.get('hostuser')
        hostport=request.POST.get('hostport')
        encodepwd=encode(hostpwd)
        if hostport == "":
            Host.objects.create(hostip=hostip,hostpwd=encodepwd,user=hostuser)
        else:
            Host.objects.create(hostip=hostip,hostpwd=encodepwd,user=hostuser,port=int(hostport))
        return render(request,'createhost.html',{"msg":"新增成功"})
    else:
        return render(request,'createhost.html')

@login_required(login_url=reverse_lazy('login'))
def agentteam(request):

    if request.method=="POST":
        teamname=request.POST.get('team',None)
        team=TeamGroup.objects.filter(groupname=teamname).count()
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
        teamname=request.POST.get('team',None)
        team=TeamGroup.objects.filter(groupname=teamname).count()
        if team !=0:
            return HttpResponse('项目已经存在')
        else:
            return HttpResponse('项目可以添加')

@login_required(login_url=reverse_lazy('login'))
def agentlanguage(request):
    if request.method=="POST":
        language=request.POST.get('language',None)
        language_rust=Language.objects.filter(language=language).count()
        if language_rust !=0:
            return HttpResponse('项目语言已经存在')
        else:
            return HttpResponse('项目语言可以添加')

@login_required(login_url=reverse_lazy('login'))
def agentstatus(request):
    if request.method=="POST":
        status=request.POST.get('status',None)
        status_rust=Status.objects.filter(status=status).count()
        if status_rust !=0:
            return HttpResponse('状态已经存在')
        else:
            return HttpResponse('状态可以添加')

@login_required(login_url=reverse_lazy('login'))
def createstatus(request):
    if request.method=='POST':
        status=request.POST.get("status",None)
        Status.objects.get_or_create(status=status)
        return render(request,'createstatus.html',{"msg":"添加成功"})
    else:
        return render(request,'createstatus.html')

def createteam(request):
    hostall=Host.objects.all()
    language=Language.objects.all()
    teamall=TeamGroup.objects.all()
    if request.method=='POST':
        host=request.POST.get('host')
        teamname=request.POST.get('teamname')
        teampath=request.POST.get('teampath')
        teamport=request.POST.get('teamport')
        svnpath=request.POST.get('svnpath')
        svnuser=request.POST.get('svnuser')
        svnpwd=request.POST.get('svnpwd')
        nginxpath=request.POST.get('nginxpath')
        nginxupstream=request.POST.get('nginxupstream')
        url=request.POST.get('url')
        teamlanguage=request.POST.get('teamlanguage')
        ps=request.POST.get('ps')
        languageid=Language.objects.get(id=teamlanguage)
        teamgroup=TeamGroup.objects.get(id=teamname)
        hostid=Host.objects.get(id=host)
        port=hostid.hostip+":"+teamport
        Team.objects.create(teamid=teamgroup,language_id=languageid,teamport=port,path=teampath,svnpath=svnpath,svnpwd=svnpwd,nginxconf=nginxpath,nginxupstream=nginxupstream,svnuser=svnuser,ps=ps)
        team=Team.objects.get(teamport=port)
        team.host.add(hostid)
        return redirect(reverse("teamall"))
    else:
        return render(request,'createteam.html',{"language":language,"teamall":teamall,"hostall":hostall})
