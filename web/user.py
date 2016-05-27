#!/bin/env python3
#coding:utf-8
#用户管理以及项目操作
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User
from .models import Host,Language,Status,Team,NginxHost,HostStatus
from .base import encode,decode
@login_required(login_url=reverse_lazy('login'))
def createuser(request):
    teamall=Team.objects.all()
    if request.method == 'POST':
        name=request.POST.get('name',None)
        username=request.POST.get('loginname',None)
        email=request.POST.get('email',None)
        superuser=request.POST.get('superuser',None)
        teamid=request.POST.getlist('team')
        password="1"
        if superuser=="0":
            user=User.objects.create_user(username=username,email=email,password=password)
        else:
            user=User.objects.create_superuser(username=username,email=email,password=password)
        user.first_name=name
        user.save()
        user=User.objects.get(username=username)
        for id in teamid:
            team=Team.objects.get(id=id)
            team.userid.add(user)
        return render(request, 'user.html',{"msg":"添加成功",'teamall':teamall})
    else:
        return render(request, 'user.html',{'teamall':teamall})

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
def teamall(request):
    teamall=Team.objects.all()
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
        nginxhost=request.POST.get('nginxhost')
        encodepwd=encode(hostpwd)
        hoststuts=HostStatus.objects.get(status='在线')
        if nginxhost =="0":
            if hostport == "":
                Host.objects.create(hostip=hostip,hostpwd=encodepwd,user=hostuser,status=hoststuts)
            else:
                Host.objects.create(hostip=hostip,hostpwd=encodepwd,user=hostuser,port=int(hostport),status=hoststuts)
        else:
            if hostport == "":
                NginxHost.objects.create(hostip=hostip,hostpwd=encodepwd,user=hostuser,status=hoststuts)
            else:
                NginxHost.objects.create(hostip=hostip,hostpwd=encodepwd,user=hostuser,port=int(hostport),status=hoststuts)
        return render(request,'createhost.html',{"msg":"新增成功"})
    else:
        return render(request,'createhost.html')

@login_required(login_url=reverse_lazy('login'))
def agentteam(request):

    if request.method=="POST":
        teamname=request.POST.get('team',None)
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

@login_required(login_url=reverse_lazy('login'))
def createteam(request):
    hostall=Host.objects.all()
    language=Language.objects.all()
    nhost=NginxHost.objects.all()
    if request.method=='POST':
        host=request.POST.getlist('host')
        teamname=request.POST.get('teamname')
        teampath=request.POST.get('teampath')
        teamport=request.POST.get('teamport')
        svnpath=request.POST.get('svnpath')
        svnuser=request.POST.get('svnuser')
        svnpwd=request.POST.get('svnpwd')
        nginxpath=request.POST.get('nginxpath')
        nginxhost=request.POST.getlist('nginxhost')
        nginxupstream=request.POST.get('nginxupstream')
        url=request.POST.get('url')
        teamlanguage=request.POST.get('teamlanguage')
        ps=request.POST.get('ps')
        languageid=Language.objects.get(id=teamlanguage)
        if nginxupstream=="":
            nginxupstream=teamname
        Team.objects.create(groupname=teamname,language_id=languageid,teamport=teamport,url=url,path=teampath,svnpath=svnpath,svnpwd=svnpwd,nginxconf=nginxpath,nginxupstream=nginxupstream,svnuser=svnuser,ps=ps)
        team=Team.objects.get(groupname=teamname)
        for h in host:
            hostid=Host.objects.get(id=h)
            team.host.add(h)
        for nh in nginxhost:
            nhid=NginxHost.objects.get(id=nh)
            team.nginxhost.add(nhid)
        return redirect(reverse("teamall"))
    else:
        return render(request,'createteam.html',{"language":language,"hostall":hostall,"nginxhost":nhost})
