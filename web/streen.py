#!/bin/env python3
#coding:utf-8

from django.shortcuts import render,redirect,HttpResponse
import subprocess
from .base import send_mail
from django.contrib.auth.models import User

def streen(request):
    if request.method =="POST":
        userid=User.objects.get(username=request.user)
        addr=request.POST.get("addr")
        count=request.POST.get("count")
        sum=request.POST.get("sum")
        print(addr,count,sum)
        _,out=subprocess.getstatusoutput('siege -r{0} -c{1} "{2}" >/tmp/siege.log'.format(count,sum,addr))
        print(out)
        #send_mail(userid.email,"测试平台测试结果",out)
        return HttpResponse("ok")
    return render(request,"stree.html")