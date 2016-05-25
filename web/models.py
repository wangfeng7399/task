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

class Host(models.Model):
    hostip=models.GenericIPAddressField()
    hostpwd=models.CharField(max_length=200,null=True,blank=True)
    user=models.CharField(max_length=200,default='root')
    port=models.IntegerField(default=22)
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
    teamid=models.ForeignKey(TeamGroup)
    url=models.CharField(max_length=200,null=True,blank=True)
    ps=models.CharField(max_length=200,null=True,blank=True)
    language_id=models.ForeignKey(Language)
    status=models.ManyToManyField(Status)
    host=models.ManyToManyField(Host)
    def __str__(self):
        return self.groupname

class Code(models.Model):
    create_data=models.DateTimeField(auto_now=True)
    team=models.ForeignKey(Team)

