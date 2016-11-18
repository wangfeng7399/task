#!/usr/bin/env python3
#coding:utf-8
#用户管理以及项目操作
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User
from .models import Host,Language,Status,Team,NginxHost,HostStatus
from .base import ec
@login_required(login_url=reverse_lazy('login'))
def createuser(request):
    teamall=Team.objects.all()
    if request.method == 'POST':
        name=request.POST.get('name',None)
        username=request.POST.get('loginname',None)
        email=request.POST.get('email',None)
        superuser=request.POST.get('superuser',None)
        teamid=request.POST.getlist('my_multi_select1[]')
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
        hostname=request.POST.get('hostname')
        hostip=request.POST.get('hostip')
        #hostpwd=request.POST.get('hostpwd')
        hostuser=request.POST.get('hostuser')
        hostport=request.POST.get('hostport')
        nginxhost=request.POST.get('nginxhost')
        dev=request.POST.get("dev")
        print(dev)
        #encodepwd=ec(hostpwd)
        hoststatus=HostStatus.objects.get(id=dev)
        if nginxhost =="0":
            if hostport == "":
                #Host.objects.create(hostname=hostname,hostip=hostip,hostpwd=encodepwd,user=hostuser,status=hoststuts)
                Host.objects.create(hostname=hostname,hostip=hostip,user=hostuser,status=hoststatus)
            else:
                #Host.objects.create(hostname=hostname,hostip=hostip,hostpwd=encodepwd,user=hostuser,port=int(hostport),status=hoststuts)
                Host.objects.create(hostname=hostname,hostip=hostip,user=hostuser,port=int(hostport),status=hoststatus)
        else:
            if hostport == "":
                #NginxHost.objects.create(hostname=hostname,hostip=hostip,hostpwd=encodepwd,user=hostuser,status=hoststuts)
                NginxHost.objects.create(hostname=hostname,hostip=hostip,user=hostuser,status=hoststatus)
            else:
                #NginxHost.objects.create(hostname=hostname,hostip=hostip,hostpwd=encodepwd,user=hostuser,port=int(hostport),status=hoststuts)
                NginxHost.objects.create(hostname=hostname,hostip=hostip,user=hostuser,port=int(hostport),status=hoststatus)

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
        datapath=request.POST.get('datapath')
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
        Team.objects.create(groupname=teamname,language_id=languageid,teamport=teamport,datapath=datapath,url=url,path=teampath,svnpath=svnpath,svnpwd=svnpwd,nginxconf=nginxpath,nginxupstream=nginxupstream,svnuser=svnuser,ps=ps)
        team=Team.objects.get(groupname=teamname)
        for h in host:
            hostid=Host.objects.get(id=h)
            team.host.add(hostid)
        for nh in nginxhost:
            nhid=NginxHost.objects.get(id=nh)
            team.nginxhost.add(nhid)
        return redirect(reverse("teamall"))
    else:
        return render(request,'createteam.html',{"language":language,"hostall":hostall,"nginxhost":nhost})

@login_required(login_url=reverse_lazy('login'))
def reuser(request,id):
    teamall=Team.objects.all()
    user=User.objects.get(id=id)
    return render(request,'reuser.html',{"teamall":teamall,"user":user})

@login_required(login_url=reverse_lazy('login'))
def deluser(request,id):
    user = User.objects.get(id=id)
    #user.team_set.filter(userid=user).delete()
    #会把所有跟user有关的配置都删除
    user.delete()
    return redirect(reverse("userall"))


@login_required(login_url=reverse_lazy('login'))
def updateuser(request):
    teamall=Team.objects.all()
    if request.method=="POST":
        list=[]
        username=request.POST.get('loginname')
        teamid=request.POST.getlist('my_multi_select1[]')
        user=User.objects.get(username=username)
        for id in user.team_set.all():
            list.append(id)
        for newid in teamid:
            if newid not in list:
                team=Team.objects.get(id=newid)
                team.userid.add(user)
        return redirect(reverse("userall"))
    return render(request, 'reuser.html',{'teamall':teamall})


@login_required(login_url=reverse_lazy('login'))
def reteam(request,id):
    hostall=Host.objects.all()
    language=Language.objects.all()
    nhost=NginxHost.objects.all()
    team=Team.objects.get(id=id)
    return render(request, 'reteam.html', {"language":language, "hostall":hostall, "nginxhost":nhost, "team":team})


@login_required(login_url=reverse_lazy('login'))
def updateteam(request):
    hostall=Host.objects.all()
    language=Language.objects.all()
    nhost=NginxHost.objects.all()
    if request.method=='POST':
        hostlist=[]
        nginxlist=[]
        host=request.POST.getlist('host')      #获取前端传过来的主机
        teamname=request.POST.get('teamname')
        teampath=request.POST.get('teampath')
        datapath=request.POST.get('datapath')
        teamport=request.POST.get('teamport')
        svnpath=request.POST.get('svnpath')
        svnuser=request.POST.get('svnuser')
        svnpwd=request.POST.get('svnpwd')
        nginxpath=request.POST.get('nginxpath')
        nginxhost=request.POST.getlist('nginxhost') #获取前端传过来的nginx主机
        nginxupstream=request.POST.get('nginxupstream')
        url=request.POST.get('url')
        teamlanguage=request.POST.get('teamlanguage')
        ps=request.POST.get('ps')
        languageid=Language.objects.get(id=teamlanguage)
        if nginxupstream=="":
            nginxupstream=teamname
        team=Team.objects.get(groupname=teamname)
        team.teamport=teamport
        team.path=teampath
        team.nginxupstream=nginxupstream
        team.nginxconf=nginxpath
        team.url=url
        team.svnpath=svnpath
        team.svnpwd=svnpwd
        team.datapath=datapath
        team.svnuser=svnuser
        team.language_id=languageid
        team.ps=ps
        team.save()
        hall=team.host.all()             #获取现在已经存在的host
        nall=team.nginxhost.all()       #获取现在已经存在的nginx host
        for hl in hall:
            hostlist.append(hl.id)
        for nl in nall:
            nginxlist.append(nl.id)
        for dh in hostlist:
            if dh not in host:
                dhostid=Host.objects.get(id=dh)
                team.host.remove(dhostid)
        for h in host:
            if h not in hall:
                hostid=Host.objects.get(id=h)
                team.host.add(hostid)

        for dnh in nginxlist:
            if dnh not in nginxhost:
                dnhid=NginxHost.objects.get(id=dnh)
                team.nginxhost.remove(dnhid)
        for nh in nginxhost:
            if nh not in nall:
                nhid=NginxHost.objects.get(id=nh)
                team.nginxhost.add(nhid)
        return redirect(reverse("teamall"))
    else:
        return render(request,'createteam.html',{"language":language,"hostall":hostall,"nginxhost":nhost})

def issuper(request):
    if request.method=="POST":
        isuser=User.objects.get(username=request.user)
        if isuser.is_superuser:
            return HttpResponse('1')
        else:
            return HttpResponse("2")