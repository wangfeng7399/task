#!/bin/env python3
#coding:utf-8
#代码操作
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User
from .models import Team,Host
from .base import encode,decode
import paramiko

@login_required(login_url=reverse_lazy('login'))
def code(request):
    teamall=Team.objects.all()
    if request.method =="POST":
        filename=request.FILES.get('file')
        path='{0}/{1}'.format('/root/',filename.name)
        with open(path,'wb+') as f:
            for chunk in filename.chunks():
                f.write(chunk)
        #cp文件，重启服务，返回结果
        return HttpResponse("上传完成")
    return render(request,'updatefile.html',{"teamall":teamall})

@login_required(login_url=reverse_lazy('login'))
def status(request):
    return render(request, 'status.html')


def updateall(request):
    return render(request,'updateall.html')