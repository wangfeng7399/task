#!/bin/env python3
#coding:utf-8
#性能
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from pyzabbix import ZabbixAPI


def wapkaku(request):
    data={"title":["邮件营销","联盟广告","视频广告","直接访问","搜索引擎"],"xAxis":["周一","周二","周三","周四","周五","周六","周日"],
          "youjian":[120, 132, 101, 134, 90, 230, 210],"lianmeng":[220, 182, 191, 234, 290, 330, 310],"shipin":[150, 232, 201, 154, 190, 330, 410],
          "zhijie":[320, 332, 301, 334, 390, 330, 320],"sousuo":[820, 932, 901, 934, 1290, 1330, 1320]}
    return render(request,'property.html',{"data":data})
#处理过程
'''
    1.获得机器ip地址
    2.通过ip地址获得机器的zabbixid
    3.通过zabbixid来获取数据出图
'''
def proprty(request,codeid,hostid):
    data=[{"title":["邮件营销","联盟广告","视频广告","直接访问","搜索引擎"],"xAxis":["周一","周二","周三","周四","周五","周六","周日"],
          "youjian":[120, 132, 101, 134, 90, 230, 210],"lianmeng":[220, 182, 191, 234, 290, 330, 310],"shipin":[150, 232, 201, 154, 190, 330, 410],
          "zhijie":[320, 332, 301, 334, 390, 330, 320],"sousuo":[820, 932, 901, 934, 1290, 1330, 1320]}]
    return HttpResponse(data)
