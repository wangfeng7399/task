# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-02 06:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20160801_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='name',
            field=models.CharField(default='', max_length=2000),
            preserve_default=False,
        ),
    ]
