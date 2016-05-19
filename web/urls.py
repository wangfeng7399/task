#!/bin/env python3
#coding:utf-8

from django.conf.urls import url
from web import views
appname="web"
from . import code
from . import db
from . import user
urlpatterns = [
    url(r'^index',views.index,name="index"),
    url(r'^logout/$',views.Logout,name='logout'),
    url(r'^error/$',views.error,name='error'),
    url(r'^createuser/$',user.createuser,name='createuser'),
    url(r'^agentpasswd/$',user.agentpasswd,name='agentpasswd'),
    url(r'^creategroup/$',user.creategroup,name='creategroup'),
    url(r'^createhost/$',user.createhost,name='createhost'),
    url(r'^teamall/$',user.teamall,name='teamall'),
    url(r'^groupall/$',user.groupall,name='groupall'),
]