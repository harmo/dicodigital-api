# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dico', '0001_squashed_0004_remove_word_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefinitionVote',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('score', models.SmallIntegerField(default=0)),
                ('definition', models.ForeignKey(to='dico.Definition')),
                ('elector', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WordVote',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('score', models.SmallIntegerField(default=0)),
                ('elector', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(to='dico.Word')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
