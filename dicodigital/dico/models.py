from django.db import models
from django.conf import settings
from autoslug import AutoSlugField


class Word(models.Model):
    label = models.CharField(max_length=128)
    slug = AutoSlugField(populate_from='label')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label


class Definition(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    word = models.ForeignKey(Word, related_name='definitions')
    is_primary = models.BooleanField(default=False)
