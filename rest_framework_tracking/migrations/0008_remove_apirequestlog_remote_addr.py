# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-12 07:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_framework_tracking', '0007_apirequestlog_remote_addr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apirequestlog',
            name='remote_addr',
        ),
    ]
