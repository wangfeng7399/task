# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 05:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0026_auto_20160602_1349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='datepath',
            new_name='datapath',
        ),
        migrations.AlterField(
            model_name='relat',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Code'),
        ),
    ]