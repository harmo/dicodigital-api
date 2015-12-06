import django_filters as filters
from . import models


class WordFilter(filters.FilterSet):

    creator = filters.CharFilter(name='creator__username')

    class Meta:
        model = models.Word
        fields = ['label', 'creator']
