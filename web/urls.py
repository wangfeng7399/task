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
    url(r'^createhost/$',user.createhost,name='createhost'),
    url(r'^createstatus/$',user.createstatus,name='createstatus'),
    url(r'^agentstatus/$',user.agentstatus,name='agentstatus'),
     url(r'^createteam/$',user.createteam,name='createteam'),
    url(r'^teamall/$',user.teamall,name='teamall'),
    url(r'^userall/$',user.userall,name='userall'),
    url(r'^agentteam/$',user.agentteam,name='agentteam'),
    url(r'^createlanguage/$',user.createlanguage,name='createlanguage'),
    url(r'^agentlanguage/$',user.agentlanguage,name='agentlanguage'),
    url(r'^code/$',code.code,name='code'),
    url(r'^rust/$',views.rust,name='rust'),
    url(r'^status/$',code.status,name='status'),
    url(r'^updateall/$',code.updateall,name='updateall'),
    url(r'^backall/$',code.backall,name='backall'),
    url(r'^tree/$',code.tree,name='tree'),
]