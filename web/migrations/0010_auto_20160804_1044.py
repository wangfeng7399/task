# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-04 02:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_remove_monitor_zabbixid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='hostpwd',
        ),
        migrations.RemoveField(
            model_name='nginxhost',
            name='hostpwd',
        ),
    ]
