# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wikiwho', '0002_fkeys'),
    ]

    operations = [
        # https://docs.djangoproject.com/en/1.10/ref/migration-operations/#django.db.migrations.operations.RunSQL
        migrations.RunSQL(
            sql='ALTER TABLE public.wikiwho_token DROP CONSTRAINT wikiwho_token_pkey;',
            reverse_sql='ALTER TABLE public.wikiwho_token ADD CONSTRAINT wikiwho_token_pkey PRIMARY KEY(id);'
        ),

        migrations.RunSQL(
            sql='ALTER TABLE public.wikiwho_sentence DROP CONSTRAINT wikiwho_sentence_pkey;',
            reverse_sql='ALTER TABLE public.wikiwho_sentence ADD CONSTRAINT wikiwho_sentence_pkey PRIMARY KEY(id);'
        ),

        migrations.RunSQL(
            sql='ALTER TABLE public.wikiwho_paragraph DROP CONSTRAINT wikiwho_paragraph_pkey;',
            reverse_sql='ALTER TABLE public.wikiwho_paragraph ADD CONSTRAINT wikiwho_paragraph_pkey PRIMARY KEY(id);'
        ),

        migrations.RunSQL(
            sql='ALTER TABLE public.wikiwho_revision DROP CONSTRAINT wikiwho_revision_pkey;',
            reverse_sql='ALTER TABLE public.wikiwho_revision ADD CONSTRAINT wikiwho_revision_pkey PRIMARY KEY(id);'
        ),

        migrations.RunSQL(
            sql='ALTER TABLE public.wikiwho_article DROP CONSTRAINT wikiwho_article_pkey;',
            reverse_sql='ALTER TABLE public.wikiwho_article ADD CONSTRAINT wikiwho_article_pkey PRIMARY KEY(id);'
        ),

        migrations.RunSQL(
            sql='ALTER TABLE public.wikiwho_revisionparagraph DROP CONSTRAINT wikiwho_revisionparagraph_pkey;',
            reverse_sql='ALTER TABLE public.wikiwho_revisionparagraph ADD CONSTRAINT wikiwho_revisionparagraph_pkey PRIMARY KEY(id);'
        ),

        migrations.RunSQL(
            sql='ALTER TABLE public.wikiwho_paragraphsentence DROP CONSTRAINT wikiwho_paragraphsentence_pkey;',
            reverse_sql='ALTER TABLE public.wikiwho_paragraphsentence ADD CONSTRAINT wikiwho_paragraphsentence_pkey PRIMARY KEY(id);'
        ),

        migrations.RunSQL(
            sql='ALTER TABLE public.wikiwho_sentencetoken DROP CONSTRAINT wikiwho_sentencetoken_pkey;',
            reverse_sql='ALTER TABLE public.wikiwho_sentencetoken ADD CONSTRAINT wikiwho_sentencetoken_pkey PRIMARY KEY(id);'
        )
    ]