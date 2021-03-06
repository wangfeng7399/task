# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-29 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_remove_code_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=200)),
                ('num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ServerType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='monitor',
            name='servertype',
            field=models.ManyToManyField(to='web.ServerType'),
        ),
        migrations.AddField(
            model_name='monitor',
            name='type',
            field=models.ManyToManyField(to='web.Type'),
        ),
    ]
