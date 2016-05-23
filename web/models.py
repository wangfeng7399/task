#!/bin/env python3
#coding:utf-8
from django.db import models
from django.contrib.auth.models import User,Group



class Language(models.Model):
     language=models.CharField(max_length=200)
class Team(models.Model):
    groupname=models.CharField(max_length=200)
    userid=models.ManyToManyField(User)
class Host(models.Model):
    hostip=models.GenericIPAddressField()
    hostpwd=models.CharField(max_length=200,null=True,blank=True)
    path=models.CharField(max_length=200)
    svnpath=models.CharField(max_length=200,null=True,blank=True)
    svnuser=models.CharField(max_length=200,null=True,blank=True)
    svnpwd=models.CharField(max_length=200,null=True,blank=True)
    nginxconf=models.CharField(max_length=200,null=True,blank=True)
    nginxupsteam=models.CharField(max_length=200,null=True,blank=True)
    nginxsbin=models.CharField(max_length=200,null=True,blank=True)
    teamid=models.ManyToManyField(Team)
    ps=models.CharField(max_length=200,null=True,blank=True)
    language_id=models.ForeignKey(Language)
    def __str__(self):
        return self.hostip,self.path
class Code(models.Model):
    create_data=models.DateTimeField(auto_now=True)
    team=models.ForeignKey(Team)


