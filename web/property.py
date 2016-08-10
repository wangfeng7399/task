#!/bin/env python3
#coding:utf-8
#性能
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from pyzabbix import ZabbixAPI
from .models import Host,Team,Code,Type,Monitor
import time

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
        for history in z.history.get(output="extend",history=0,itemids=cpu.num,limit=10,):
            list.append(history["value"])
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        cpudict["xAxis"]=xAxis
        cpudict[cpu.name]=list
    cpudict["title"]=cputitle
    all["cpu"]=cpudict
        #data["cpu"]["itemid"]=list
    #print(data)
    diskdict={}
    for disk in diskall:
        list=[]
        xAxis=[]
        disktitle.append(disk.name)
        for history in z.history.get(output="extend",history=3,itemids=disk.num,limit=1,):
            list.append(history["value"])
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        diskdict[disk.name]=list
        diskdict["xAxis"]=xAxis
    diskdict["title"]=disktitle
    all["disk"]=diskdict
    networkdict={}
    for network in networkall:
        list=[]
        xAxis=[]
        networktitle.append(network.name)
        for history in z.history.get(output="extend",history=3,itemids=network.num,limit=10,):
            list.append(history["value"])
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        networkdict["xAxis"]=xAxis
        networkdict[network.name]=list
    networkdict["title"]=networktitle
    all["network"]=networkdict
    nginxdict={}
    for nginx in nginxall:
        list=[]
        xAxis=[]
        nginxtitle.append(nginx.name)
        for history in z.history.get(output="extend",history=3,itemids=nginx.num,limit=10,):
            list.append(history["value"])
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        nginxdict["xAxis"]=xAxis
        nginxdict[nginx.name]=list
    nginxdict["title"]=nginxtitle
    all["nginx"]=nginxdict
    dbdict={}
    for db in dball:
        list=[]
        xAxis=[]
        dbtitle.append(db.name)
        for history in z.history.get(output="extend",history=3,itemids=db.num,limit=10,):
            list.append(history["value"])
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        dbdict["xAxis"]=xAxis

        dbdict[db.name]=list
    dbdict["title"]=dbtitle
    all["db"]=dbdict
    processdict={}
    for process in processall:
        list=[]
        xAxis=[]
        processtitle.append(process.name)
        for history in z.history.get(output="extend",history=3,itemids=process.num,limit=10,):
            list.append(history["value"])
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        processdict["xAxis"]=xAxis

        processdict[process.name]=list
    processdict["title"]=processtitle
    all["process"]=processdict
    memdict={}
    for mem in memall:
        list=[]
        xAxis=[]
        memtitle.append(mem.name)
        for history in z.history.get(output="extend",history=3,itemids=mem.num,limit=10,):
            list.append(history["value"])
            xAxis.append(time.strftime("%m-%d %H:%M",time.localtime(int(history["clock"]))))
        memdict["xAxis"]=xAxis
        memdict[mem.name]=list
    memdict["title"]=memtitle
    all["mem"]=memdict
    data.append(all)
    # print(time.strftime("%m-%d %H:%M:%S",time.localtime(1470034355)))
    # #获取前15次数值
    # for a in z.history.get(output="extend",history=0,itemids="23944",limit=15):
    #     print(a)
    return HttpResponse(data)
