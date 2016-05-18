#!/bin/env python3
#coding:utf-8
#用户管理操作
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
def createuser(request):
    return render(request,'user.html')

def agentpasswd(request):
    return render(request,'agentpasswd.html')