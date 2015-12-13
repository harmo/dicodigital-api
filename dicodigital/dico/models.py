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
    word = models.ForeignKey(Word, related_name='definitions')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return '{word} : {s.text}'.format(word=self.word.label.upper(), s=self)


class Vote(models.Model):
    elector = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.SmallIntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return '{s.elector} voted {s.score} on the {s.created_at}'.format(s=self)


class WordVote(Vote):
    word = models.ForeignKey(Word)


class DefinitionVote(Vote):
    definition = models.ForeignKey(Definition)
