import django_filters
from . import models


class Word(django_filters.FilterSet):

    class Meta:
        model = models.Word
        fields = ['label']
