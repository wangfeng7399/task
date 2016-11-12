#!/usr/bin/env python3
#coding:utf-8


from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Slow

@login_required(login_url=reverse_lazy('login'))
def slow(request):
    sql=Slow.objects.all()
    return render(request,'sqlall.html',{"sqlall":sql})

@login_required(login_url=reverse_lazy('login'))
def sqlselect(request):
    if request.method == "POST":
        starttime=request.POST.get("starttime")
        endtime=request.POST.get("endtime")
        print(starttime,endtime)
        sql=Slow.objects.all()
        selectsql=sql.exclude(date__lt=starttime)
        sqls=selectsql.exclude(date__gt=endtime)
        return render(request,'sqlall.html',{"sqlall":sqls})
