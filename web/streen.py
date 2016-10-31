#!/bin/env python3
#coding:utf-8

from django.shortcuts import render,redirect,HttpResponse
import subprocess
from .base import send_mail
import re,json
from django.contrib.auth.models import User

def streen(request):
    if request.method =="POST":
        all={}
        userid=User.objects.get(username=request.user)
        addr=request.POST.get("addr")
        count=request.POST.get("count")
        sum=request.POST.get("sum")
        print(addr,count,sum)
        _,out=subprocess.getstatusoutput('siege -r{0} -c{1} "{2}" >/tmp/siege.log'.format(count,sum,addr))
        print(out)
        all["allnum"]=re.findall("Transactions:(.*)hits",out,re.S)[0].strip() #完成总次数请求
        all["cgl"]=re.findall("Availability:(.*)Elapsed time:",out,re.S)[0].strip() #成功率
        all["alltime"]=re.findall("Elapsed time:(.*)Data transferred:",out,re.S)[0].strip() #总用时
        all["data"]=re.findall("Data transferred:(.*)Response time:",out,re.S)[0].strip() #传输数据
        all["response"]=re.findall("Response time:(.*)Transaction rate:",out,re.S)[0].strip() #响应时间
        all["rate"]=re.findall("Transaction rate:(.*)Throughput:",out,re.S)[0].strip() #平均每秒完成的请求次数
        all["throughput"]=re.findall("Throughput:(.*)Concurrency:",out,re.S)[0].strip() #每秒传输的数据
        all["concurrency"]=re.findall("Concurrency:(.*)Successful transactions:",out,re.S)[0].strip() #实际最高并发连接数
        all["successful"]=re.findall("Successful transactions:(.*)Failed transactions:",out,re.S)[0].strip() #成功次数
        all["failed"]=re.findall("Failed transactions:(.*)Longest transaction:",out,re.S)[0].strip() #失败次数
        #send_mail(userid.email,"测试平台测试结果",out)
        print(all)
        data=json.dumps(all)
        return HttpResponse(data)
    return render(request,"stree.html")