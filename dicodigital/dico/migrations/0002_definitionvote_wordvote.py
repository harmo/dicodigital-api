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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(null=True)),
                ('cookie', models.CharField(blank=True, max_length=64, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField()),
                ('definition', models.ForeignKey(to='dico.Definition', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WordVote',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(null=True)),
                ('cookie', models.CharField(blank=True, max_length=64, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
                ('word', models.ForeignKey(to='dico.Word', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
