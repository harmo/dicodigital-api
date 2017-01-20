from django.conf import settings
from django.db import models
from django.db.models import Sum


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
    word = models.ForeignKey(Word, related_name='definitions')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return '{word} : {s.text}'.format(word=self.word.label.upper(), s=self)

    @property
    def score(self):
        total = self.votes.all().aggregate(Sum('score'))
        return total['score__sum']


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    cookie = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
    definition = models.ForeignKey(
        Definition, related_name='votes', on_delete=models.CASCADE
    )
