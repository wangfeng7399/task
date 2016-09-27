#!/bin/env python3
#coding:utf-8


from django.shortcuts import render,redirect,HttpResponse

from django.contrib.auth.decorators import login_required
from .models import Slow
import time,datetime


def slow(request):
    sql=Slow.objects.all()
    return render(request,'sqlall.html',{"sqlall":sql})
def sqlselect(request):
    if request.method == "POST":
        starttime=request.POST.get("starttime")
        endtime=request.POST.get("endtime")
        print(starttime,endtime)
        sql=Slow.objects.all()
        selectsql=sql.exclude(date__lte=starttime)
        sqls=selectsql.exclude(date__gte=endtime)
        print(sqls)
        return render(request,'sqlall.html',{"sqlall":sqls})