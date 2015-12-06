import django_filters as filters
from . import models


class WordFilter(filters.FilterSet):

    creator = filters.CharFilter(name='creator__username')
    first = filters.MethodFilter(action='search_by_first_letter')
    def_like = filters.MethodFilter(action='search_by_word_in_definition')

    class Meta:
        model = models.Word
        fields = ['label', 'creator', 'first', 'def_like']

    def search_by_first_letter(self, queryset, value):
        return queryset.filter(label__istartswith=value)

    def search_by_word_in_definition(self, queryset, value):
        return queryset.filter(definitions__text__icontains=value)
