#!/bin/env python3
#coding:utf-8
#性能
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required


def wapkaku(request):
    return render(request,'property.html')

def a(request):
    #data=[{"name":"衬衫","num":10},{"name":"羊毛衫","num":24},{"name":"学房山","num":15},{"name":"裤子","num":34},{"name":"高跟鞋","num":11},{"name":"袜子","num":12}]
    data=[{"categories":["1","2","3","4","5","6","7"],"data":[{"name":"邮件营销","type":"line","stack":'总量',"areaStyle":{"normal":{}},"data":[1,2,3,4,5,6,7]},
                                                          {"name":'联盟广告',"type":"line","stack": '总量',"areaStyle":{"normal":{}},"data":[12,23,32,42,51,62,71]},
                                                          {"name":'视频广告',"type":"line","stack": '总量',"areaStyle":{"normal":{}},"data":[12,23,32,42,51,62,71]},
                                                          {"name":'直接访问',"type":"line","stack": '总量',"areaStyle":{"normal":{}},"data":[12,23,32,42,51,62,71]},
                                                          {"name":'搜索引擎',"type":"line","stack": '总量',"areaStyle":{"normal":{}},"data":[11,22,31,3,43,62,7]},]}]
    return HttpResponse(data)