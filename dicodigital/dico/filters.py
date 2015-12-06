import django_filters as filters
from . import models


class WordFilter(filters.FilterSet):

    creator = filters.CharFilter(name='creator__username')
    first = filters.MethodFilter(action='search_by_first_letter')

    class Meta:
        model = models.Word
        fields = ['label', 'creator', 'first']

    def search_by_first_letter(self, queryset, value):
        return queryset.filter(label__istartswith=value)
