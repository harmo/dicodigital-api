from django.db import models
from django.conf import settings


class Word(models.Model):
    label = models.CharField(max_length=128)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = 'Mot'


class Definition(models.Model):
    word = models.ForeignKey(Word, verbose_name='mot')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='creator')
    description = models.TextField(max_length=500)
    related = models.ManyToManyField(Word, related_name='related_words', verbose_name='mots relatifs')
