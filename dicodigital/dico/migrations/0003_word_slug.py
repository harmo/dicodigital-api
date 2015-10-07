# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from autoslug.settings import slugify


def auto_fill_slug(apps, schema_editor):
    Word = apps.get_model('dico', 'Word')
    for word in Word.objects.all():
        word.slug = slugify(word.label)
        word.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dico', '0002_auto_20151001_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='nr', populate_from='label', editable=False),
            preserve_default=False,
        ),
        migrations.RunPython(auto_fill_slug),
    ]
