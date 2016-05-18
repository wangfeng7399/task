#!/bin/env python3
#coding:utf-8

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
# Create your views here.
def Login(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        print(username,password)
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            request.session["name"]=1
            return redirect(reverse('index'))
        else:
            return render(request, 'login.html',{'ret_msg':'帐号或密码错误'})
    else:
        return render(request, 'login.html')
@login_required(login_url=reverse_lazy('login'))
def index(request):
    print(request.user)
    return render(request, 'master/index.html')

def Logout(request):
    logout(request)
    return redirect(reverse('login'))

@login_required(login_url=reverse_lazy('login'))
def error(request):
    return render(request,'500.html')