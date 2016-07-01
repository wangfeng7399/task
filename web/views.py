#!/bin/env python3
#coding:utf-8

from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User
from .models import Code
# Create your views here.
def Login(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
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
    user=User.objects.get(username=request.user)
    if user.is_superuser:
        updateall=Code.objects.all()
    else:
        updateall=Code.objects.filter(user=user)
    return render(request,'updateall.html',{'updateall':updateall})

def Logout(request):
    logout(request)
    return redirect(reverse('login'))

@login_required(login_url=reverse_lazy('login'))
def error(request):
    return render(request,'404.html')

@login_required(login_url=reverse_lazy('login'))
def rust(request):
    user=User.objects.get(username=request.user)
    if user.is_superuser:
        return HttpResponse(1)
    else:
        return HttpResponse(0)