# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20160525_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='nginxhost',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]