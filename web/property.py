#!/usr/bin/env python3
#coding:utf-8
#性能
from django.shortcuts import HttpResponse,render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from pyzabbix import ZabbixAPI
from .models import Host,Team,Code,Type,Monitor
import time
import json
# def wapkaku(request):
#     data={"title":["邮件营销","联盟广告","视频广告","直接访问","搜索引擎"],"xAxis":["周一","周二","周三","周四","周五","周六","周日"],
#           "youjian":[120, 132, 101, 134, 90, 230, 210],"lianmeng":[220, 182, 191, 234, 290, 330, 310],"shipin":[150, 232, 201, 154, 190, 330, 410],
#           "zhijie":[320, 332, 301, 334, 390, 330, 320],"sousuo":[820, 932, 901, 934, 1290, 1330, 1320]}
#     return render(request,'property.html',{"data":data})
# 处理过程
'''
    1.获得机器ip地址
    2.通过ip地址获得机器的zabbixid
    3.通过zabbixid来获取数据出图
'''
@login_required(login_url=reverse_lazy('login'))
def proprty(request,codeid,hostid):
    z=ZabbixAPI("http://10.10.0.50/zabbix")
    z.login('wangsh','wodehao123')
    # #data=[{"title":["邮件营销","联盟广告","视频广告","直接访问","搜索引擎"],"xAxis":["周一","周二","周三","周四","周五","周六","周日"],
    #       "youjian":[120, 132, 101, 134, 90, 230, 210],"lianmeng":[220, 182, 191, 234, 290, 330, 310],"shipin":[150, 232, 201, 154, 190, 330, 410],
    #       "zhijie":[320, 332, 301, 334, 390, 330, 320],"sousuo":[820, 932, 901, 934, 1290, 1330, 1320]}]
    #codeid
    #hostid机器id
    code=Code.objects.get(id=codeid)
    team=Team.objects.get(id=code.team_id)
    # for nginx in team.nginxhost.all():
    #     print(nginx.hostip)
    host=Host.objects.get(id=hostid)
    cputype=Type.objects.get(name="cpu")
    disktype=Type.objects.get(name="disk")
    networktype=Type.objects.get(name="network")
    nginxtype=Type.objects.get(name="nginx")
    dbtype=Type.objects.get(name="db")
    processtype=Type.objects.get(name="进程数")
    memtype=Type.objects.get(name="mem")
    data=[]
    cpuall=Monitor.objects.filter(type=cputype,ip=host.hostip)
    diskall=Monitor.objects.filter(type=disktype,ip=host.hostip)
    networkall=Monitor.objects.filter(type=networktype,ip=host.hostip)
    nginxall=Monitor.objects.filter(type=nginxtype,ip=host.hostip)
    dball=Monitor.objects.filter(type=dbtype,ip=host.hostip)
    processall=Monitor.objects.filter(type=processtype,ip=host.hostip)
    memall=Monitor.objects.filter(type=memtype,ip=host.hostip)
    all={}
    cpudict={}
    cputitle=[]
    disktitle=[]
    networktitle=[]
    nginxtitle=[]
    dbtitle=[]
    processtitle=[]
    memtitle=[]
    for cpu in cpuall:
        list=[]
        xAxis=[]
        cputitle.append(cpu.name)
        for history in z.history.get(output="extend",history=0,itemids=cpu.num,sortfield="clock",sortorder="DESC",limit=10,):
            list.append(history["value"])
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        cpudict["xAxis"]=xAxis
        if cpu.name=="1分钟的load值":
            cpudict["cpuone"]=list
        elif cpu.name=="5分钟的load值":
            cpudict["cpufive"]=list
        elif cpu.name=="15分钟的load值":
            cpudict["cpufivten"]=list
    cpudict["title"]=cputitle
    all["cpu"]=cpudict
        #data["cpu"]["itemid"]=list
    #print(data)
    diskdict={}
    userlist=[]
    for disk in diskall:
        list=[]
        xAxis=[]
        disktitle.append(disk.name)
        for history in z.history.get(output="extend",history=3,itemids=disk.num,sortfield="clock",sortorder="DESC",limit=1,):
            if disk.name=="根的已用总容量":
                diskdict["userdisk"]=int(history["value"])/1024/1024//1024
            elif disk.name=="根的总容量":
                diskdict["disk"]=int(history["value"])/1024/1024//1024
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        diskdict["xAxis"]=xAxis
    diskdict["freedisk"]=diskdict["disk"]-diskdict["userdisk"]
    diskdict["title"]=disktitle
    diskdict["data"]=[{"name":"根的已用总容量","value":diskdict["userdisk"]},{"name":"根的剩余容量","value":diskdict["freedisk"]}]
    all["disk"]=diskdict
    networkdict={}
    for network in networkall:
        list=[]
        xAxis=[]
        networktitle.append(network.name)
        for history in z.history.get(output="extend",history=3,itemids=network.num,sortfield="clock",sortorder="DESC",limit=10,):
            list.append(int(history["value"])//1024)
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        networkdict["xAxis"]=xAxis
        if network.name=="em1 进入的流量":
            networkdict["networkin"]=list
        if network.name=="em1 流出的流量":
            networkdict["networkout"]=list
    networkdict["title"]=networktitle
    all["network"]=networkdict
    # nginxdict={}
    # for nginx in nginxall:
    #     list=[]
    #     xAxis=[]
    #     nginxtitle.append(nginx.name)
    #     for history in z.history.get(output="extend",history=3,itemids=nginx.num,sortfield="clock",sortorder="DESC",limit=10,):
    #         list.append(history["value"])
    #         xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
    #     nginxdict["xAxis"]=xAxis
    #     nginxdict[nginx.name]=list
    # nginxdict["title"]=nginxtitle
    # all["nginx"]=nginxdict
    # dbdict={}
    # for db in dball:
    #     list=[]
    #     xAxis=[]
    #     dbtitle.append(db.name)
    #     for history in z.history.get(output="extend",history=3,itemids=db.num,sortfield="clock",sortorder="DESC",limit=10,):
    #         list.append(history["value"])
    #         xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
    #     dbdict["xAxis"]=xAxis
    #     dbdict[db.name]=list
    # dbdict["title"]=dbtitle
    # all["db"]=dbdict
    processdict={}
    for process in processall:
        list=[]
        xAxis=[]
        processtitle.append(process.name)
        for history in z.history.get(output="extend",history=3,itemids=process.num,sortfield="clock",sortorder="DESC",limit=10,):
            list.append(history["value"])
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        processdict["xAxis"]=xAxis
        if process.name=="最大进程数":
            processdict["max"]=list
        elif process.name=="正在运行的进程数":
            processdict["new"]=list
        elif process.name=="当前进程数":
            processdict["all"]=list
    processdict["title"]=processtitle
    all["process"]=processdict
    memdict={}
    for mem in memall:
        list=[]
        xAxis=[]
        memtitle.append(mem.name)
        for history in z.history.get(output="extend",history=3,itemids=mem.num,sortfield="clock",sortorder="DESC",limit=10,):
            list.append(int(history["value"])/1024/1024//1024)
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        memdict["xAxis"]=xAxis
        if mem.name=="可用内存":
            memdict["freemem"]=list
    memdict["title"]=memtitle
    all["member"]=memdict
    # data.append(all)
    # print(data)
    # print(time.strftime("%m-%d %H:%M:%S",time.localtime(1470034355)))
    # #获取前15次数值
    # for a in z.history.get(output="extend",history=0,itemids="23944",limit=15):
    #     print(a)
    all=json.dumps(all)
    return HttpResponse(all)
