#!/usr/bin/env python3
#coding:utf-8


from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Slow
import datetime




@login_required(login_url=reverse_lazy('login'))
def slow(request):
    d=datetime.date.today()
    onday=datetime.timedelta(days=1)
    yesterday=d-onday
    sql=Slow.objects.filter(date=yesterday)
    return render(request,'sqlall.html',{"sqlall":sql})

@login_required(login_url=reverse_lazy('login'))
def sqlselect(request):
    if request.method == "POST":
        starttime=request.POST.get("starttime")
        endtime=request.POST.get("endtime")
        if starttime =="":
            starttime="2010-01-01"
        d = datetime.date.today()
        onday = datetime.timedelta(days=1)
        yesterday = d - onday
        if endtime =="":
            endtime=yesterday
        sql=Slow.objects.all()
        selectsql=sql.exclude(date__lt=starttime)
        sqls=selectsql.exclude(date__gt=endtime)
        return render(request,'sqlall.html',{"sqlall":sqls})
