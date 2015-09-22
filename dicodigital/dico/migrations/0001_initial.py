# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('creator', models.ForeignKey(verbose_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Mot',
            },
        ),
        migrations.AddField(
            model_name='definition',
            name='related',
            field=models.ManyToManyField(verbose_name='mots relatifs', related_name='related_words', to='dico.Word'),
        ),
        migrations.AddField(
            model_name='definition',
            name='word',
            field=models.ForeignKey(verbose_name='mot', to='dico.Word'),
        ),
    ]
