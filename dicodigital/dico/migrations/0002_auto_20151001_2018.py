# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dico', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='word',
            field=models.ForeignKey(to='dico.Word', related_name='definitions'),
        ),
    ]
