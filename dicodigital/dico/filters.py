import django_filters as filters
from random import randint
from . import models


class WordFilter(filters.FilterSet):

    creator = filters.CharFilter(field_name='creator__username')
    first = filters.CharFilter(method='search_by_first_letter')
    def_like = filters.CharFilter(method='search_by_word_in_definition')
    empty = filters.BooleanFilter(method='search_without_definition')
    random = filters.BooleanFilter(method='get_random_word')

    class Meta:
        model = models.Word
        fields = ['label', 'creator', 'first', 'def_like']

    def search_by_first_letter(self, queryset, name, value):
        return queryset.filter(label__istartswith=value)

    def search_by_word_in_definition(self, queryset, name, value):
        return queryset.filter(definitions__text__icontains=value)

    def search_without_definition(self, queryset, name, value):
        return queryset.filter(definitions__isnull=value)

    def get_random_word(self, queryset, name, value):
        ids = [word.id for word in queryset.all()]
        ids.sort()
        if len(ids) > 1:
            return queryset.filter(id=randint(ids[0], ids[-1]))
        return queryset
