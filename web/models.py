#!/bin/env python3
#coding:utf-8
from django.db import models
from django.contrib.auth.models import User,Group

class Status(models.Model):
    status=models.CharField(max_length=20)
    def __str__(self):
        return self.status

class Language(models.Model):
     language=models.CharField(max_length=200)
     def __str__(self):
         return self.language
class HostStatus(models.Model):
    status=models.CharField(max_length=50)

class Host(models.Model):
    hostname=models.CharField(max_length=200)
    hostip=models.GenericIPAddressField()
    hostpwd=models.CharField(max_length=200,null=True,blank=True)
    user=models.CharField(max_length=200,default='root')
    port=models.IntegerField(default=22)
    status=models.ForeignKey(HostStatus)
    def __str__(self):
        return self.hostip

class NginxHost(models.Model):
    hostname=models.CharField(max_length=200)
    hostip=models.GenericIPAddressField()
    hostpwd=models.CharField(max_length=200,null=True,blank=True)
    user=models.CharField(max_length=200,default='root')
    port=models.IntegerField(default=22)
    status=models.ForeignKey(HostStatus)
    def __str__(self):
        return self.hostip

class Team(models.Model):
    groupname=models.CharField(max_length=200)
    userid=models.ManyToManyField(User)
    path=models.CharField(max_length=200)
    teamport=models.CharField(max_length=200)
    svnpath=models.CharField(max_length=200,null=True,blank=True)
    svnuser=models.CharField(max_length=200,null=True,blank=True)
    svnpwd=models.CharField(max_length=200,null=True,blank=True)
    nginxconf=models.CharField(max_length=200,null=True,blank=True)
    nginxupstream=models.CharField(max_length=200,null=True,blank=True)
    nginxhost=models.ManyToManyField(NginxHost)
    url=models.CharField(max_length=200,null=True,blank=True)
    ps=models.CharField(max_length=200,null=True,blank=True)
    language_id=models.ForeignKey(Language)
    host=models.ManyToManyField(Host)
    datapath=models.CharField(max_length=200)
    def __str__(self):
        return self.groupname

class Code(models.Model):
    date=models.CharField(max_length=2000)
    create_date=models.DateTimeField(auto_now_add=True)
    team=models.ForeignKey(Team)
    path=models.CharField(max_length=2000)
    user=models.ForeignKey(User)
    status=models.ForeignKey(Status)
    update_date=models.DateTimeField(auto_now=True)
    dir=models.CharField(max_length=100)
    #url=models.CharField(max_length=2000)

class Relat(models.Model):
    code=models.ForeignKey(Code)
    host=models.ForeignKey(Host)
    status=models.ForeignKey(Status)
    update_date=models.DateTimeField(auto_now=True)

# 1代表cpu 2代表 disk 3 代表 network 4 代表nginx 5 代表db 6代表进程数 7代表mem
class Type(models.Model):
    name=models.CharField(max_length=200)

class Monitor(models.Model):
    ip=models.CharField(max_length=200)
    type=models.ForeignKey(Type)
    num=models.IntegerField()
    name=models.CharField(max_length=2000)
    #zabbixid=models.CharField(max_length=200)