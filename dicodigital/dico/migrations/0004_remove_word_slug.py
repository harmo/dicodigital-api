# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dico', '0003_word_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='slug',
        ),
    ]
