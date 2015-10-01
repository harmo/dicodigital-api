from django.db import models
from django.conf import settings


class Word(models.Model):
    label = models.CharField(max_length=128)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label


class Definition(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    word = models.ForeignKey(Word)
    is_primary = models.BooleanField(default=False)
