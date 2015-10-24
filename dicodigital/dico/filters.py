import django_filters as filters
from . import models


class WordFilter(filters.FilterSet):

    class Meta:
        model = models.Word
        fields = ['label']
