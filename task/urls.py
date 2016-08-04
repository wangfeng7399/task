#!/bin/env python3
#coding:utf-8

"""task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from web import views
from web import user,code,property
app_name="web"
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.Login,name='login'),
    #url(r'^web/',include("web.urls")),
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
    url(r'^release/$',code.release,name='release'),
    url(r'^rust/$',views.rust,name='rust'),
    url(r'^status/$',code.status,name='status'),
    url(r'^updateall/$',code.updateall,name='updateall'),
    url(r'^backall/$',code.backall,name='backall'),
    url(r'^tree/(?P<id>[0-9]+)$',code.tree,name='tree'),
    url(r'^retype/$',code.retype,name='retype'),
    url(r'^svncode/$',code.svncode,name='svncode'),
    url(r'^upyun/$',code.upyun,name='upyun'),
    url(r'^download/$',code.downloadxls,name='downloadxls'),
    url(r'^issuper/$',user.issuper,name='issuper'),
    url(r'^reuser/(?P<id>[0-9]+)$',user.reuser,name='reuser'),
    url(r'^del/(?P<id>[0-9]+)$',code.delfile,name='delfile'),
    url(r'^reteam/(?P<id>[0-9]+)$',user.reteam,name='reteam'),
    url(r'^goback/(?P<id>[0-9]+)$',code.goback,name='goback'),
    url(r'^detail/(?P<id>[0-9]+)$',code.detail,name='detail'),
    url(r'^logs/(?P<id>[0-9]+)/(?P<hostid>[0-9]+)$',code.log,name='log'),
    url(r'^updateuser/$',user.updateuser,name='updateuser'),
    url(r'^updateteam/$',user.updateteam,name='updateteam'),
    url(r'^wapkahu/$',property.wapkaku,name='wapkahu'),
    url(r'^zabbix/(?P<codeid>[0-9]+)/(?P<hostid>[0-9]+)$',property.proprty,name='zabbix')
]
