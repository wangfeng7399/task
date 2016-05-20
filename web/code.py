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
def code(request):
    if request.method =="POST":
        filename=request.FILES.get('file')
        path='{0}/{1}'.format('/root/',filename.name)
        with open(path,'wb+') as f:
            for chunk in filename.chunks():
                f.write(chunk)
        return HttpResponse("上传完成")
    return render(request,'form_dropzone.html')