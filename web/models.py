#!/bin/env python3
#coding:utf-8
from django.db import models

# Create your models here.
class Host(models.Model):
    hostip=models.GenericIPAddressField()
    hostpwd=models.CharField(max_length=200)
    path=models.CharField(max_length=200)
    svnpath=models.CharField(max_length=200)
    svnpwd=models.CharField(max_length=200)
    svntmppath=models.CharField(max_length=200)
    def __str__(self):
        return self.hostip,self.path
