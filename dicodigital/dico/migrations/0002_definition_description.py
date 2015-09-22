# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dico', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='definition',
            name='description',
            field=models.TextField(default=datetime.datetime(2015, 9, 22, 20, 4, 57, 509208, tzinfo=utc), max_length=500),
            preserve_default=False,
        ),
    ]
