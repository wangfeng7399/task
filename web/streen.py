#!/bin/env python3
#coding:utf-8

from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User


def streen(request):
    if request.method =="POST":
        addr=request.POST.get("addr")
        count=request.POST.get("count")
        sum=request.POST.get("sum")
        print(addr,count,sum)
        return render(request,"stree.html")
    return render(request,"stree.html")