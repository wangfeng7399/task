# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-12 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0015_auto_20160912_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slow',
            name='date',
            field=models.DateField(),
        ),
    ]
