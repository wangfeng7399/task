# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 07:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0020_auto_20160601_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='host',
        ),
    ]