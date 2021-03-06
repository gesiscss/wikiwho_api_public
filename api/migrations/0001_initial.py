# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 11:47
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LongFailedArticle',
            fields=[
                ('id', models.IntegerField(editable=False, help_text='Wikipedia page id', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('count', models.PositiveIntegerField(default=0)),
                ('revisions', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RecursionErrorArticle',
            fields=[
                ('id', models.IntegerField(editable=False, help_text='Wikipedia page id', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('count', models.PositiveIntegerField(default=0)),
                ('revisions', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
