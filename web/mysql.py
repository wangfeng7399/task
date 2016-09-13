#!/bin/env python3
#coding:utf-8


from django.shortcuts import render,redirect,HttpResponse

from django.contrib.auth.decorators import login_required
from .models import Slow

def slow(request):
    sql=Slow.objects.all()
    return render(request,'sqlall.html',{"sqlall":sql})