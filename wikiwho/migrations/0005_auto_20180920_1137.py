# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-20 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wikiwho', '0004_auto_20180105_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='editordatade',
            name='adds_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordatade',
            name='dels_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordatade',
            name='reins_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordatadenotindexed',
            name='adds_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordatadenotindexed',
            name='dels_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordatadenotindexed',
            name='reins_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataen',
            name='adds_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataen',
            name='dels_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataen',
            name='reins_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataennotindexed',
            name='adds_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataennotindexed',
            name='dels_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataennotindexed',
            name='reins_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataes',
            name='adds_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataes',
            name='dels_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataes',
            name='reins_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataesnotindexed',
            name='adds_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataesnotindexed',
            name='dels_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataesnotindexed',
            name='reins_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataeu',
            name='adds_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataeu',
            name='dels_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataeu',
            name='reins_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataeunotindexed',
            name='adds_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataeunotindexed',
            name='dels_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordataeunotindexed',
            name='reins_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordatatr',
            name='adds_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordatatr',
            name='dels_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordatatr',
            name='reins_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordatatrnotindexed',
            name='adds_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordatatrnotindexed',
            name='dels_stopword_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editordatatrnotindexed',
            name='reins_stopword_count',
            field=models.IntegerField(default=0),
        ),
    ]
