# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-06-16 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_framework_tracking', '0013_auto_20181115_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='apirequestlog',
            name='remote_addr',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AlterField(
            model_name='apirequestlog',
            name='instance_id',
            field=models.IntegerField(blank=True, db_index=True, help_text='id of the most relevant instance', null=True),
        ),
    ]
