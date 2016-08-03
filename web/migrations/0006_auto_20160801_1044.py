# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-01 02:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20160729_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitor',
            name='servertype',
        ),
        migrations.RemoveField(
            model_name='monitor',
            name='type',
        ),
        migrations.AddField(
            model_name='monitor',
            name='type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='web.Type'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ServerType',
        ),
    ]
